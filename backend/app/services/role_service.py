USER_ROLE: int = 0 # anyone
TEACHER_ROLE: int = 1 # 2^0
STUDENT_ROLE: int = 2 # 2^1
ADMIN_ROLE: int = 4   # 2^2

class RoleService:
    @staticmethod
    def is_admin(user) -> bool:
        return user.role & ADMIN_ROLE

    @staticmethod
    def is_teacher(user) -> bool:
        return user.role & TEACHER_ROLE

    @staticmethod
    def is_student(user) -> bool:
        return user.role & STUDENT_ROLE