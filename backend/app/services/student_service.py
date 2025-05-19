from uuid import UUID
from fastapi import  HTTPException, status

from app.database.models.subjects import student_subjects
from app.repositoryes.student_repository import Repository
from app.repositoryes.group_repository import Repository as GroupRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositoryes.user_repository import UserRepository
from app.shemas.auth import UserOut
from app.shemas.students import StudentBase, StudentOut, StudentIn, Achievement, StudentUpdateIn
from app.utils.hash import get_hash
from app.database import Student
from app.repositoryes.subject_repository import Repository as SubjectRepository



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
        self.group_repo = GroupRepository(db)
        self.user_repo = UserRepository(db)
        self.subject_repo =SubjectRepository(db)

    async def _get(self, id) -> Student:
        student = await self.repo.get(id)
        if not student:
            raise HTTPException(status_code=404,
                                detail="Student not found")
        return student

    async def _get_group(self, number):
        group = await self.group_repo.get_by_number(number)
        if not group:
            raise HTTPException(status_code=404,
                                detail="Group not found")
        return group

    async def get(self, id):
        student = await self._get(id)
        return StudentOut(group_number = student.group.group_number,
                          full_name=student.full_name,
                          nickname=student.nickname,
                          student_id=student.id,
                          email=student.user.email,
                          achievements=[Achievement.model_validate(a) for a in student.achievements], # Почему тут ошибка
                          telegram=student.telegram,
                          avatar_url=student.avatar_url)


    async def create_student(self, student: StudentIn, id: int):#создаём нового студента
        print ("hello1")
        if await self.repo.get(id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Student already exist')
        group = await self._get_group(student.group_number)
        print("hello1")
        new_student = await self.repo.create(id,group.group_id,student.full_name)
        print("hello1")
        return StudentOut(group_number=student.group_number,
                          full_name=student.full_name,
                          student_id=new_student.id)

    async def update(self, new_student: StudentUpdateIn, id: int):
        student = await self._get(id)
        group = None
        if new_student.group_number is not None:
            group = await self.group_repo.get_by_number(new_student.group_number)
            if not group:
                raise HTTPException(status_code=404,
                                    detail="Wrong group number")
        user = await self.user_repo.get_by_email(new_student.email)
        if user and user.email != student.user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Email already busy')
        new_student = await self.repo.update(student = student,
                                             group_id = group.group_id if group else None,
                                             full_name=new_student.full_name,
                                             telegram=new_student.telegram,
                                             avatar = new_student.avatar_url,
                                             nickname=new_student.nickname,
                                             email=new_student.email) #  Это поменять на EmailStr
        return StudentOut(group_number = new_student.group.group_number,
                          full_name=new_student.full_name,
                          nickname=new_student.nickname,
                          student_id=new_student.id,
                          email=new_student.user.email,
                          achievements=[Achievement.model_validate(a) for a in new_student.achievements], # Почему тут ошибка
                          telegram=new_student.telegram,
                          avatar_url=new_student.avatar_url)



    async def delete_student(self, student_id: int):  # удаляем студента
        # проверка, что студент существует
        await self._get(student_id)
        #Попытка удаления
        await self.repo.delete(student_id)


    async def add_subject(self, subject_id: int,user_id: int ):
        subject = await self.subject_repo.get(subject_id)
        if not subject:
            raise HTTPException(status_code=404,
                                detail="Subject not found")
        student = await self._get(user_id)
        student = await self.repo.add_subject(student,subject)
        return student

    async def get_subjects(self, user_id: int ):
        student = await self._get(user_id)
        return student.subjects

    async def delete_subject(self, subject_id: int, user_id: int ):
        subject = await self.subject_repo.get(subject_id)
        if not subject:
            raise HTTPException(status_code=404,
                                detail="Subject not found")
        student = await self._get(user_id)
        if subject in student.subjects:
            if not await self.repo.delete_subject(student,subject):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        else:
            raise HTTPException(status_code=404,
                                detail="Student have not subject {}".format(subject.name))



    async def get_group(self, student_id: int) -> int:  # Возвращаем id группы по id студента
        student = await self._get(student_id)
        return student.group_id


    async def update_group(self, student_id, group_id): #обновляем номер группы
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Student not found")
        student = await self.repo.update(student_id, group_id)


    async def get_all(self):
        students = await self.repo.get_all()
        return students


    async def get_by_group(self, id: int):
        students = await self.repo.get_by_group(id)
        result = []

        for student in students:
            temp = StudentOut(
                student_id=student.id,
                email=student.user.email,
                group_number=student.group.group_number,
                full_name=student.full_name,
                telegram=student.telegram,
            )
            result.append(temp)

        return result