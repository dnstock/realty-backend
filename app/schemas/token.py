from pydantic import BaseModel, ConfigDict

class Base(BaseModel):
    access_token: str
    refresh_token: str

class Read(Base):
    model_config = ConfigDict(from_attributes=True)
