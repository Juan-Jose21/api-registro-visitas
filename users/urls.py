from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views import UsuarioViewSet, VisitaViewSet, IngresoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'visitas', VisitaViewSet)
router.register(r'ingresos', IngresoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
