from rest_framework import serializers
from .models import Etudiant

class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'email', 'date_naissance', 'created_by']
        read_only_fields = ['created_by']  # On ne veut pas que le front définisse l'utilisateur
