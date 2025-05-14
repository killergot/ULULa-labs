from sqladmin import Admin, ModelView
from app.database import User
from app.database.models.students import Student
from app.database.models.subjects import Subject
from app.database.models.tasks import Task
from app.database.models.teachers import Teacher


# Определяем админ-представление
class UserAdmin(ModelView, model=User):
    column_list = [User.id,User.role, User.email, User.is_active]

class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id,Student.full_name, Student.telegram, 'group.group_number']

class TaskAdmin(ModelView, model=Task):
    column_list = [Task.task_id,
                   Task.user_id,
                   Task.description,
                   Task.deadline,
                   Task.task_flag
                   ]

class TeacherAdmin(ModelView, model=Teacher):
    column_list = [Teacher.id,
                   Teacher.FIO]

class SubjectAdmin(ModelView, model=Subject):
    column_list = [Subject.id,
                   Subject.name]


# Функция для инициализации админки
def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(SubjectAdmin)
    admin.add_view(TaskAdmin)