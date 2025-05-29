import mysql.connector

def get_db_connection():
    """
    MySQL DB에 접속하는 함수
    """
    conn = mysql.connector.connect(
        host="localhost",           # 또는 db 서버 주소
        user="root",                # 사용자 계정
        password="your_password",   # 본인의 비밀번호
        database="haedal_uni"       # 사용할 데이터베이스
    )
    return conn

def verify_student_login(num: int, name: str, phone: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM student
        WHERE num = %s AND name = %s AND phone = %s
    """
    cursor.execute(query, (num, name, phone))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None
