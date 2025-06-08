from sqladmin import Admin, ModelView
from app.database import User
from app.database.models.auth import UserSession
from app.database.models.group_files import GroupFile
from app.database.models.students import Student
from app.database.models.subjects import Subject
from app.database.models.tasks import Task
from app.database.models.teachers import Teacher
from app.database import TwoFactorCode


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

class FilesAdmin(ModelView, model=GroupFile):
    column_list = [GroupFile.id,
                   GroupFile.filename,
                   'group.group_number',
                   'subject.name']

class SessionAdmin(ModelView, model=UserSession):
    column_list = ['user.id',
                   'user.email',
                   UserSession.token]

class TwoFa(ModelView, model = TwoFactorCode):
    column_list = [TwoFactorCode.code,
                    'user.email']



# Функция для инициализации админки
def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(SubjectAdmin)
    admin.add_view(TaskAdmin)
    admin.add_view(FilesAdmin)
    admin.add_view(SessionAdmin)
    admin.add_view(TwoFa)