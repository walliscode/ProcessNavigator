from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from process_navigator.extensions import db


class User(db.Model):
    id: Mapped[int] = mapped_column(
        primary_key=True, init=False
    )  # init prevents it from being passed in the constructor as the database will handle this
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

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
