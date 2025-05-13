from sqladmin import Admin, ModelView
from app.database import User
from app.database.models.students import Student
from app.database.models.tasks import Task


# Определяем админ-представление
class UserAdmin(ModelView, model=User):
    column_list = [User.id,User.role, User.email]

class StudentAdmin(ModelView, model=Student):
    column_list = [Student.id,Student.full_name, Student.telegram, Student.group]

class TaskAdmin(ModelView, model=Task):
    column_list = [Task.task_id,
                   Task.user_id,
                   Task.description,
                   Task.deadline,
                   Task.task_flag
                   ]

# Функция для инициализации админки
def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(StudentAdmin)
    admin.add_view(TaskAdmin)