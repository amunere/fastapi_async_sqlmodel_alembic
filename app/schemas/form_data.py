from sqlmodel import SQLModel


class FormData(SQLModel):
    title: str
    description: str
    tags: list