from django.urls import path

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('product/<str:id>/availability/', views.ProductAvailability.as_view()), 
    path('product/', views.ProductManagement.as_view()),
    path('product/<str:id>/', views.ProductManagement.as_view()), 
    path('products/', views.Products.as_view()), 
    path('products/search/', views.search), 
    path('products/<str:category_slug>/<str:product_slug>/', views.ProductDetail.as_view()), 
    path('products/<str:category_slug>/', views.CategoryDetail.as_view()), 
    path('categories/', views.GetCategories.as_view()),
    path('categorieslight', views.GetCategoriesLight.as_view()),
    path('category/', views.CategoryManagement.as_view()), 
    path('category/<str:id>/', views.CategoryManagement.as_view()), 
    path('wishlist/', views.CreateWishlist.as_view()), 
    path('wishlist/<str:client_id>/', views.GetWishlist.as_view()), 
    path('wishlists/', views.Wishlists.as_view()),
]