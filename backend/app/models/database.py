from sqlmodel import Field, SQLModel


class Food(SQLModel, table=True):
    """Database model for food ingredients."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field()
