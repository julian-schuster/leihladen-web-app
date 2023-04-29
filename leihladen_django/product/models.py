from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    image2 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    image3 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail3 = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default = 1, validators=[MinValueValidator(0)])
    available = models.IntegerField(default = 1, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def clean(self):
        if self.available > self.quantity:
            raise ValidationError("Die verfügbare Menge kann nicht größer sein als die Gesamtmenge.")
        
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=98)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def save(self, *args, **kwargs):
        # Erstelle Thumbnails für Bild 1
        if self.image:
            super().save(*args, **kwargs)  # Speichere zuerst das Modell, um einen slug zu haben
            if not self.thumbnail:
                self.thumbnail = self.make_thumbnail(self.image, size=(300, 200))
                self.save(update_fields=['thumbnail'])

        # Erstelle Thumbnails für Bild 2
        if self.image2:
            super().save(*args, **kwargs)  # Speichere zuerst das Modell, um einen slug zu haben
            if not self.thumbnail2:
                self.thumbnail2 = self.make_thumbnail(self.image2, size=(300, 200))
                self.save(update_fields=['thumbnail2'])

        # Erstelle Thumbnails für Bild 3
        if self.image3:
            super().save(*args, **kwargs)  # Speichere zuerst das Modell, um einen slug zu haben
            if not self.thumbnail3:
                self.thumbnail3 = self.make_thumbnail(self.image3, size=(300, 200))
                self.save(update_fields=['thumbnail3'])

        super().save(*args, **kwargs)  # Speichere das Modell komplett

    def get_images(self):
        images = []
        if self.image:
            images.append({'url': 'http://127.0.0.1:8000' + self.image.url, 'thumbnail': self.get_thumbnail()})
        if self.image2:
            images.append({'url': 'http://127.0.0.1:8000' + self.image2.url, 'thumbnail': self.get_thumbnail()})
        if self.image3:
            images.append({'url': 'http://127.0.0.1:8000' + self.image3.url, 'thumbnail': self.get_thumbnail()})
        return images

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_text = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist {self.id}"