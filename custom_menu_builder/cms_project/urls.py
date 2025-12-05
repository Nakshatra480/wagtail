"""cms_project URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from menu_builder import views as menu_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # Authentication URLs
    path('login/', menu_views.login_view, name='login'),
    path('signup/', menu_views.signup_view, name='signup'),
    path('logout/', menu_views.logout_view, name='logout'),
    
    # Menu management
    path('menus/create/', menu_views.menu_create_view, name='menu_create'),
    path('menus/<int:menu_id>/edit/', menu_views.menu_edit_view, name='menu_edit'),
    path('menus/<int:menu_id>/preview/', menu_views.menu_preview_view, name='menu_preview'),
    path('menus/<int:menu_id>/reorder/', menu_views.menu_reorder_view, name='menu_reorder'),
    path('menus/<int:menu_id>/delete/', menu_views.menu_delete_view, name='menu_delete'),
    
    # Menu item management
    path('menus/<int:menu_id>/items/add/', menu_views.menu_item_add_view, name='menu_item_add'),
    path('menus/<int:menu_id>/items/<int:item_id>/edit/', menu_views.menu_item_edit_view, name='menu_item_edit'),
    path('menus/<int:menu_id>/items/<int:item_id>/delete/', menu_views.menu_item_delete_view, name='menu_item_delete'),
    
    path('menus/', menu_views.menu_list_view, name='menu_list'),
    path('', menu_views.menu_list_view, name='home'),
    
    # Wagtail pages
    path('pages/', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

