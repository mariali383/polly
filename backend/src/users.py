from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from ..db import Base
import datetime
from datetime import timezone


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now(timezone.utc))

