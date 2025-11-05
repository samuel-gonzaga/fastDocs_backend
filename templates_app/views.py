from rest_framework import viewsets, decorators, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import APIException
from django.db import transaction

from templates_app.models import Template
from templates_app.serializers import TemplateSerializer
from templates_app.utils.placeholder_extractor import PlaceholderExtractor
from core.utils.exceptions import ValidationError  # se existir no seu projeto
from core.utils.formatters import format_serializer_error  # idem


class TemplateViewSet(viewsets.ModelViewSet):
    """Gerencia templates de documentos"""
    queryset = Template.objects.all().order_by('-created_at')
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = serializer.save()
        return Response(TemplateSerializer(template).data, status=status.HTTP_201_CREATED)


    @decorators.action(detail=True, methods=['get'])
    def placeholders(self, request: Request, pk=None):
        """Retorna apenas os placeholders de um template específico"""
        try:
            template = self.get_object()
            return Response({
                "template": template.name,
                "placeholders": template.placeholders
            })
        except Template.DoesNotExist:
            raise APIException("Template não encontrado.")
