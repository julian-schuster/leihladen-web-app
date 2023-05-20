from django.db.models import Sum, Q
from django.http import Http404
from slugify import slugify
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Wishlist
from .serializers import ProductSerializer, CategorySerializer, CategorySerializerLight, WishlistSerializer
import base64

class Products(APIView):
    # API-Endpunkt, um alle Produkte abzurufen.
    def get(self, request, format=None):
        products = Product.objects.all()
        available_count = products.aggregate(total=Sum('available'))['total']
        total_count = products.aggregate(total=Sum('quantity'))['total']
        serializer = ProductSerializer(products, many=True)
        data = {'products': serializer.data, 'quantity': total_count, 'available_count': available_count}
        return Response(data, status=status.HTTP_200_OK)


class LatestProductsList(APIView):
    # API-Endpunkt, um die neuesten 4 Produkte abzurufen.
    def get(self, request, format=None):
        products = Product.objects.order_by('-date_added').all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        # Hilfsfunktion, um das Produkt anhand der Kategorie-Slugs und des Produkt-Slugs zu finden.
        try: 
            return Product.objects.filter(categories__slug__in=category_slug).get(id=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        # GET-Request, um ein Produkt anhand der Kategorie-Slugs und des Produkt-Slugs abzurufen.
        category_slug = category_slug.split(',')
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetail(APIView):
    # API-Endpunkt um eine Kategorie anhand ihres Slugs abzurufen.
    def get_object(self, category_slug):
        try: 
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    #GET-Request Gibt eine bestimmte Kategorie mit zugehörigen Produkten zurück.
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Sucht nach Produkten anhand des Suchbegriffs im Namen oder der Beschreibung.
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query))
    else:
        products = Product.objects.all()
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class GetCategories(APIView):
    #API-Endpunkt der alle Kategorien zurückgibt. Endpunkt dauert länger weil in CategorySerializer jede Kategorie mit jedem Produkt in Beziehung gesetzt wird. 
    #Wichtig für Kategorieansicht und laden aller Produkte in einer Kategorie
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetCategoriesLight(APIView):
    #API-Endpunkt der alle Kategorien zurückgibt. Schnelle Version die nur id, name und absolute_url zurückgibt ohne die Beziehung zu den Produkten.
    #Wichtig für Performance an Stellen wo man nur die Kategorienamen braucht.
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializerLight(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryManagement(APIView):
    permission_classes = [IsAuthenticated]
    #API-Endpunkt der eine neue Kategorie erstellt, bearbeitet und entfernt

    #Neue Kategorie erstellen
    def post(self, request):
        categoryName = request.data.get('categoryName')
        categorySlug = slugify(categoryName, allow_unicode=True)
        category = Category(name=categoryName, slug=categorySlug)
        category.save()
        return Response(status=status.HTTP_201_CREATED)
      

    #Kategorie bearbeiten
    def put(self, request):
        categoryId = request.data.get('id')
        categoryNewName = request.data.get('newName')
        category = Category.objects.get(id=categoryId)
        category.name = categoryNewName
        category.slug = slugify(categoryNewName, allow_unicode=True)
        category.save()
        return Response(status=status.HTTP_200_OK)

    #Kategorie löschen
    def delete(self, request, id):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetWishlist(APIView):
    #API-Endpunkt der die Wunschliste eines bestimmten Benutzers zurückgibt.
    def get(self, request, client_id, format=None):
        try: 
            wishlist = Wishlist.objects.get(client_id=client_id)
            qr_code_text = wishlist.qr_code_text
            date_added = wishlist.date_added
            data = {
                "qr_code_text": qr_code_text,
                "date_added": date_added
            }
            return Response(data, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            raise Http404
    
class CreateWishlist(APIView):
    #API-Endpunkt der eine neue Wunschliste erstellt oder aktualisiert.
    def post(self, request):
        qr_code_text = request.data.get('qr_code_text')
        client_id = request.data.get('client_id')
        
        # Versuche, die Wishlist des Clients zu finden oder zu aktualisieren
        wishlist, created = Wishlist.objects.update_or_create(
            client_id=client_id,
            defaults={'qr_code_text': qr_code_text}
        )

        if created:
            # Wenn eine neue Wishlist erstellt wurde
            response_data = {
                'status': 'Wunschliste wurde erstellt', 
                'wishlist_id': wishlist.id, 
                'client_id': client_id
            }
            status_code = status.HTTP_201_CREATED
        else:
            # Wenn die Wishlist des Clients aktualisiert wurde
            response_data = {'status': 'Wunschliste wurde aktualisiert.'}
            status_code = status.HTTP_200_OK

        return Response(response_data, status=status_code)
      
class Wishlists(APIView):
    #API-Endpunkt, um alle Wishlists sowie ihre Anzahl zurückzugeben.
    def get(self, request, format=None):
        wishlists = Wishlist.objects.all()
        wishlist_count = wishlists.count()
        
        serializer = WishlistSerializer(wishlists, many=True)
        response_data = {'wishlists': serializer.data, 'count': wishlist_count}
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class ProductAvailability(APIView):
    #API-Endpunkt um die Verfügbarkeit von Artikeln zu ändern.
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        # Produkt mit der gegebenen ID abrufen
        product = Product.objects.get(id=id)

        # Den neuen Verfügbarkeitswert aus den Anfragedaten abrufen
        value = request.data.get('value', None)

        if value is not None:
            # Die neue Verfügbarkeit berechnen
            new_available = product.available + value

            # Überprüfen, ob die neue Verfügbarkeit gültig ist
            if new_available < 0:
                # Wenn die neue Verfügbarkeit ungültig ist, Fehlermeldung zurückgeben
                return Response({'error': 'Die Verfügbarkeit darf nicht unter 0 fallen.'}, status=status.HTTP_400_BAD_REQUEST)
            elif new_available > product.quantity:
                # Wenn die neue Verfügbarkeit ungültig ist, Fehlermeldung zurückgeben
                return Response({'error': 'Die Verfügbarkeit darf nicht größer als der aktuelle Bestand sein.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Wenn die neue Verfügbarkeit gültig ist, Produkt aktualisieren und zurückgeben
                product.available = new_available
                product.save()
                serialized_product = ProductSerializer(product).data
                return Response(serialized_product, status=status.HTTP_200_OK)
        else:
            # Wenn der neue Verfügbarkeitswert nicht gegeben ist, Fehlermeldung zurückgeben
            return Response({'error': 'Fehler beim Aktualisieren der Verfügbarkeit'}, status=status.HTTP_400_BAD_REQUEST)

        
class ProductManagement(APIView):
    #API-Endpunkt um Artikel hinzuzufügen, Artikel zu entfernen und Artikeln zu bearbeiten.
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            # Serialize the product to JSON
            serialized_product = ProductSerializer(product).data
            return Response(serialized_product, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    #POST-Request um ein Artikel hinzuzufügen
    def post(self, request):
        id = request.data.get('id')

        # Überprüfen, ob die ID bereits vorhanden ist
        if Product.objects.filter(id=id).exists():
            return Response({'error': 'Ein Artikel mit dieser ID existiert bereits.'}, status=status.HTTP_409_CONFLICT)
        
        name = request.data.get('name')
        description = request.data.get('description')
        quantity = request.data.get('quantity')
        image = request.data.get('image')
        image2 = request.data.get('image2')
        image3 = request.data.get('image3')
        image4 = request.data.get('image4')
        categories = request.data.get('categories')
        dimension = request.data.get('dimension')
        weight = request.data.get('weight')
        deposit = request.data.get('deposit')
        fee = request.data.get('fee')
        smallPieces = request.data.get('smallPieces')

        # Konvertiere die Kategorien-IDs in eine Liste von Ganzzahlen
        categories = [int(cat_id) for cat_id in categories.split(',')]

        # Holt die Kategorien mit den gegebenen IDs aus der Datenbank
        categories_objs = Category.objects.filter(id__in=categories)
        
        slug = slugify(name, allow_unicode=True)

        if smallPieces == 'true':
            smallPieces = True
        else :
            smallPieces = False

        # Erstellt ein neues Artikel-Objekt mit den übergebenen Daten
        product = Product(id=id, name=name, slug=slug, description=description, quantity=quantity, dimension=dimension, weight=weight, deposit=deposit, fee=fee, smallPieces=smallPieces)
        product.save()

        # Fügt dem Artikel die ausgewählten Kategorien hinzu
        product.categories.add(*categories_objs)

        # Fügt optional Bilder hinzu
        if image:
            product.image = image
            product.images.append(image.name)
        if image2:
            product.image2 = image2
            product.images.append(image2.name)
        if image3:
            product.image3 = image3
            product.images.append(image3.name)
        if image4:
            product.image4 = image4
            product.images.append(image4.name)

        product.save()

        return Response({'status': 'Artikel erstellt'}, status=status.HTTP_201_CREATED)

    #DELETE-Request um ein Artikel mit der gegebenen ID zu löschen.
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    #PUT-Request um ein Artikel zu bearbeiten.
    def put(self, request):
        product_id = request.data.get('id')
        product = Product.objects.get(id=product_id)
        product.name = request.data['name']
        product.slug = slugify(product.name, allow_unicode=True)
        product.description = request.data['description']
        product.quantity = request.data['quantity']
        product.available = request.data['available']
        categories = request.data['categories']
        product.dimension = request.data['dimension']
        product.weight = request.data['weight']
        product.smallPieces = request.data['smallPieces']
        product.deposit = request.data['deposit']
        product.fee = request.data['fee']
        noImageChange = request.data.get('noImageChange')

        # Konvertiere die Kategorien-IDs in eine Liste von Ganzzahlen
        categories = [int(cat_id) for cat_id in categories.split(',')]

        # Holt die Kategorien mit den gegebenen IDs aus der Datenbank
        categories_objs = Category.objects.filter(id__in=categories)

        product.categories.set(categories_objs)

        if product.smallPieces == 'true':
            product.smallPieces = True
        else :
            product.smallPieces = False


        # Fügt optional Bilder hinzu oder entfernt vorhandene Bilder
        if request.data.get('image') is not None:
            product.images = []
            product.image = request.data['image']
            product.images.append(request.data['image'].name)
        if request.data.get('image2') is not None:
            product.image2 = request.data['image2']
            product.images.append(request.data['image2'].name)
        else:
            if not noImageChange:
                product.image2 = None
        if request.data.get('image3') is not None:
            product.image3 = request.data['image3']
            product.images.append(request.data['image3'].name)
        else:
            if not noImageChange:
                product.image3 = None
        if request.data.get('image4') is not None:
            product.image4 = request.data['image4']
            product.images.append(request.data['image4'].name)
        else:
            if not noImageChange:
                product.image4 = None
                
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


