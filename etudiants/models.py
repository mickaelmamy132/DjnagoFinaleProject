from django.db import models

class Etudiant(models.Model):
    """Profil d'étudiant avec informations supplémentaires"""
    # paiement = models.IntegerField('paiements.Paiement', on_delete=models.CASCADE,null=True, blank=True, related_name='etudiant_Profil')
    paiement = models.IntegerField()
    bourse = models.FloatField()
    numero_inscription = models.CharField(max_length=50, unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=15)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    cin = models.CharField(max_length=12)  
    annee_bacc = models.DateField()
    code_redoublement = models.IntegerField(null=True, blank=True)
    faculte = models.CharField(max_length=50)
    domaine = models.CharField(max_length=50)
    niveau = models.CharField(max_length=15)
    
    nationalite = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='Etudiant/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Etudiant: {self.nom} {self.prenom}"