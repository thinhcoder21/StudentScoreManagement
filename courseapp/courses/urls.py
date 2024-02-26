from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from rest_framework import routers
from .views import (HomeView, user_register_view, user_logout, UserRegistrationView ,UserLoginView,
                    list_course,ManageScoreView,teacher_dashboard)

router = routers.DefaultRouter()
router.register('roles',views.RoleViewSet, basename= 'roles')
router.register('users',views.UserViewSet, basename= 'users')
router.register('posts',views.PostViewSet, basename= 'posts')
router.register('accounts',views. AccountViewSet, basename= 'accounts')
router.register('post_forums',views.PostForumViewSet, basename= 'post_forums')
router.register('forum_questions',views.ForumQuestionViewSet, basename= 'forum_questions')
router.register('forum_responses',views.ForumResponseViewSet, basename= 'forum_responses')
router.register('forum_answers',views.ForumAnswerViewSet, basename= 'forum_answers')
router.register('classes',views.ClassViewSet, basename= 'classes')

urlpatterns = [
    path('',include(router.urls)),

    path('home/', HomeView.as_view(),name='home'),
    path('home/logout/',LogoutView.as_view()),
    path('register/', user_register_view, name='register'),
    path('register2/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('list-course/', list_course, name='list_course'),
    path('manage-score/', teacher_dashboard, name='manage_score'),
]