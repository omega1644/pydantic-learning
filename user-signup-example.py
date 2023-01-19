from datetime import datetime
from pydantic import (BaseModel, ValidationError,
                      EmailStr, validator,
                      root_validator, Field)
from typing import Optional


class UserSignUp(BaseModel):
    username: str = Field(..., max_length=20)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)
    datetime_signup: datetime = Field(None)
    password1: str
    password2: str

    @validator('datetime_signup', pre=True, always=True)
    def set_signup_time(cls, value):
        return value or datetime.now()

    @validator('username')
    def username_is_alpha_numeric(cls, value):
        assert value.isalnum()
        return value

    @root_validator
    def exist_either_email_or_phone(cls, values):
        if "email" in values or "phone" in values:
            return values
        else:
            raise ValueError("Need either email or phone")

    @root_validator
    def checking_retyped_password(cls, values):
        if values["password1"] == values["password2"]:
            return values
        else:
            raise ValueError("Passwords do not match")


if __name__ == "__main__":
    try:
        user = UserSignUp(
            username='omega',
            email='chimichunga@gmail.com',
            password1='strong_password',
            password2='strong_password'
        )
        print(user.dict())
    except ValidationError as err:
        print(f"Error: {err}")
