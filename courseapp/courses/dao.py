from django.db.models import Count

from .models import User, Post, Account, ForumQuestion, ForumReponse, ForumAnswer


def load_users(params={}):
    query = User.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(username__icontains=keyword)

    return query


def load_account(params={}):
    query = Account.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(phone_number__icontains=keyword)

    role_id = params.get("role_id")
    if role_id:
        query = query.filter(role_id=role_id)

    return query


def load_posts(params={}):
    query = Post.objects.filter(active=True)

    keyword = params.get("keyword")
    if keyword:
        query = query.filter(post_content__icontains=keyword)

    return query

def get_answer_by_question_id(question_id):
    query = ForumAnswer.objects.filter(forum_question_id=question_id).values('Forum_question_id', 'answer')

    return query