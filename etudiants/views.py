from rest_framework import viewsets
from .models import Etudiant
from .serializers import EtudiantSerializer
from rest_framework.permissions import IsAuthenticated

class EtudiantViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les étudiants.
    - GET /etudiants/        : liste des étudiants
    - GET /etudiants/{id}/   : détails d’un étudiant
    - POST /etudiants/       : création d’un étudiant + création automatique de la bourse
    - PUT /etudiants/{id}/   : mise à jour
    - PATCH /etudiants/{id}/ : mise à jour partielle
    - DELETE /etudiants/{id}/: suppression
    """
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    permission_classes = [IsAuthenticated]
