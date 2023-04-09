from django.db.models import Q
from django.http import Http404
from django.views.decorators.http import require_http_methods

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Category, Wishlist
from .serializers import ProductSerializer, CategorySerializer, WishlistSerializer

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

class GetWishlist(APIView):
    def get(self, request, client_id, format=None):
        try: 
            wishlist = Wishlist.objects.get(client_id=client_id)
            response_data = wishlist.qr_code_text
            return Response(response_data, status=status.HTTP_200_OK)
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
      

      
    
    