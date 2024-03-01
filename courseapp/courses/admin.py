from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse

from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from .models import PostForum,ForumQuestion,User,Role,Account,Post,ForumAnswer,ForumReponse,Class,Score,Course

class RoleAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username']
    search_fields = ['username']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'role', 'user']
    search_fields = ['email']
    list_filter = ['role_id']
    readonly_fields = ['show_avatar']

    @staticmethod
    def show_avatar(account):
        if account:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=account.avatar.name)
            )

class PostForumInLineAdmin(admin.TabularInline):
    model = PostForum

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_content', 'comment_lock', 'account']
    search_fields = ['post_content', 'account']
    list_filter = ['comment_lock']
    inlines = [PostForumInLineAdmin]

class ForumQuestionInLineAdmin(admin.TabularInline):
    model = ForumQuestion

class PostForumAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_forum_title', 'start_time', 'end_time', 'is_closed', 'post']
    search_fields = ['post_forum_title']
    inlines = [ForumQuestionInLineAdmin]

class ForumAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'forum_question', 'forum_response']

class ForumResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'post_forum']

class ForumQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_content', 'is_required', 'post_forum']

class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Lưu tất cả các thay đổi liên quan vào cơ sở dữ liệu trước khi thêm các tài khoản vào trường account.
        # Lấy thể hiện của Class sau khi đã được lưu vào cơ sở dữ liệu
        instance = form.instance

        # Lưu tất cả các thay đổi liên quan vào cơ sở dữ liệu
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)

        # Lưu các tài khoản vào trường account của Class
        account_data = form.cleaned_data.get('account', [])
        instance.account.set(account_data)
class ScoreAdmin(admin.ModelAdmin):
    pass
class CourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course,CourseAdmin)
admin.site.register(Score,ScoreAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostForum, PostForumAdmin)
admin.site.register(ForumQuestion, ForumQuestionAdmin)
admin.site.register(ForumReponse, ForumResponseAdmin)
admin.site.register(ForumAnswer, ForumAnswerAdmin)
