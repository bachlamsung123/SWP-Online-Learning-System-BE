from sqlalchemy import Boolean, Column, Float, ForeignKey, String, Text, select
from sqlalchemy.sql.functions import func

from .base import AuthorRelatedCrud, Base, CourseRelatedCrud, Crud
from .user import UserCrud


class CategoryCrud(Crud, Base):
    __tablename__ = "Categories"

    name = Column(String(256), nullable=False)


class CourseLevel:
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    ALL = ( BEGINNER, INTERMEDIATE, ADVANCED )


class CourseCrud(AuthorRelatedCrud, CourseRelatedCrud, Base):
    __tablename__ = "Courses"

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(String(256), nullable=False)
    image = Column(Text)
    is_public = Column(Boolean, nullable=False)
    category_id = Column(String(36), ForeignKey("Categories.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_all(cls, search: str, levels: list[str], category_ids: list[str], user_ids: list[str], limit: int, offset: int):
        stmt = cls.select().where(cls.title.contains(search))
        if levels:
            stmt = stmt.where(cls.level.in_(levels))
        if category_ids:
            stmt = stmt.where(cls.category_id.in_(category_ids))
        if user_ids:
            stmt = stmt.where(cls.author_id.in_(user_ids))
        return await cls.fetch_all(
            stmt.order_by(cls.created_at.desc())
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_course_id(cls, obj) -> str:
        return obj.id

    @classmethod
    async def find_author_id(cls, obj) -> str:
        return obj.author_id


class EnrollmentCrud(Crud, Base):
    __tablename__ = "Enrollments"

    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.fetch_one(
            cls.select()
                .where(cls.user_id == user_id)
                .where(cls.course_id == course_id)
        )

    @classmethod
    async def exist_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.find_by_user_id_and_course_id(user_id, course_id) is not None

    @classmethod
    async def find_all_courses_by_user_id(cls, user_id: str, search: str, limit: int, offset: int):
        return await cls.fetch_all(
            CourseCrud.select()
                .join(cls)
                .where(cls.user_id == user_id)
                .where(CourseCrud.title.contains(search))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def find_all_users_by_course_id(cls, course_id: str, search:str, limit: int, offset: int):
        return await cls.fetch_all(
            UserCrud.select()
                .join(cls)
                .where(cls.course_id == course_id)
                .where(UserCrud.full_name.contains(search))
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)


class FeedbackCrud(Crud, Base):
    __tablename__ = "Feedbacks"

    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(String(36), ForeignKey("Courses.id", ondelete="CASCADE"), nullable=False)

    @classmethod
    async def find_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.fetch_one(
            cls.select()
                .where(cls.user_id == user_id)
                .where(cls.course_id == course_id)
        )

    @classmethod
    async def exist_by_user_id_and_course_id(cls, user_id: str, course_id: str):
        return await cls.find_by_user_id_and_course_id(user_id, course_id) is not None

    @classmethod
    async def find_all_by_course_id(cls, course_id: str, limit: int, offset: int):
        return await cls.fetch_all(
            cls.select()
                .where(cls.course_id == course_id)
                .limit(limit).offset(offset)
        )

    @classmethod
    async def count_by_course_id(cls, course_id: str):
        return await cls.count_by_attr(cls.course_id, course_id)

    @classmethod
    async def average_rating_by_course_id(cls, course_id: str):
        return await cls.fetch_val(
            select(func.avg(cls.rating))
                .where(cls.course_id == course_id)
        ) or 0
