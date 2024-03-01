from django.urls import path, include
from . import views
from rest_framework import routers
from .views import (HomeView, UserRegistrationView ,UserLoginView,ScoreViewSet,
                    teacher_dashboard,CourseListCreateView)

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
router.register('scores', views.ScoreViewSet, basename='scores')

urlpatterns = [
    path('',include(router.urls)),
    path('home/', HomeView.as_view(),name='home'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('manage-score/', teacher_dashboard, name='manage_score'),
    path('scores/search_students/', ScoreViewSet.as_view({'get': 'search_students'}), name='search_students'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
]