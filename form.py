from pydantic import BaseModel, Field, EmailStr


class HelpdeskForm(BaseModel):
    firstname: str = Field(..., max_length=20)
    lastname: str = Field(..., max_length=20)
    email: EmailStr
    reason_of_contact: str = Field(..., max_length=100)
    urgency: int = Field(..., ge=1, le=10)
