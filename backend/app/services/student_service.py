from uuid import UUID

from fastapi import  HTTPException, status

from app.repositoryes.student_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.students import StudentBase
from app.utils.hash import get_hash
from app.database import Student



# Что хотим уметь для сущности студента?
# 1.1 - получать номер группы для конкретного студента (вход - имя студента, выход - номер группы )(только для авторизованных)
# 1.2 - получать номер группы для себя (вход - ничего, получаем id юзера через токен, выход - номер группы)

# 2 - добавлять/изменять номер группы (а вообще - и параметры в целом) для конкретного студента (вход - id, номер группы, выход - успех/неуспех, только для админа??)
# 2.2 добавлять/изменять номер группы (а вообще - и параметры в целом) для себя (вход - новый номер группы, получаем id юзера через токен, выход - успех/неуспех)

# 3 - получать список всех студентов (вход - ничего, выход - список из (имя_студента, номер группы), для авторизованного пользователя)

# 4.1 - получать список студентов по конкретной группе (вход - номер группы, выход - список из студентов)
# 4.2 - получать список студентов своей группы (вход - получаем id юзера через токен, выход - список из студентов)

# 5 - создавать студента (себя) (вход - получаем id usera по токену + номер группы, выход - успех/неуспех) - должно ли подтверждаться админом?

# 6.1 - удалять студента (себя) (вход - получаем id usera по токену, выход - успех/неуспех)
# 6.2 - удалять конкретного студента (вход - id юзера, выход - успех/неуспех) - только для админа




class StudentService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)

    async def _create_student(self, student: StudentBase):#создаём нового студента
        #проверка, что студент ещё не существует
        if await self.repo.get_group(student.group_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Student already exist')
     #Мб стоит объединить создание и обновление всё же???
        #создание студента
        await self.repo.create(student.student_id, student.group_id)

    """
    
    async def _get_group(self, user_id: int) -> int: #Возвращаем id группы по id студента
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def _set_group(self, student: int) -> int: #Устанавливаем параметры (пока только номер группы)
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def _get_students_by_grouo() -> int: #Выводим список id студентов по группе

    async def _get_all() -> int:  # Выводим список всех студентов

"""