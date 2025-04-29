from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Kết nối với MySQL (sử dụng thông tin từ XAMPP hoặc container MySQL)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql",  # Tên service MySQL trong docker-compose
            user="root",   # Mặc định user của MySQL trong XAMPP
            password="",   # Mặc định không có mật khẩu trong XAMPP
            database="student_db"
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to database: {e}")

# Endpoint để lấy thông tin sinh viên theo tên
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