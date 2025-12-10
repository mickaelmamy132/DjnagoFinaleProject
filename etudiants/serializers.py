from rest_framework import serializers
from .models import Etudiant
from bourses.models import Bourse
from datetime import date

class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'email', 'bourse', 'niveau', 'code_redoublement', 'numero_inscription', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        numero_inscription = validated_data.get('numero_inscription')
        # 1) Vérifier si l'étudiant existe déjà (réinscription)
        etudiant, created = Etudiant.objects.get_or_create(
            numero_inscription=numero_inscription,
            defaults=validated_data
        )

        # 2) Initialiser les variables
        montant_bourse = 0.0
        boursier = getattr(etudiant, 'boursier', "NON")  # si tu as ce champ
        niveau = etudiant.niveau
        code_redoublement = etudiant.code_redoublement

        # 3) Calcul de la bourse selon les règles
        if boursier == "OUI":
            if niveau in ["M2", "M1", "DOT1"]:
                montant_bourse = 48400.00 if code_redoublement == "N" else 48400.00 / 2
            elif niveau == "L3":
                montant_bourse = 36300.00 if code_redoublement == "N" else 36300.00 / 2
            elif niveau == "L2":
                montant_bourse = 30250.00 if code_redoublement == "N" else 30250.00 / 2
            elif niveau == "L1":
                montant_bourse = 20550.00 if code_redoublement == "N" else 20550.00 / 2
        elif boursier == "NON":
            if niveau in ["M2", "M1", "DOT1"] and code_redoublement == "T+":
                montant_bourse = 0
            elif niveau == "L3" and code_redoublement == "T+":
                montant_bourse = 0
            elif niveau == "L2" and code_redoublement == "T+":
                montant_bourse = 0
            elif niveau == "L1" and code_redoublement == "T+":
                montant_bourse = 0

        # 4) Créer une nouvelle bourse si c'est une réinscription ou première inscription
        today = date.today()
        Bourse.objects.create(
            etudiant=etudiant,
            montant=montant_bourse,
            annee_academique=f"{today.year}-{today.year + 1}",
            status="EN_ATTENTE",
            date_debut=today,
            date_fin=today,
            conditions="Bourse automatiquement attribuée (réinscription)" if not created else "Bourse automatiquement attribuée"
        )

        return etudiant
