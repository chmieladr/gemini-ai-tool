from pydantic import BaseModel, Field, EmailStr, ValidationError


class HelpdeskForm(BaseModel):
    firstname: str = Field(..., max_length=20)
    lastname: str = Field(..., max_length=20)
    email: EmailStr
    reason_of_contact: str = Field(..., max_length=100)
    urgency: int = Field(..., ge=1, le=10)

    def __setattr__(self, name, value):
        if name in self.model_fields:
            update_data = {name: value}
            try:
                validated = self.__class__.model_validate({**self.model_dump(), **update_data})
                super().__setattr__(name, getattr(validated, name))
            except ValidationError:
                return  # Do not set the attribute if validation fails
        else:  # For non-field attributes, proceed normally
            super().__setattr__(name, value)
