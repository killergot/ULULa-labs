from uuid import UUID
from fastapi import  HTTPException, status
from app.repositoryes.teacher_repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.students import StudentBase
from app.utils.hash import get_hash
from app.database import Student



class TeacherService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)

    async def create_teacher(self, teacher):#создаём нового студента
        #проверка, что студент ещё не существует
        if await self.repo.get_by_id(teacher['teacher_id']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Teacher already exist')
        #Проверка, существует ли группа
        #Если нет - создание группы
     #Мб стоит объединить создание и обновление всё же???
        #создание студента
        new_teacher = await self.repo.create(teacher['teacher_id'], teacher['FIO'])

        return new_teacher

'''
    async def delete_student(self, student_id: int):  # удаляем студента
        # проверка, что студент существует
        if not await self.repo.get_by_id(student_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Student is not exist')
        #Попытка удаления
        await self.repo.delete(student_id)


    async def get_group(self, student_id: int) -> int:  # Возвращаем id группы по id студента
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Student not found")
        return student.group_id


    async def update_group(self, student_id, group_id): #обновляем номер группы
        student = await self.repo.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Student not found")
        student = await self.repo.update(student_id, group_id)


    async def get_all(self):
        students = await self.repo.get_all()
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Students not found")

        return students


    async def get_by_group(self, id: int):
        students = await self.repo.get_by_group(id)
        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Groups not found")
        print(students)
        return students
'''