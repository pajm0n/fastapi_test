from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class CustomerBaseSchema(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class CreateCustomerSchema(CustomerBaseSchema):
    ...


class CustomerSchema(CustomerBaseSchema):
    id: uuid.UUID
