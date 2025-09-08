from sqlmodel import Field

class TYPE:
    PRIMARY_KEY = Field(default=None, primary_key=True)
    FOREIGN_KEY = lambda field: Field(default=None, index=True,foreign_key=field, ondelete="cascade")  # noqa: E731
    UNIQUE = Field(default=None, unique=True)