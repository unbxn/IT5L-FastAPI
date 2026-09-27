from typing import Literal
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StudentCreate(BaseModel):
    student_id: int = Field(gt=0)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    program: Literal["BSIT", "BSCS", "BSEMC", "BMA", "BLIS"]
    year_level: int = Field(ge=1, le=4)

# Fixed indentation here
@app.get("/")
def home():
    return {"message": "Student API is running"}

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.StudentRecord).all()

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.StudentRecord).filter(models.StudentRecord.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/students", status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.StudentRecord).filter(models.StudentRecord.student_id == student.student_id).first()
    if db_student:
        raise HTTPException(status_code=409, detail="Student ID already exists")
    
    new_student = models.StudentRecord(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.StudentRecord).filter(models.StudentRecord.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    db_student.first_name = updated_student.first_name
    db_student.last_name = updated_student.last_name
    db_student.program = updated_student.program
    db_student.year_level = updated_student.year_level
    
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}", status_code=200)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.StudentRecord).filter(models.StudentRecord.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    db.delete(db_student)
    db.commit()
    return {"message": f"Student {student_id} successfully deleted"}