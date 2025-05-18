from fastapi import  HTTPException, status
from typing import Optional

from app.repositoryes.teacher_repository import Repository
from app.repositoryes.teacher_schedule_repository import Repository as TeacherScheduleRepository
from app.repositoryes.teacher_subject_repository import Repository as TeacherSubjectRepository
from app.repositoryes.subject_repository import Repository as SubjectRepository
from app.repositoryes.student_repository import Repository as StudentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositoryes.achievements_repository import AchivementRepository
from app.database import TeacherSubject
from app.utils.get_schedule import get_teacher_schedule
from app.database.models.achievent import Achievement

class TeacherService:
    def __init__(self, db: AsyncSession):
        self.repo = Repository(db)
        self.schedule_repo = TeacherScheduleRepository(db)
        self.teacher_subject_repo = TeacherSubjectRepository(db)
        self.subject_repo = SubjectRepository(db)
        self.achieve_repo = AchivementRepository(db)
        self.student_repo = StudentRepository(db)

    async def create_teacher(self, teacher):
        if await self.repo.get_by_id(teacher['id']):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Teacher already exist')
        new_teacher = await self.repo.create(teacher['id'], teacher['FIO'])
        #подгрузка расписания для препода
        schedule = await  get_teacher_schedule([{'id': teacher['id'], 'FIO': teacher['FIO']}])
        #получаем из get_schedule расписание
        #закидываем его в таблицу
        #print ("schedule is", schedule[0])
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
        try:
            teacher = await self.repo.get_by_FIO(FIO)
            id = teacher.id
            return id
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Teacher not found')


    async def delete(self, FIO: str)->bool:
        id = await self.get_teacher_id(FIO)
        if not id:
            raise HTTPException(status_code=404,
                                detail="Teacher not found")
        return await self.repo.delete(id)

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
        if subject:
            id = subject.id
            return id
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Subject not found"
                )



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



    # управление ачивками
    async def get_achievement(self, id):
        achievement = await self.achieve_repo.get(id)
        if not achievement:
            raise HTTPException(status_code=404,
                            detail="Achievement not found")
        return achievement

    async def create_achievement(self, name: str, description: str, amount: int):
        # создать новую ачивку
        return await self.achieve_repo.create(name, description, amount)



    async def delete_achievement(self, id: int)->bool:
        # проверка существования
        await self.get_achievement(id)
        # удалить ачивку
        return await self.achieve_repo.delete(id)


    async def update_achievement(self, id: int, name: Optional[str] = None, description: Optional[str] = None, amount: Optional[int] = None):
        achievement = await self.get_achievement(id)
        return await self.achieve_repo.update(achievement, name, description, amount)


    async def give_achievement(self, student_id: int, achievement_id: int)->Achievement:
        student = await self.student_repo.get(student_id)
        achievement = await self.get_achievement(achievement_id)
        return await self.achieve_repo.give(achievement, student)

    async def revoke_achievement(self, student_id: int, achievement_id: int) -> bool:
        student = await self.student_repo.get(student_id)
        achievement = await self.get_achievement(achievement_id)
        return await self.achieve_repo.revoke(achievement, student)

    async def get_all_achievements(self)->list[Achievement]:
        return await self.achieve_repo.get_all()