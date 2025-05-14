from uuid import UUID
from fastapi import  HTTPException, status

from app.repositoryes.teacher_repository import Repository
from app.repositoryes.teacher_schedule_repository import Repository as TeacherScheduleRepository
from app.repositoryes.teacher_subject_repository import Repository as TeacherSubjectRepository
from app.repositoryes.subject_repository import Repository as SubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.shemas.students import StudentBase
from app.utils.hash import get_hash
from app.database import Student
from app.database import TeacherSubject
from app.utils.get_schedule import get_teacher_schedule
from watchfiles import awatch


class TeacherService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.schedule_repo = TeacherScheduleRepository(db)
        self.teacher_subject_repo = TeacherSubjectRepository(db)
        self.subject_repo = SubjectRepository(db)

    async def create_teacher(self, teacher):
        if await self.repo.get_by_id(teacher['id']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Teacher already exist')
        new_teacher = await self.repo.create(teacher['id'], teacher['FIO'])
        #подгрузка расписания для препода
        schedule = await  get_teacher_schedule([{'id': teacher['id'], 'FIO': teacher['FIO']}])
        #получаем из get_schedule расписание
        #закидываем его в таблицу
        print ("schedule is", schedule[0])
        if schedule[0]!=[{}]:
            await self.schedule_repo.create_by_list(schedule)
        return new_teacher

    #получение расписания для конкретного преподавателя по ФИО
    async def get_schedule(self, id: int, week_number: int)->dict:
        # получить id
        full_schedule = await self.schedule_repo.get(id, week_number)
        result = {
                'monday': full_schedule.monday,
                'tuesday': full_schedule.tuesday,
                'wednesday': full_schedule.wednesday,
                'thursday': full_schedule.thursday,
                'friday': full_schedule.friday,
                'saturday': full_schedule.saturday,
                'sunday': full_schedule.sunday
            }
        return result


    async def get_teacher_id(self, FIO: str)->int:
        teacher = await self.repo.get_by_FIO(FIO)
        id = teacher.id
        return id

    async def get_schedule_by_FIO(self, FIO: str, week_number: int)->dict:
        # получить id
        id = await self.get_teacher_id(FIO)
        return await self.get_schedule(id, week_number)



    async def get_subjects(self, id: int)->list[str]:
        # получить id
        full_subjects = await self.teacher_subject_repo.get(id)
        subjects=[]
        for subject in full_subjects:
            name = await self.subject_repo.get(subject.subject_id)
            subjects.append(name.name)
        return subjects


    async def get_subjects_by_FIO(self, FIO: str)->list[str]:
        # получить id
        id = await self.get_teacher_id(FIO)
        return await self.get_subjects(id)

    async def get_subject_id(self, name: str)->int:
        subject = await self.subject_repo.get_by_name(name)
        id = subject.id
        return id



    async def add_subject(self, teacher_id: int, name: str)->TeacherSubject:
        # получить id

            subject_id = await self.get_subject_id(name)
            subj = await self.teacher_subject_repo.is_exist(teacher_id, subject_id)
            if not subj:
                return await self.teacher_subject_repo.create(teacher_id, subject_id)
            else:
                subj = await self.teacher_subject_repo.is_exist(teacher_id, subject_id)
                print(subj.teacher_id, subj.subject_id)
                raise HTTPException(
                status_code=400,
                detail=f"This subject already exist!"
                )

    async def delete_subject(self, teacher_id: int, name: str)->TeacherSubject:
        # получить id

            subject_id = await self.get_subject_id(name)
            subj = await self.teacher_subject_repo.is_exist(teacher_id, subject_id)
            if subj:
                return await self.teacher_subject_repo.delete(teacher_id, subject_id)
            else:
                subj = await self.teacher_subject_repo.is_exist(teacher_id, subject_id)
                print(subj.teacher_id, subj.subject_id)
                raise HTTPException(
                status_code=404,
                detail=f"Subject not found"
                )

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