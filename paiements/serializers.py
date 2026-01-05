from rest_framework import serializers
from .models import Paiement, EcheancierPaiement
from etudiants.models import Etudiant  # Assure-toi que ton modèle Etudiant a un champ faculte

class PaiementSerializer(serializers.ModelSerializer):
    echeancier = serializers.DictField(write_only=True, required=False)
    faculte = serializers.CharField(write_only=True, required=False)  # Nouveau champ

    class Meta:
        model = Paiement
        fields = [
            'id',
            'etudiant',
            'montant',
            'montant_restant',
            'status',
            'date_paiement',
            'date_confirmation',
            'notes',
            'echeancier',
            'faculte',  # champ facultatif
        ]
        read_only_fields = ['date_paiement', 'date_confirmation']

    def create(self, validated_data):
        echeancier_data = validated_data.pop('echeancier', None)
        faculte = validated_data.pop('faculte', None)

        paiements = []

        if faculte:
            # Paiement collectif : tous les étudiants de la faculté
            etudiants = Etudiant.objects.filter(faculte=faculte)
            for etudiant in etudiants:
                paiement = Paiement.objects.create(etudiant=etudiant, **validated_data)
                paiements.append(paiement)

                if echeancier_data:
                    EcheancierPaiement.objects.create(
                        etudiant=etudiant,
                        nombre_echeances=echeancier_data.get('nombre_echeances', 3),
                        montant_par_echeance=echeancier_data.get('montant_par_echeance')
                    )
        else:
            # Paiement individuel
            paiement = Paiement.objects.create(**validated_data)
            paiements.append(paiement)

            if echeancier_data:
                EcheancierPaiement.objects.create(
                    etudiant=paiement.etudiant,
                    nombre_echeances=echeancier_data.get('nombre_echeances', 3),
                    montant_par_echeance=echeancier_data.get('montant_par_echeance')
                )

        # Retourne le premier paiement (DRF attend un seul objet)
        return paiements[0]



# POST /paiements/
# {
#   "etudiant": 5,
#   "montant": 2000,
#   "status": "EN_ATTENTE",
#   "notes": "Paiement individuel",
#   "echeancier": {
#     "nombre_echeances": 2,
#     "montant_par_echeance": 1000
#   }
# }


# POST /paiements/
# {
#   "faculte": "Sciences",
#   "montant": 1500,
#   "status": "EN_ATTENTE",
#   "notes": "Paiement bourse pour toute la faculté",
#   "echeancier": {
#     "nombre_echeances": 3,
#     "montant_par_echeance": 500
#   }
# }
