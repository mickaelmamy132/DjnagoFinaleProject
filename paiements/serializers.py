from rest_framework import serializers
from .models import Paiement, EcheancierPaiement
from etudiants.models import Etudiant


class PaiementIndividuelSerializer(serializers.ModelSerializer):
    echeancier = serializers.DictField(write_only=True, required=False)

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
        ]
        read_only_fields = ['date_paiement', 'date_confirmation']

    def create(self, validated_data):
        echeancier_data = validated_data.pop('echeancier', None)
        etudiant = validated_data['etudiant']

        # 🔹 Calcul automatique de la bourse avec conditions
        if etudiant.boursier != "OUI":
            montant_bourse = 0.0
        elif etudiant.code_redoublement == "T":
            montant_bourse = 0.0
        else:
            montants = {
                "M2": 48400.00,
                "M1": 48400.00,
                "DOT1": 48400.00,
                "L3": 36300.00,
                "L2": 30250.00,
                "L1": 20550.00,
            }
            montant_base = montants.get(etudiant.niveau, 0.0)

            if etudiant.code_redoublement == "R":
                montant_bourse = montant_base / 2
            else:
                montant_bourse = montant_base

        validated_data['montant'] = montant_bourse

        paiement = Paiement.objects.create(**validated_data)

        if echeancier_data:
            EcheancierPaiement.objects.create(
                etudiant=paiement.etudiant,
                nombre_echeances=echeancier_data.get('nombre_echeances', 3),
                montant_par_echeance=echeancier_data.get('montant_par_echeance')
            )
        return paiement


class PaiementCollectifSerializer(serializers.Serializer):
    faculte = serializers.CharField()
    status = serializers.CharField(default="EN_ATTENTE")
    notes = serializers.CharField(required=False, allow_blank=True)
    echeancier = serializers.DictField(write_only=True, required=False)

    def create(self, validated_data):
        faculte = validated_data.get('faculte')
        echeancier_data = validated_data.pop('echeancier', None)

        etudiants = Etudiant.objects.filter(faculte=faculte)
        paiements = []

        for etudiant in etudiants:
            # 🔹 Calcul automatique de la bourse avec conditions
            if etudiant.boursier != "OUI":
                montant_bourse = 0.0
            elif etudiant.code_redoublement == "T":
                montant_bourse = 0.0
            else:
                montants = {
                    "M2": 48400.00,
                    "M1": 48400.00,
                    "DOT1": 48400.00,
                    "L3": 36300.00,
                    "L2": 30250.00,
                    "L1": 20550.00,
                }
                montant_base = montants.get(etudiant.niveau, 0.0)

                if etudiant.code_redoublement == "R":
                    montant_bourse = montant_base / 2
                else:
                    montant_bourse = montant_base

            paiement = Paiement.objects.create(
                etudiant=etudiant,
                montant=montant_bourse,
                montant_restant=0,
                status=validated_data.get('status', "EN_ATTENTE"),
                notes=validated_data.get('notes', "")
            )
            paiements.append(paiement)

            if echeancier_data:
                EcheancierPaiement.objects.create(
                    etudiant=etudiant,
                    nombre_echeances=echeancier_data.get('nombre_echeances', 3),
                    montant_par_echeance=echeancier_data.get('montant_par_echeance')
                )

        return paiements


class EcheancierPaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcheancierPaiement
        fields = [
            'id',
            'etudiant',
            'nombre_echeances',
            'montant_par_echeance',
            'created_at',
        ]
        read_only_fields = ['created_at']
