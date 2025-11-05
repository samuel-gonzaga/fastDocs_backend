from rest_framework.routers import DefaultRouter

from templates_app.views import TemplateViewSet

router = DefaultRouter()
router.register('', TemplateViewSet, basename='template')

urlpatterns = router.urls