import logging

from django.db import transaction
from psycopg2.extras import DateTimeTZRange
from rest_framework import serializers

from apps.archive.models import ArchiveFile
from apps.archive.operations.hash import generate_hash
from apps.archive.tasks import archive
from apps.webassets.tasks import create as create_webassets
from apps.ingest.models import IngestQueue
from apps.hav_collections.models import Collection
from apps.media.models import MediaToCreator, MediaCreatorRole, Media, MediaCreator, License
from .fields import HAVTargetField, IngestHyperlinkField, FinalIngestHyperlinkField, \
    InternalIngestHyperlinkField, IngestionReferenceField

from .resolver import resolveIngestionItems


logger = logging.getLogger(__name__)


class MediaLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = License
        fields = [
            'id',
            'name'
        ]


class MediaCreatorRoleSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, mcr):
        return str(mcr)

    class Meta:
        model = MediaCreatorRole
        fields = ['id', 'name']


class MediaCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaToCreator
        fields = ['role', 'creator']


class SimpleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['pk', 'creators', 'license', 'creation_date']


class IngestionItemSerializer(serializers.Serializer):

    path = serializers.ListField(serializers.CharField(max_length=200))

    item = FinalIngestHyperlinkField()


class PrepareIngestSerializer(serializers.Serializer):

    target = HAVTargetField()

    items = serializers.ListField(
        child=IngestHyperlinkField()
    )


class IngestSerializer(serializers.Serializer):

    source = InternalIngestHyperlinkField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

    creators = serializers.PrimaryKeyRelatedField(queryset=MediaCreator.objects.all(), many=True)
    license = serializers.PrimaryKeyRelatedField(queryset=License.objects.all())

    media_type = serializers.ChoiceField(choices=Media.MEDIA_TYPE_CHOICES)
    media_description = serializers.CharField(allow_blank=True, required=False)
    media_identifier = serializers.CharField(allow_blank=True, required=False)

    @property
    def target(self):
        return self.context['target']

    @property
    def collection(self):
        try:
            return self.target.collection
        except Collection.DoesNotExist:
            ancestor = self.target.get_ancestors().filter(collection__isnull=False).last()
            if ancestor is None:
                return None
            else:
                return ancestor.collection

        return None


    def validate_source(self, value):
        try:
            hash = generate_hash(value)
        except FileNotFoundError:
            raise serializers.ValidationError("The file could not be found.")

        try:
            ArchiveFile.objects.get(hash=hash)
            raise serializers.ValidationError("A file with the hash %s is already archived." % hash)
        except ArchiveFile.DoesNotExist:
            return value

    def validate(self, data):
        user = self.context['user']
        if user not in self.collection.administrators or not user.is_superuser:
            raise serializers.ValidationError('You do not have the appropriate permissions to ingest into the collection "{}"'.format(self.collection.name))

        if data['start'] > data['end']:
            raise serializers.ValidationError("Start time must be before end time.")
        if not self.target.is_descendant_of(self.collection.root_node) and not self.target == self.collection.root_node:
            raise serializers.ValidationError("Target set is not a descendant of the specified collection.")

        return data


    def create(self, validated_data):
        user = self.context['user']
        dt_range = DateTimeTZRange(lower=validated_data['start'], upper=validated_data['end'])

        # actually create the media object
        media = Media.objects.create(
            creation_date=dt_range,
            license=validated_data.get('license'),
            set=self.target,
            collection=self.collection,
            created_by=user,
            original_media_type=validated_data['media_type'],
            original_media_description=validated_data.get('media_description', ''),
            original_media_identifier=validated_data.get('media_identifier', '')
        )

        # save m2m
        for creator in validated_data['creators']:
            MediaToCreator.objects.create(
                creator=creator,
                media=media
            )

        logger.info(
            "Triggering archiving for file %s, media: %d, user: %d",
            str(validated_data['source']),
            media.pk,
            user.pk
        )

        def ingestion_trigger():
            return (
                archive.s(str(validated_data['source']), media.pk, user.pk) |
                create_webassets.s()
            )()

        # this instructs django to execute the function after any commit
        transaction.on_commit(ingestion_trigger)
        return media


class SimpleIngestQueueSerializer(serializers.ModelSerializer):
    target = HAVTargetField()

    item_count = serializers.SerializerMethodField()
    ingested_item_count = serializers.SerializerMethodField()

    def get_item_count(self, obj):
        return len(obj.ingestion_items)

    def get_ingested_item_count(self, obj):
        return len(obj.ingested_items)

    class Meta:
        model = IngestQueue
        fields = [
            'uuid',
            'target',
            'name',
            'item_count',
            'ingested_item_count',
            # 'ingestion_',
            'created_at'
        ]


class IngestQueueSerializer(serializers.ModelSerializer):

    target = HAVTargetField()

    selection = serializers.ListField(child=IngestionReferenceField(), write_only=True)

    media_entries = serializers.SerializerMethodField()

    def create(self, validated_data):
        logger.debug('creating queue: %s', validated_data)
        q = IngestQueue(
            target=validated_data['target'],
            name=validated_data['name'],
            created_by=self.context['request'].user
        )
        q.add_items(validated_data['selection'])
        q.save(force_insert=True)
        return q

    def get_media_entries(self, iq):
        field = IngestionReferenceField()
        items = []
        for k, v in iq.ingestion_items.items():
            items.append(field.get_file_path(k))

        # print(resolveIngestionItems(items))

        return []

    class Meta:
        model = IngestQueue
        fields = [
            'uuid',
            'name',
            'target',
            'selection',
            'ingestion_items',
            'ingested_items',
            'media_entries'
        ]
