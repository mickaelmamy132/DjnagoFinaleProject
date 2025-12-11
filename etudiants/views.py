from rest_framework import viewsets, status
from .models import Etudiant
from .serializers import EtudiantSerializer, EtudiantDetailSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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
    
    @action(detail=False, methods=['get'])
    def affiche_etudiant(self, request):
        try:
            etudiant = request.Etudiant
            serializer = EtudiantDetailSerializers(etudiant)
            return Response(serializer.data)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Etudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False,methods=['put'])
    def mettre_a_jou_etud(self, request):
        try:
            etudiant = request.Etudiant
            serializer = EtudiantDetailSerializers(etudiant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Etudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        

    