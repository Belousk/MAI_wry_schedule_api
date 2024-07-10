from fastapi import FastAPI
from pydantic import BaseModel

from repository import ScheduleRepository

app = FastAPI()


class Schedule(BaseModel):
    id: int
    group_name: str
    date: str
    time: str
    teacher_id: int
    place_id: int
    lesson_id: int
    day_name: str
    week_id: int


@app.get('/{group_name}/{week}')
async def get_home(group_name: str, week: int):
    print(group_name)
    lessons = await ScheduleRepository.get_group_schedule(group_name, week)
    return lessons