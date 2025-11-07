from rest_framework import viewsets, decorators, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import APIException

from templates_app.models import Template
from templates_app.serializers import TemplateSerializer
from templates_app.utils.placeholder_extractor import PlaceholderExtractor
from core.utils.exceptions import ValidationError
from core.utils.formatters import format_serializer_error

from docxtpl import DocxTemplate
from io import BytesIO
from django.http import HttpResponse


class TemplateViewSet(viewsets.ModelViewSet):
    """Gerencia templates de documentos"""
    queryset = Template.objects.all().order_by('-created_at')
    serializer_class = TemplateSerializer
    permission_classes = [AllowAny]

    def create(self, request: Request, *args, **kwargs):
        """
        Cria um template no banco, armazena o binário do arquivo e extrai placeholders.
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            error_message = format_serializer_error(serializer.errors)
            raise ValidationError(detail=error_message)

        # Salva o template (o arquivo é convertido em binário no serializer)
        template = serializer.save()

        # Extrai placeholders diretamente da memória
        try:
            file_stream = BytesIO(template.file_content)
            template.placeholders = PlaceholderExtractor.extract(file_stream)
            template.save(update_fields=['placeholders'])
        except Exception as e:
            print(f"[ERRO] Falha ao extrair placeholders: {e}")

        return Response(
            TemplateSerializer(template).data,
            status=status.HTTP_201_CREATED
        )

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

    @decorators.action(detail=True, methods=['post'])
    def generate(self, request: Request, pk=None):
        """
        Gera um documento preenchido com base nos dados enviados.
        Retorna o arquivo .docx diretamente em memória, sem salvar localmente.
        """
        try:
            template = self.get_object()
            output_name = request.data.get("output_name", template.name)
            context_data = request.data.get("data", {})

            if not isinstance(context_data, dict):
                raise ValidationError(detail="O campo 'data' deve ser um objeto com os placeholders e valores.")

            # Carrega o template direto do binário
            doc = DocxTemplate(BytesIO(template.file_content))
            doc.render(context_data)

            # Salva o resultado em memória
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            # Retorna o arquivo em memória
            response = HttpResponse(
                buffer.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            response["Content-Disposition"] = f'attachment; filename=\"{output_name}.docx\"'
            return response

        except Template.DoesNotExist:
            raise APIException("Template não encontrado.")
        except Exception as e:
            raise APIException(f"Erro ao gerar documento: {str(e)}")
