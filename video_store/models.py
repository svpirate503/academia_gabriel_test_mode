
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.db.models import JSONField

class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255,null=True)
    stripeSubscriptionId = models.CharField(max_length=255,null=True)
    customer_email = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True, null=True)  # Estado de la suscripción ('active', 'canceling', etc.)

    def __str__(self):
        return self.user.username
    


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to='categorias_thumbnails/')

    def __str__(self):
        return self.nombre
    

class Post(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='posts')
    nombre = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='posts_thumbnails/')
    # Asumimos que las lecciones de video se gestionan por otro modelo

    def __str__(self):
        return self.nombre
    

class LeccionVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='lecciones_video')
    titulo = models.CharField(max_length=100)
    url = models.TextField()

    def __str__(self):
        return self.titulo
    def codigo_safe(self):
        return mark_safe(self.url)
    
   
class Capitulo(models.Model):
    name_category = models.CharField(max_length=100)
    videos = JSONField(default=list) 


    def __str__(self):
        return self.name_category


