from typing import List

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from process_navigator.extensions import Base
from process_navigator.shared_data.enums import DataTypes


class AnalysisMethod(Base):
    __tablename__ = "analysis_method"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    file_name: Mapped[str] = mapped_column(nullable=False)

    analysis_method_parts: Mapped[List["AnalysisMethodPart"]] = relationship(
        back_populates="analysis_method",
        init=False,
        cascade="all, delete",
    )

    def __repr__(self):
        return f"Analysis Method {self.name}"


class AnalysisMethodPart(Base):
    __tablename__ = "analysis_method_part"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    analysis_method_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_method.id"), nullable=False
    )
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.id"), nullable=False)
    data_type: Mapped[str] = mapped_column(nullable=False)

    analysis_method: Mapped["AnalysisMethod"] = relationship(
        back_populates="analysis_method_parts"
    )

    __table_args__ = (
        CheckConstraint(
            data_type.in_([enum_data_type.value for enum_data_type in DataTypes]),
        ),
    )

    def __repr__(self):
        return f"Analysis Method Part {self.name}"
