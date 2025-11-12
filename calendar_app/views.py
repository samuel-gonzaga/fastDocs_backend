from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwnerOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal para o modelo Event.

    Regras:
    - Eventos da categoria "outro" (ou "other") são ocultos por padrão;
    - Podem ser exibidos apenas se a senha for enviada corretamente via query param;
    - Inclui rota adicional `/stats` e ação `/unlock/<id>/`.
    """
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'time']

    def get_queryset(self):
        """
        Controla quais eventos são retornados na listagem.
        """
        queryset = Event.objects.all()
        category = self.request.GET.get('category')
        password = self.request.GET.get('password')

        # Normaliza nomes (garante que 'outro' e 'other' funcionem)
        if category in ['outro', 'other']:
            if password:
                queryset = queryset.filter(category='outro', password=password)
            else:
                # Nenhuma senha -> nenhum evento sensível retornado
                return Event.objects.none()
        else:
            # Exclui eventos sensíveis por padrão
            queryset = queryset.exclude(category__in=['outro', 'other'])

        return queryset

    def perform_create(self, serializer):
        """
        Cria evento. (Caso haja autenticação no futuro, pode vincular ao user.)
        """
        serializer.save()

    @action(detail=False, methods=['get'], url_path='stats')
    def get_stats(self, request):
        """
        Retorna um resumo estatístico simples por categoria.
        """
        events = Event.objects.all()
        return Response({
            "total_events": events.count(),
            "meeting_count": events.filter(category='meeting').count(),
            "payment_count": events.filter(category='payment').count(),
            "other_count": events.filter(category__in=['outro', 'other']).count(),
        })

    @action(detail=True, methods=['post'], url_path='unlock')
    def unlock_event(self, request, pk=None):
        """
        Desbloqueia um evento da categoria 'outro' com senha.
        """
        event = self.get_object()

        if event.category not in ['outro', 'other']:
            return Response(
                {"detail": "Este evento não requer senha."},
                status=status.HTTP_400_BAD_REQUEST
            )

        password = request.data.get('password')
        if not password:
            return Response(
                {"detail": "Senha obrigatória."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password == event.password:
            serializer = self.get_serializer(event)
            return Response(serializer.data)

        return Response(
            {"detail": "Senha incorreta."},
            status=status.HTTP_403_FORBIDDEN
        )
