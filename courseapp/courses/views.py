from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from .perms import IsAdmin, PostOwner , CanManageScorePermission
from drf_yasg.openapi import Response
from .models import User,Role,Post,PostForum,ForumQuestion,ForumAnswer,ForumReponse,Account,Score,Teacher,Student,Class

from rest_framework.decorators import action, permission_classes
from rest_framework import viewsets, generics, status , parsers, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from . import serializers
from . import paginators
from . import perms

from .serializers import (RoleSerializer,UserSerializer,PostSerializer,AccountSerializer,CreateAccountSerializer,
                          CreateUserSerializer,CreatePostSerializer,CreateForumAnswerSerializer,CreateForumQuestionSerializer,
                          CreatePostForumSerializer,CreateForumReponseSerializer,UpdateUserSerializer,UpdatePostSerializer,
                          UpdateAccountSerializer,PostForumSeriliazer,ForumQuestionSerializer,
                          UpdateForumQuestionSerializer,ForumReponseSerializer,
                          ForumAnswerSerializer,UpdateForumAnswerSerializer,UserRegisterSerializer,
                          TeacherSerializer, StudentSerializer, ClassSerializer,
                          CreateClassSerializer,UpdateClassSerializer)
# Create your views here.

class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_queryset(self):
        queries = self.queryset
        name = self.request.query_params.get('name')

        if name:
            names = name.split()
            for name in names:
                queries = queries.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        return queries

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        if self.action in ['update','partial_update']:
            return UpdateUserSerializer
        return self.serializer_class

    @action(methods=['get'],url_name='current-user', detail=False)
    def current_user(self,request):
        return Response(serializers.UserSerializer(request.user).data,status=status.HTTP_200_OK)

    @action(methods=['get'],url_name='account', detail=True)
    def get_account_by_userid(self,request,pk):
        try:
            user = self.get_object()
            account = user.account
            return Response(AccountSerializer(account,context={'request':request}).data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Not found !!!'},status=status.HTTP_404_NOT_FOUND)

class RoleViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PostViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView,generics.CreateAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [PostOwner()]
        if self.action in ['create_post_forum']:
            return [IsAdmin()]
        else:
            return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        if self.action in ['update', 'partial_update']:
            return UpdatePostSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=False, url_path='create_post_forum')
    def create_post_forum(self,request):
        try:
            with transaction.atomic():
                account_id = request.data.get('account_id')
                post_content = request.data.get('post_content')

                post = Post.objects.create(post_content=post_content, account_id=account_id)

                post_forum_title = request.data.get('post_forum_title')
                start_time = request.data.get('start_time')
                end_time = request.data.get('end_time')
                post_forum = PostForum.objects.create(post=post, post_forum_title=post_forum_title,
                                                        start_time=start_time,
                                                        end_time=end_time)

                forum_question_list = request.data.get('forum_question_list', [])
                for question in forum_question_list:
                    question_content = question.get('question_content')
                    is_required = question.get('is_required')
                    forum_question = ForumQuestion.objects.create(post_forum=post_forum,
                                                                  question_content = question_content,
                                                                  is_required = is_required,
                                                                  )
                return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            error_message = str(e)
            return Response({error_message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['POST'], detail=False, url_path='answer_post_forum')
    def answer_post_forum(self,request):
        try:
            with transaction.atomic():
                account_id = request.data.get('account_id')
                post_forum = request.data.get('post_survey')
                forum_response = ForumReponse.objects.create(post_forum_id=post_forum,
                                                                account_id=account_id)
                forum_question_list = request.data.get('forum_question_list', [])

                for question in forum_question_list:
                    question_id = question.get('question')
                    answer_value = question.get('answer_value')
                    survey_answer = ForumAnswer.objects.create(answer_value=answer_value,
                                                                survey_question_id=question_id,
                                                                survey_response=forum_response)
                return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = str(e)
            return Response({error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AccountViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView,generics.CreateAPIView,generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = Account.objects.select_related('role','user').filter(active=True).all()
    serializer_class = AccountSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def create(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        if email:
            duplicate_email = Account.objects.filter(email=email).exists()
            if duplicate_email:
                return Response({'Email đã tồn tại !! Vui Lòng thử lại ' : email}, status=status.HTTP_400_BAD_REQUEST)

            user = self.request.data.get('user')
        if user:
            duplicate_user = Account.objects.filter(
                user=user).exists()
            if duplicate_user:
                return Response({'User đã tạo tài khoản! ': user},
                                    status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        email = self.request.data.get('email')
        if email:
            duplicate_email = Account.objects.filter(
                email=email).exists()
            if duplicate_email:
                return Response({'Email đã tồn tại! ': email},
                                status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action in ['list', 'update', 'partial_update', 'destroy', 'get_posts_by_account']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateAccountSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateAccountSerializer
        return self.serializer_class

class PostForumViewSet(viewsets.ViewSet,generics.ListAPIView,generics.RetrieveAPIView,generics.UpdateAPIView,generics.DestroyAPIView,generics.CreateAPIView):
    queryset = PostForum.objects.filter(active=True).all()
    serializer_class = PostForumSeriliazer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostForumSerializer
        if self.action in ['update', 'partial_update']:
            return UpdatePostSerializer
        return self.serializer_class

    @action(methods=['GET'], detail=True, url_path='forum_question')
    def get_forum_questions(self, request, pk):
        forum_questions = self.get_object().forumquestion_set.filter(active=True).all()
        return Response(ForumQuestionSerializer(forum_questions, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

class ForumQuestionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView,
                            generics.UpdateAPIView, generics.DestroyAPIView):
    queryset =  ForumQuestion.objects.filter(active=True).all()
    serializer_class = ForumQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateForumQuestionSerializer
        if self.action in ['update','partial_update']:
            return UpdateForumQuestionSerializer
        return self.serializer_class

class ForumResponseViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView,
                            generics.DestroyAPIView):
    queryset = ForumReponse.objects.filter(active=True).all()
    serializer_class = ForumReponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateForumReponseSerializer
        return self.serializer_class

class ForumAnswerViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView,
                          generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = ForumAnswer.objects.filter(active=True).all()
    serializer_class = ForumAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateForumAnswerSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateForumAnswerSerializer
        return self.serializer_class

class HomeView(View):
    template_name = "login_google/home.html"
    def get(self,request):
        current_user =  request.user
        return render(request, self.template_name, {'current_user': current_user})

@api_view(["POST"])
def user_register_view(request):
        if request.method == "POST":
            serializer = UserRegisterSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    template_name = 'registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Registration successful", status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

@user_passes_test(is_teacher, login_url='/login/')  # Redirect to the login page if not a teacher
def teacher_dashboard(request):
    # Logic for the teacher dashboard view
    return render(request, 'manage_score.html')

class UserLoginView(APIView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_authenticated :
                if is_teacher(request.user):
                    return redirect(reverse('manage_score'))
                else:
                    return redirect('home')
        else:
            return render(request, self.template_name, {'error': 'Invalid login credentials'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required
def list_course(request):
    student_score = Score.object.filter(student=request.user)

    return render(request, 'list_course.html', {'student_score': student_score})

class ManageScoreView(APIView):
    permission_classes = [CanManageScorePermission]

    def get(self, request):
        # Xử lý logic khi người dùng có quyền
        return Response({"message": "You have permission to manage grades."}, status=status.HTTP_200_OK)



class TeacherAPIView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ClassAPIView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.CreateAPIView,
                            generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateClassSerializer
        if self.action in ['update','partial_update']:
            return UpdateClassSerializer
        return self.serializer_class
