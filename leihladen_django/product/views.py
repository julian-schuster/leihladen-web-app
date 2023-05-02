from django.db.models import Sum, Q
from django.http import Http404
from slugify import slugify
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Wishlist
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer

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
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(APIView):
    # API-Endpunkt, um ein bestimmtes Produkt abzurufen.
    def get_object(self, category_slug, product_slug):
        #Hilfsfunktion, um das Produkt anhand des Kategorie-Slugs und des Produkt-Slugs zu finden.
        try: 
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        # GET-Request, um ein Produkt anhand des Kategorie-Slugs und des Produkt-Slugs abzurufen.
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
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"products": []})

class GetCategories(APIView):
    #API-Endpunkt der alle Kategorien zurückgibt.
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
                'status': 'success', 
                'wishlist_id': wishlist.id, 
                'client_id': client_id
            }
            status_code = status.HTTP_201_CREATED
        else:
            # Wenn die Wishlist des Clients aktualisiert wurde
            response_data = {'status': 'Wishlist updated'}
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

    #POST-Request um ein Artikel hinzuzufügen
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        quantity = request.data.get('quantity')
        image = request.data.get('image')
        image2 = request.data.get('image2')
        image3 = request.data.get('image3')
        image4 = request.data.get('image4')
        category_id = request.data.get('category')

        # Holt die Kategorie mit der gegebenen ID aus der Datenbank
        category = Category.objects.get(id=category_id)
        
        slug = slugify(name, replacements=[['Ü', 'UE'], ['ü', 'ue'],['Ä', 'AE'], ['ä', 'ae'], ['Ö', 'OE'], ['ö', 'oe']])
    
        # Erstellt ein neues Artikel-Objekt mit den übergebenen Daten
        product = Product(name=name, slug=slug, description=description, quantity=quantity, category=category, available=quantity)
        product.save()

        # Fügt optional Bilder hinzu
        if image:
            product.image = image
        if image2:
            product.image2 = image2
        if image3:
            product.image3 = image3
        if image4:
            product.image4 = image4

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
        noImageChange = request.data.get('noImageChange')
        product.name = request.data['name']
        product.slug = slugify(product.name, replacements=[['Ü', 'UE'], ['ü', 'ue'],['Ä', 'AE'], ['ä', 'ae'], ['Ö', 'OE'], ['ö', 'oe']])
        product.description = request.data['description']
        product.quantity = request.data['quantity']
        product.available = request.data['available']
        category_id = request.data['category']
        category = Category.objects.get(id=category_id)
        product.category = category


        # Fügt optional Bilder hinzu oder entfernt vorhandene Bilder
        if request.data.get('image') is not None:
            product.image = request.data['image']
        if request.data.get('image2') is not None:
            product.image2 = request.data['image2']
        else:
            if not noImageChange:
                product.image2 = None
        if request.data.get('image3') is not None:
            product.image3 = request.data['image3']
        else:
            if not noImageChange:
                product.image3 = None
        if request.data.get('image4') is not None:
            product.image4 = request.data['image4']
        else:
            if not noImageChange:
                product.image4 = None

        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


