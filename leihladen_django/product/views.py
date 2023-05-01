from django.db.models import Sum, Q
from django.http import Http404
from django.utils.text import slugify
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Wishlist
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer

class Products(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        available_count = products.aggregate(total=Sum('available'))['total']
        total_count = products.aggregate(total=Sum('quantity'))['total']
        serializer = ProductSerializer(products, many=True)
        data = {'products': serializer.data, 'quantity': total_count, 'available_count': available_count}
        return Response(data, status=status.HTTP_200_OK)

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try: 
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetail(APIView):
       def get_object(self, category_slug):
        try: 
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
   
       def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class GetWishlist(APIView):
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
    def post(self, request):
        qr_code_text = request.data.get('qr_code_text')
        client_id = request.data.get('client_id')
        
        # Versuche, die Wishlist des Clients zu finden
        wishlist, created = Wishlist.objects.update_or_create(
            client_id=client_id,
            defaults={'qr_code_text': qr_code_text}
        )

        if created:
            # Wenn eine neue Wishlist erstellt wurde
            return Response({
                'status': 'success', 
                'wishlist_id': wishlist.id, 
                'client_id': client_id
            }, status=status.HTTP_201_CREATED)
        else:
            # Wenn die Wishlist des Clients aktualisiert wurde
            return Response({'status': 'Wishlist updated'}, status=status.HTTP_200_OK)
      
class Wishlists(APIView):
    def get(self, request, format=None):
        wishlists = Wishlist.objects.all()
        wishlist_count = wishlists.count()
        serializer = WishlistSerializer(wishlists, many=True)
        data = {'wishlists': serializer.data, 'count': wishlist_count}
        return Response(data, status=status.HTTP_200_OK)
    
class ProductAvailability(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id):
        product = Product.objects.get(id=id)
        value = request.data.get('value', None)
        if value is not None:
            # Berechne die neue Verfügbarkeit
            new_available = product.available + value
            
            # Überprüfe, ob die neue Verfügbarkeit gültig ist
            if new_available < 0:
                return Response({'error': 'Die Verfügbarkeit darf nicht unter 0 fallen.'}, status=status.HTTP_400_BAD_REQUEST)
            elif new_available > product.quantity:
                return Response({'error': 'Die Verfügbarkeit darf nicht größer als der aktuelle Bestand sein.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Wenn die neue Verfügbarkeit gültig ist, aktualisiere das Produkt
                product.available = new_available
                product.save()
                # Gib das aktualisierte Produkt zurück
                serialized_product = ProductSerializer(product).data
                return Response(serialized_product, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Fehler beim Aktualisieren der Verfügbarkeit'}, status=status.HTTP_400_BAD_REQUEST)
        
class ProductManagement(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        quantity = request.data.get('quantity')
        image = request.data.get('image')
        image2 = request.data.get('image2')
        image3 = request.data.get('image3')
        image4 = request.data.get('image4')
        category_id = request.data.get('category')

        category = Category.objects.get(id=category_id)
        slug = slugify(name)

        product = Product(name=name, slug=slug, description=description, quantity=quantity, category=category, available=quantity)
        product.save()

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

    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    permission_classes = [IsAuthenticated]
    def put(self, request):
        product_id = request.data.get('id')
        product = Product.objects.get(id=product_id)
        noImageChange = request.data.get('noImageChange')

        if request.data.get('name') is not None:
            product.name = request.data['name']
        if request.data.get('description') is not None:
            product.description = request.data['description']
        if request.data.get('quantity') is not None:
            product.quantity = request.data['quantity']
        if request.data.get('available') is not None:
            product.available = request.data['available']
        if request.data.get('category') is not None:
            category_id = request.data['category']
            category = Category.objects.get(id=category_id)
            product.category = category
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

