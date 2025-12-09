from rest_framework import viewsets
from .models import Etudiant
from .serializers import EtudiantSerializer
from rest_framework.permissions import IsAuthenticated

class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer
    permission_classes = [IsAuthenticated]
