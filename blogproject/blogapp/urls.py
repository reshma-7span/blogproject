from django.urls import path
from .import views
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.signout, name='logout'),
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.create_blog, name='create_blog'),
    path('blog/<int:blog_id>/update/', views.update_blog, name='update_blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('search/', views.search_blog, name='search_blog'),
]