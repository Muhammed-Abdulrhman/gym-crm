from django.contrib import admin
from django.urls import path, include
from the_app import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start, name='start'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category/', views.category_view, name='category'),
    path('customers/', views.customer_view, name='customers'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
    path('customer_progress/<int:customer_id>/', views.progress_view, name='customer_progress'),
    path('delete_progress/<int:progress_id>/', views.delete_progress, name='delete_progress'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)