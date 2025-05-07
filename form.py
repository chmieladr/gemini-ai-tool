import json

from pydantic import BaseModel, Field, EmailStr


class HelpdeskForm(BaseModel):
    firstname: str = Field(..., max_length=20)
    lastname: str = Field(..., max_length=20)
    email: EmailStr
    reason_of_contact: str = Field(..., max_length=100)
    urgency: int = Field(..., ge=1, le=10)

    def update_from_json(self, json_string: str):
        try:
            data = json.loads(json_string)
            for key, value in data.items():
                if hasattr(self, key) and value is not None and value != "":
                    setattr(self, key, value) if key != "urgency" else setattr(self, key, int(value))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")
