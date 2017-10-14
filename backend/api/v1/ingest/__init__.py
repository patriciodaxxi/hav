from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from datetime import date
from apps.media.models import MediaCreator, MediaCreatorRole, License
from ..permissions import IncomingBaseMixin
from .serializers import MediaCreatorRoleSerializer, MediaLicenseSerializer, BatchMediaSerializer



class PrepareIngestView(IncomingBaseMixin, APIView):

    def post(self, request):

        files = set(request.data.get('files', []))
        creators = [{'id': mc.pk, 'name': str(mc)} for mc in MediaCreator.objects.all()]
        roles = MediaCreatorRoleSerializer(MediaCreatorRole.objects.all(), many=True).data
        licenses = MediaLicenseSerializer(License.objects.all(), many=True).data

        today = date.today()

        return Response({
            'files': [{
                'ingest_id': f,
                'initial_data': {
                    'year': today.year,
                    'month': today.month,
                    'day': today.day
                }
            } for f in files],
            'options': {
                'creators': creators,
                'roles': roles,
                'licenses': licenses,
            }
        })


class IngestView(IncomingBaseMixin, CreateAPIView):

    serializer_class = BatchMediaSerializer

