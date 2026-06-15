from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('post/<slug:slug>/', views.post_detail, name='post_detail'),

    path('author/<str:username>/', views.author_profile, name='author_profile'),

    path('save/<slug:slug>/', views.save_post, name='save_post'),

    path('saved-posts/', views.saved_posts, name='saved_posts'),

    path('remove-saved/<slug:slug>/', views.remove_saved_post, name='remove_saved_post'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),

    path('like/<slug:slug>/', views.like_post,name='like_post'),

    path('create-post/', views.create_post, name='create_post'),

    path('edit-post/<slug:slug>/', views.edit_post, name='edit_post'),

    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),

    path('profile/', views.profile, name='profile'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('request-author/', views.request_author, name='request_author'),

]