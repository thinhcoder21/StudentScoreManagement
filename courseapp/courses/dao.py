from .models import User

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