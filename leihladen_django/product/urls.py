from django.urls import path

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('product/<int:id>/availability/', views.ProductAvailability.as_view()), 
    path('product/', views.ProductManagement.as_view()),
    path('product/<int:id>/', views.ProductManagement.as_view()), 
    path('products/', views.Products.as_view()), 
    path('products/search/', views.search), 
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()), 
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()), 
    path('categories', views.GetCategories.as_view()), 
    path('wishlist/', views.CreateWishlist.as_view()), 
    path('wishlist/<str:client_id>/', views.GetWishlist.as_view()), 
    path('wishlists/', views.Wishlists.as_view()),
]