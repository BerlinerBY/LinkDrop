from django.urls import path
from . import views

urlpatterns = [
    path('collections/create/', views.create_collection, name='create_collection'),
    path('collections/read_all/', views.read_collections, name='read_collections'),
    path('collections/read/<int:collection_id>', views.read_collection, name='read_collection'),
    path('collections/delete/<int:collection_id>', views.delete_collection, name='delete_collection'),
    path('collections/update/<int:collection_id>', views.update_collection, name='update_collection'),
    path('links/create/', views.create_link, name='create_link'),
    path('links/read_all/', views.read_links, name='read_links'),
    path('links/read/<int:link_id>', views.read_link, name='read_link'),
    path('links/delete/<int:link_id>', views.delete_link, name='delete_link'),
    path('links/update/<int:link_id>', views.update_link, name='update_link'),
    path('links/by_collection/<int:collection_id>', views.read_link_by_collection, name='links_by_collection')
]
