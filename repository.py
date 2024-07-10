from random import choice

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import new_session, ScheduleOrm




class ScheduleRepository:
    @classmethod
    async def get_group_schedule(cls, group: str, week: int):
        async with new_session() as session:
            query = select(ScheduleOrm).options(joinedload(ScheduleOrm.place)).options(joinedload(ScheduleOrm.lesson)).options(joinedload(ScheduleOrm.teacher)).filter_by(group_name=group, week_id=week)
            res = await session.execute(query)
            lessons: list[ScheduleOrm] = res.scalars().all()
            if not lessons:
                return {"success": False}

            # {"name": "",
            #  "place": "",
            #  "teacher": "",
            #  "time": "",
            #  "type": ""
            #  }
            days = {}
            for lesson in lessons:
                group_name = lesson.group_name
                date = lesson.date
                week_id = lesson.week_id
                time = lesson.time
                day_name = lesson.day_name
                place, teacher, lesson_name = "", "", ""
                if lesson.place:
                    place = lesson.place.place
                if lesson.teacher:
                    teacher = lesson.teacher.fullname
                if lesson.lesson:
                    lesson_name = lesson.lesson.name
                days[day_name] = days.get(day_name, dict())
                days[day_name]["name"] = days[day_name].get("name", day_name)
                print(days[day_name])
                days[day_name]["date"] = days[day_name].get("date", date)
                days[day_name]["lessons"] = days[day_name].get("lessons", list()) + [{"name": lesson_name, "place": place, "teacher": teacher, "time": time, "type": choice(["ЛК", "ПЗ", "ЛР"])}]
            print(days)

            return {"success": True,
                    group_name: {"number": week_id,
                                 "days": [i for i in days.values()]}}

