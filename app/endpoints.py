from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.deps import get_db
from app import models
from app import schemas
from typing import List
from io import StringIO
import csv


router = APIRouter()


@router.post("/", status_code=201)
def add_customers(
    payload: schemas.CreateCustomerSchema, db: Session = Depends(get_db)
) -> schemas.CustomerSchema:
    new_customer = models.CustomerModel(**payload.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.get("/")
def get_customers(db: Session = Depends(get_db)) -> List[schemas.CustomerSchema]:
    return db.query(models.CustomerModel).all()


@router.get("/export")
def export_customers(db: Session = Depends(get_db)):
    from_db = db.query(models.CustomerModel).all()
    data = [[obj.id, obj.name, obj.description] for obj in from_db]
    f = StringIO()
    csv.writer(f).writerows(data)

    response = StreamingResponse(iter([f.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response


@router.get("/{id}")
def get_customer(id: str, db: Session = Depends(get_db)):
    customer = (
        db.query(models.CustomerModel).filter(models.CustomerModel.id == id).first()
    )
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No customer with this id: {id} found",
        )
    return customer
