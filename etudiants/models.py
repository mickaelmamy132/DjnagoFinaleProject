from django.db import models

class Etudiant(models.Model):
    """Profil d'étudiant avec informations supplémentaires"""
    bourse = models.FloatField(default=0)
    boursier = models.CharField(max_length=10)
    numero_inscription = models.CharField(max_length=50, unique=True)
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=15)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    cin = models.CharField(max_length=12)  
    annee_bacc = models.DateField()
    code_redoublement = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    
    mention = models.CharField(max_length=50)
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