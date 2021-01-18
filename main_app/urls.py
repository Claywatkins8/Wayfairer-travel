from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/show', views.post_show, name='post_show'),
    path('post/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete', views.post_delete, name='post_delete'),
    path('profile/<int:profile_id>/add_photo/',
         views.add_photo, name='add_photo'),
    path('profile/<int:photo_id>/delete',
         views.photo_delete, name='photo_delete'),
]
