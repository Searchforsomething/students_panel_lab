from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import uvicorn
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# База данных
DATABASE_URL = "postgresql://postgres:postgres@db:5432/students_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

students_data = [
    {"first_name": "Иван", "last_name": "Иванов", "patronymic": "Иванович", "group": "N3101", "grade": 1, "faculty": "ФБИТ"},
    {"first_name": "Мария", "last_name": "Петрова", "patronymic": "Сергеевна", "group": "M3202", "grade": 2, "faculty": "ФИТиП"},
    {"first_name": "Алексей", "last_name": "Смирнов", "patronymic": "Олегович", "group": "H3303", "grade": 3, "faculty": "Центр ХИ"},
    {"first_name": "Ольга", "last_name": "Сидорова", "patronymic": "Владимировна", "group": "P3404", "grade": 4, "faculty": "ФПИ и КТ"},
    {"first_name": "Дмитрий", "last_name": "Кузнецов", "patronymic": "Александрович", "group": "U3305", "grade": 3, "faculty": "ФТМИ"},
    {"first_name": "Анастасия", "last_name": "Фёдорова", "patronymic": "Николаевна", "group": "J3306", "grade": 3, "faculty": "ФЦТ"},
    {"first_name": "Николай", "last_name": "Попов", "patronymic": "Игоревич", "group": "U3407", "grade": 4, "faculty": "ФТМИ"},
    {"first_name": "Елена", "last_name": "Волкова", "patronymic": "Андреевна", "group": "M3308", "grade": 3, "faculty": "ФИТиП"},
    {"first_name": "Андрей", "last_name": "Соколов", "patronymic": "Михайлович", "group": "N3151", "grade": 1, "faculty": "ФБИТ"},
    {"first_name": "Екатерина", "last_name": "Зайцева", "patronymic": "Васильевна", "group": "M3232", "grade": 2, "faculty": "ФИТиП"},
    {"first_name": "Максим", "last_name": "Воронов", "patronymic": "Алексеевич", "group": "H3303", "grade": 3, "faculty": "Центр ХИ"},
    {"first_name": "Светлана", "last_name": "Тимофеева", "patronymic": "Юрьевна", "group": "P3404", "grade": 4, "faculty": "ФПИ и КТ"},
    {"first_name": "Владимир", "last_name": "Григорьев", "patronymic": "Павлович", "group": "U3305", "grade": 3, "faculty": "ФТМИ"},
    {"first_name": "Ирина", "last_name": "Михайлова", "patronymic": "Сергеевна", "group": "J3306", "grade": 3, "faculty": "ФЦТ"},
    {"first_name": "Артем", "last_name": "Крылов", "patronymic": "Игоревич", "group": "M3307", "grade": 3, "faculty": "ФИТиП"},
    {"first_name": "Юлия", "last_name": "Тарасова", "patronymic": "Евгеньевна", "group": "M3408", "grade": 4, "faculty": "ФИТиП"},
    {"first_name": "Виктор", "last_name": "Никитин", "patronymic": "Борисович", "group": "J3229", "grade": 2, "faculty": "ФЦТ"},
    {"first_name": "Анна", "last_name": "Ковалева", "patronymic": "Дмитриевна", "group": "R3110", "grade": 1, "faculty": "ФСУ и Р"},
    {"first_name": "Сергей", "last_name": "Николаев", "patronymic": "Борисович", "group": "J3209", "grade": 2, "faculty": "ФЦТ"},
    {"first_name": "Татьяна", "last_name": "Авдалова", "patronymic": "Евгеньевна", "group": "R3110", "grade": 1, "faculty": "ФСУ и Р"}
]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель таблицы
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    patronymic = Column(String(100))
    group = Column(String(10))
    grade = Column(Integer)
    faculty = Column(String(100))


# Pydantic модель
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    group: str
    grade: int
    faculty: str


Base.metadata.create_all(bind=engine)

session = SessionLocal()
for student_data in students_data:
    student = Student(**student_data)
    session.add(student)
session.commit()

# Роуты
@app.get("/students")
def get_students(page: int = Query(1), size: int = Query(10)):
    session = SessionLocal()
    students = session.query(Student).offset((page - 1) * size).limit(size).all()
    total = session.query(Student).count()
    session.close()
    return {"data": students, "total": total, "page": page, "size": size}


@app.post("/students/")
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        patronymic=student.patronymic,
        group=student.group,
        grade=student.grade,
        faculty=student.faculty
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message": "Студент успешно добавлен", "student": new_student}


@app.put("/students/{id}")
def update_student(id: int, student: StudentCreate):
    session = SessionLocal()
    db_student = session.query(Student).filter(Student.id == id).first()
    if not db_student:
        session.close()
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    session.commit()
    session.close()
    return db_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.delete(student)
    db.commit()
    return {"message": "Студент успешно удалён"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
