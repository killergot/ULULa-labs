from datetime import datetime, timedelta
from typing import Optional
import logging

from sqlalchemy import select

from uuid import UUID
from app.database.models.auth import User, Pending2FASession, TwoFactorCode
from app.database.models.groups import Group
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class TwoFactorRepository(TemplateRepository):
    async def check_code(self, code: str, user_id: int):
        # Проверка кода
        data = select(TwoFactorCode).filter(
            TwoFactorCode.user_id == user_id,
            TwoFactorCode.code == code,
            TwoFactorCode.expires_at >= datetime.utcnow()
        )
        valid_code = await self.db.execute(data)
        return valid_code.scalars().first()

    async def check_session(self, session_token):
        data = select(Pending2FASession).filter(
            Pending2FASession.session_token == session_token,
            Pending2FASession.expires_at >= datetime.utcnow()
        )
        valid_code = await self.db.execute(data)
        return valid_code.scalars().first()

    async def create(self, code: str,user_id: int,session_token: str):
        pending_session = Pending2FASession(
            session_token=session_token,
            user_id=user_id,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        self.db.add(pending_session)

        two_factor_code = TwoFactorCode(
            user_id=user_id,
            code=code,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )
        self.db.add(two_factor_code)

        await self.db.commit()
        return pending_session

    async def delete(self, session: Pending2FASession, code: TwoFactorCode):
        await self.db.delete(session)
        await self.db.delete(code)
        await self.db.commit()


