from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engin = create_async_engine(
    "sqlite+aiosqlite:///schedule.db"
)

new_session = async_sessionmaker(engin, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ScheduleOrm(Model):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str]
    date: Mapped[str]
    time: Mapped[str]
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["TeacherOrm"] = relationship("TeacherOrm")
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id"))
    place: Mapped["PlaceOrm"] = relationship("PlaceOrm")
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    lesson: Mapped["LessonOrm"] = relationship("LessonOrm")
    day_name: Mapped[str]
    week_id: Mapped[int]


class TeacherOrm(Model):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str]

    schedule: Mapped[list["ScheduleOrm"]] = relationship("ScheduleOrm")


class PlaceOrm(Model):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    place: Mapped[str]

    schedule: Mapped[list["ScheduleOrm"]] = relationship("ScheduleOrm")


class LessonOrm(Model):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    schedule: Mapped[list["ScheduleOrm"]] = relationship("ScheduleOrm")
