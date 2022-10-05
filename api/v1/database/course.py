from sqlalchemy import Boolean, Column, ForeignKey, String, Text, select

from .base import Base, Crud


class CourseLevel:
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    ALL = [BEGINNER, INTERMEDIATE, ADVANCED]


class CourseCrud(Crud, Base):
    __tablename__ = "Courses"

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(256), nullable=False)
    # rating = Column(Float, nullable=False)
    # duration = Column(Integer, nullable=False)
    image = Column(Text)
    is_public = Column(Boolean, nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id"), nullable=False)

    @classmethod
    async def find_all(cls, search: str, levels: list[str], limit: int, offset: int):
        return await cls.fetch_all(
            select(cls)
                .where(cls.title.contains(search) & cls.level.in_(levels))
                .limit(limit).offset(offset)
        )
