from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from process_navigator.extensions.database import Base
from typing import List


@dataclass
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True, init=False
    )  # init prevents it from being passed in the constructor
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    entities: Mapped[List["Entity"]] = relationship(
        "Entity", back_populates="user", init=False
    )

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
