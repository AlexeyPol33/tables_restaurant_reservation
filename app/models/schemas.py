from datetime import datetime
from pydantic import BaseModel, FutureDatetime, field_validator


class TableBase(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(TableBase):
    @field_validator('name')
    def name_must_be_short(cls, v):
        if len(v) > 25:
            raise ValueError('Name must be 25 characters or less')
        return v


class Table(TableBase):
    id: int

    class Config:
        from_attributes = True


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int

    class Config:
        from_attributes = True