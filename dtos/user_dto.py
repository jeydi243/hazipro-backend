from pydantic import BaseModel, Field

class UserDTO(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    stay_connected: str = Field(default="off")