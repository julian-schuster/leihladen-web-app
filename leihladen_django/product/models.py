from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('name',)  #Kategorien nach ID aufsteigend sortieren

    #Eine Zeichenkette zurückgeben, die den Namen der Kategorie enthält
    def __str__(self):
        return self.name

    #Gibt die absolute URL der Kategorie zurück
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=10, unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    description = models.TextField(blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    smallPieces = models.BooleanField(default=False)
    deposit = models.CharField(max_length=10, blank=True, null=True)
    fee = models.CharField(max_length=10,blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image2 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image3 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image4 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    images = models.JSONField(default=list, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    available = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.id

    def clean(self):
        if self.available > self.quantity:
            raise ValidationError("Die verfügbare Menge kann nicht größer sein als die Gesamtmenge.")

    def get_absolute_url(self):
        if len(self.categories.all()) > 1:
            return f'/{self.categories.all()[1].slug}/{self.id}/'
        else:
            return f'/{self.categories.all()[0].slug}/{self.id}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        if self.images:
            return 'http://127.0.0.1:8000/media/uploads/' + self.images[0]
        return {}

    def get_images(self):
        images = []
        for image in self.images:
            images.append({'http://127.0.0.1:8000/media/uploads/' + image})
        return images

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_text = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',) #Wunschliste nach Dateum absteigend sortieren.
        
    def __str__(self):
        return f"Wishlist {self.id}" #Gibt die ID der Wunschliste als Zeichenfolge zurück.