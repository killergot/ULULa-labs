from .psql import engine,Base
from .models.auth import TwoFactorCode, UserSession,User
from .models.students import Student
from .models.schedule import Schedule
from .models.tasks import Task

import asyncio