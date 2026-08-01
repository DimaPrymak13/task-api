from pydantic import BaseModel, ConfigDict


# ---Task---

class TaskCreate(BaseModel):
    title: str


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: str


# ---Subtask---

class SubtaskCreate(BaseModel):
    title: str


class SubtaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: str
    tasks_id: int
