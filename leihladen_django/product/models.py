from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)

    class Meta:
        ordering = ('id',)  #Kategorien nach ID aufsteigend sortieren

    #Eine Zeichenkette zurückgeben, die den Namen der Kategorie enthält
    def __str__(self):
        return self.name

    #Gibt die absolute URL der Kategorie zurück
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image2 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image3 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    image4 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default = 1, validators=[MinValueValidator(0)])
    available = models.IntegerField(default = 1, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-date_added',)  #Artikel nach Datum absteigend sortieren.

    def __str__(self):
        return self.name  #Gibt den Namen des Objekts als Zeichenfolge zurück.

    def clean(self):
        if self.available > self.quantity:  #Überprüft, ob die verfügbare Menge größer ist als die Gesamtmenge.
            raise ValidationError("Die verfügbare Menge kann nicht größer sein als die Gesamtmenge.")  
        
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'  #Gibt die absolute URL des Objekts zurück, die aus dem Slug des übergeordneten Kategorie-Objekts und dem eigenen Slug besteht.

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url  #Gibt die URL des Hauptbildes zurück.
        return '' 

    def get_images(self):
        images = []
        if self.image:
            images.append({'url': 'http://127.0.0.1:8000' + self.image.url})  # Fügt das Hauptbild in die Liste der Bilder hinzu.
        if self.image2:
            images.append({'url': 'http://127.0.0.1:8000' + self.image2.url})  # Fügt das zweite Bild in die Liste der Bilder hinzu.
        if self.image3:
            images.append({'url': 'http://127.0.0.1:8000' + self.image3.url})  # Fügt das dritte Bild in die Liste der Bilder hinzu.
        if self.image4:
            images.append({'url': 'http://127.0.0.1:8000' + self.image4.url})  # Fügt das vierte Bild in die Liste der Bilder hinzu.
        return images  #Gibt die Liste der Bilder zurück.

    def get_category_name(self):
        return self.category.name  #Gibt den Namen der übergeordneten Kategorie des Objekts zurück.

    
class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_text = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',) #Wunschliste nach Dateum absteigend sortieren.
        
    def __str__(self):
        return f"Wishlist {self.id}" #Gibt die ID der Wunschliste als Zeichenfolge zurück.