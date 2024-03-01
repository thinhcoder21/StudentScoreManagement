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


def search_students_by_name(teacher, student_name):
    if teacher.is_authenticated and teacher.groups.filter(name='Teacher').exists():
        # Nếu giáo viên có quyền thực hiện tìm kiếm, thực hiện truy vấn
        students = User.objects.filter(
            role__role_name='student',  # Đảm bảo chỉ lấy sinh viên
            course__in=teacher.course_set.all(),  # Lọc theo lớp học của giáo viên
            username__icontains=student_name  # Lọc theo họ tên của sinh viên
        )
        return students
    else:
        # Nếu không phải giáo viên, trả về danh sách trống
        return []