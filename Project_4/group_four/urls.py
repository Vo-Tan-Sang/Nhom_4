from urllib.parse import urlparse
from django.urls import path, re_path
from group_four import views
from .views import UpdatePost
# Template url
urlpatterns = [
    path("", views.blogs, name="blog"),
    path("post/",views.view_blog,name ="post"),
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    re_path("add_blogs/", views.add_blogs, name="add_blogs"),
    re_path("draft/", views.ViewDraft, name="draft"),
    path("edit_blog/<str:slug>/", UpdatePost.as_view(), name="edit_blog"),
    path("delete_blog_post/<int:post_id>/",views.Delete_Blog_Post, name="delete_blog_post"),  
    path("view/<str:slug>/", views.view_blog, name="view"),
    path('blog/<str:slug>/', views.blogs_comments, name='comment_blogs'),
    path("profile/", views.Profile, name="profile"),
    path("user_profile/<int:myid>/", views.user_profile, name="user_profile"),
    path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("push/<str:slug>/",views.push_draft,name = "push"),
    path("search/", views.search, name="search"),
    path("delete_comment/<int:comment_id>/",views.Delete_comment, name="delete_comment"),  
]
