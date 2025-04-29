from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel

app = FastAPI()

# Model để validate dữ liệu đầu vào
class Student(BaseModel):
    cccd: str
    name: str
    phone: str

# Kết nối với MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql",  # Tên service MySQL trong docker-compose
            user="root",   # Mặc định user của MySQL
            password="",   # Mật khẩu rỗng
            database="student_db"
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {e}")

# [CREATE] Thêm một sinh viên mới
@app.post("/students/")
def create_student(student: Student):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "INSERT INTO students (cccd, name, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, (student.cccd, student.name, student.phone))
        connection.commit()
        return {"message": "Student created successfully", "student": student}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

# [READ] Lấy thông tin sinh viên theo tên (đã có)
@app.get("/lookup_student/")
def lookup_student(name: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students WHERE name = %s"
        cursor.execute(query, (name,))
        student = cursor.fetchone()
        
        if student:
            return {
                "cccd": student["cccd"],
                "name": student["name"],
                "phone": student["phone"]
            }
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

# [READ] Lấy danh sách tất cả sinh viên
@app.get("/students/")
def get_all_students():
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students"
        cursor.execute(query)
        students = cursor.fetchall()
        
        if students:
            return students
        else:
            raise HTTPException(status_code=404, detail="No students found")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

# [UPDATE] Cập nhật thông tin sinh viên theo CCCD
@app.put("/students/{cccd}")
def update_student(cccd: str, student: Student):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "UPDATE students SET name = %s, phone = %s WHERE cccd = %s"
        cursor.execute(query, (student.name, student.phone, cccd))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student updated successfully", "cccd": cccd}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()

# [DELETE] Xóa sinh viên theo CCCD
@app.delete("/students/{cccd}")
def delete_student(cccd: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = "DELETE FROM students WHERE cccd = %s"
        cursor.execute(query, (cccd,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully", "cccd": cccd}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()