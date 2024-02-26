from .models import User,Role,Account,Post,PostForum,ForumQuestion,ForumReponse,ForumAnswer,Teacher,Student,Class
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk',read_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','first_name','last_name','email']

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk',read_only=True)

    class Meta:
        model = User
        fields = ['id','password','first_name','last_name','email']

    def update(self,instance,validated_data):
        password = validated_data.pop('password',None)
        if password:
            instance.set_passwor(password)
        return super().update(instance,validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password','email','avatar']
        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = UserSerializer()
    avatar = serializers.SerializerMethodField(source='avatar')

    @staticmethod
    def get_avatar(account):
        if account.avatar:
            return account.avatar.name

    class Meta:
        model = Account
        fields = ['id','user','role','avatar']

class CreatePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Post
        fields = ['id','post_content','account']

class UpdatePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'post_content', 'comment_lock']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CreateAccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Account
        fields = ['id','user','role']

class UpdateAccountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Account
        fields = ['id','user','role']

class CreatePostForumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = PostForum
        fields = ['id', 'post_forum_title', 'start_time', 'end_time', 'post']

class UpdatePostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = PostForum
        fields = ['id', 'post_forum_title', 'start_time', 'end_time', 'is_closed']

class PostForPostForumSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Post
        fields = '__all__'

class PostForumSeriliazer(serializers.ModelSerializer):
    post = PostForPostForumSerializer()

    class Meta:
        model = PostForum
        fields = '__all__'

class CreateForumQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ForumQuestion
        fields = ['id','is_required','question_content','post_forum']

class UpdateForumQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ForumQuestion
        fields = ['id','is_required','question_content','post_forum']

class ForumQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumQuestion
        fields = '__all__'

class CreateForumReponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ForumReponse
        fields = ['id','account','post_forum']

class ForumReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumReponse
        fields = '__all__'

class CreateForumAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ForumAnswer
        fields = ['id','answer','forum_question','forum_response']

class UpdateForumAnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = ForumAnswer
        fields = ['id','answer']

class ForumAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumAnswer
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = '__all__'

class CreateClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Class
        fields = ['id','account','name']

class UpdateClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Class
        fields = ['id','name','account']