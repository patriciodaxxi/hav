from itertools import chain

import graphene
from django.db.models import Q
from graphene_django.types import DjangoObjectType

from apps.sets.models import Node
from apps.sets.schema import NodeType
from apps.tags.schema import TagType
from hav_utils.imaginary import generate_thumbnail_url, generate_srcset_urls
from .models import Media, MediaCreator, License


class MediaType(DjangoObjectType):

    ancestors = graphene.List(NodeType)
    thumbnail_url = graphene.Field(graphene.String)
    srcset = graphene.List(graphene.String)
    type = graphene.Field(graphene.String)

    creation_timeframe = graphene.List(graphene.DateTime)
    tags = graphene.List(TagType)

    def resolve_creation_timeframe(self, info):
        # print(self.creation_date)
        return [self.creation_date.lower, self.creation_date.upper]

    def resolve_srcset(self, info):
        if self.primary_file:
            webasset_images = filter(
                lambda x: x.mime_type.startswith("image"),
                self.primary_file.webasset_set.all(),
            )
            try:
                webasset = list(webasset_images)[0]
            except IndexError:
                pass
            else:
                return [f"{src[1]} {src[0]}w" for src in generate_srcset_urls(webasset)]
        return []

    def resolve_type(self, info):
        if self.primary_file:
            return self.primary_file.mime_type
        return None

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_thumbnail_url(self, info):
        if self.primary_file:
            webasset_images = filter(
                lambda x: x.mime_type.startswith("image"),
                self.primary_file.webasset_set.all(),
            )
            webasset_images = list(webasset_images)
            try:
                webasset = webasset_images[0]
            except IndexError:
                return None
            else:
                return generate_thumbnail_url(webasset)
        return ""

    def resolve_ancestors(self, info):
        return chain(self.set.collection_ancestors, [self.set])

    @classmethod
    def get_queryset(cls, queryset, info):
        print("Filtering QS", queryset)
        return queryset

    class Meta:
        model = Media
        exclude = ["creation_date"]


class CreatorType(DjangoObjectType):
    class Meta:
        model = MediaCreator


class LicenseType(DjangoObjectType):
    class Meta:
        model = License


class Query:

    media = graphene.Field(MediaType, id=graphene.String(required=True))
    media_entries = graphene.List(MediaType, nodeID=graphene.String(required=True))

    def resolve_media(self, info, **kwargs):
        id = kwargs.get("id")
        return Media.objects.prefetch_related("files__webasset_set").get(
            Q(pk=id) | Q(original_media_identifier=id) | Q()
        )

    def resolve_media_entries(self, info, nodeID):
        node = Node.objects.get(pk=nodeID)
        return Media.objects.prefetch_related("files__webasset_set").filter(set=node)
