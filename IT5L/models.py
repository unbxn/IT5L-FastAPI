from sqlalchemy import Column, Integer, String
from database import Base  # <-- Make sure this line is present

class StudentRecord(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    program = Column(String(10))
    year_level = Column(Integer)