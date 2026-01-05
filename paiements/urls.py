from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaiementIndividuelSerializer,PaiementCollectifViewSet

router = DefaultRouter()
router.register(r'paiements-individuels', PaiementIndividuelSerializer, basename='paiement-individuel') 
router.register(r'paiements-collectifs', PaiementCollectifViewSet, basename='paiement-collectif')
# router.register(r'echeanciers', EcheancierPaiementViewSet, basename='echeanciers')
# router.register(r'versements', VersementEcheanceViewSet, basename='versements')

urlpatterns = [
    path('', include(router.urls)),
]
