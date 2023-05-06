from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, max_length=255)

    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return self.name

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

    def get_images(self):
        images = []
        if self.image:
            images.append({'url': 'http://127.0.0.1:8000' + self.image.url})
        if self.image2:
            images.append({'url': 'http://127.0.0.1:8000' + self.image2.url})
        if self.image3:
            images.append({'url': 'http://127.0.0.1:8000' + self.image3.url})
        if self.image4:
            images.append({'url': 'http://127.0.0.1:8000' + self.image4.url})
        return images

    def get_category_name(self):
        return self.category.name
    
class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    qr_code_text = models.TextField(blank=True, null=True)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
        
    def __str__(self):
        return f"Wishlist {self.id}"