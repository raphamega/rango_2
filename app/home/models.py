from django.db import models

# Create your models here.
class Pag_Contato(models.Model):
    nome = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    mensagem = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.nome
    

class Texto(models.Model):
    titulo = models.CharField(max_length=100)
    texto = models.TextField(max_length=500)
    image = models.ImageField(upload_to='text_image/',  blank=True, null=True)

    def __str__(self):
        return self.titulo
    
