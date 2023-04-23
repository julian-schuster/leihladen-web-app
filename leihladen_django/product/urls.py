from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()), #get
    path('product/<int:id>/availability/', views.ProductAvailability.as_view()), #put
    path('product/', views.ProductManagement.as_view()), #post
    path('product/<int:id>/', views.ProductManagement.as_view()), #delete
    path('products/', views.Products.as_view()), #get
    path('products/search/', views.search), #get
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()), #get
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()), #get
    path('wishlist/', views.CreateWishlist.as_view()), #post und put
    path('wishlist/<str:client_id>/', views.GetWishlist.as_view()), #get
    path('wishlists/', views.Wishlists.as_view()), #get
]