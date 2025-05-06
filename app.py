from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)  # Changed from 'name' to '__name__' which is the standard
CORS(app)

# Database configuration
DB_HOST = 'dbtimur.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com'  # Replace with your RDS endpoint
DB_NAME = 'postgres'
DB_USER = 'postgres'    # Replace with your RDS username
DB_PASS = 'postgres'  # Replace with your RDS password
DB_PORT = '5432'

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Handles connection errors and returns a connection object.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")  # Log the error
        return None  # Important: Return None on failure

@app.route('/students', methods=['GET'])
def get_students():
    """
    Retrieves all students from the 'table_timur' table.
    Returns a JSON list of students.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Failed to connect to the database'}), 500
    cur = conn.cursor()
    try:
        cur.execute("SELECT student_id, full_name, gender, age, department, gpa, enrollment_year FROM table_timur")
        students = cur.fetchall()
        students_list = [{'student_id': student[0], 'full_name': student[1], 'gender': student[2],
                          'age': student[3], 'department': student[4], 'gpa': float(student[5]),
                          'enrollment_year': student[6]} for student in students]
        return jsonify(students_list)
    except psycopg2.Error as e:
        print(f"Error fetching students: {e}")
        return jsonify({'message': f'Error fetching students: {e}'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/students', methods=['POST'])
def add_student():
    """
    Adds a new student to the 'table_timur' table.
    Expects student data in JSON format in the request body.
    Returns a JSON message indicating success or failure.
    """
    data = request.get_json()
    full_name = data.get('full_name')
    gender = data.get('gender')
    age = data.get('age')
    department = data.get('department')
    gpa = data.get('gpa')
    enrollment_year = data.get('enrollment_year')

    if not all([full_name, gender, age, department, gpa, enrollment_year]):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Failed to connect to the database'}), 500
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO table_timur (full_name, gender, age, department, gpa, enrollment_year) VALUES (%s, %s, %s, %s, %s, %s)",
            (full_name, gender, age, department, gpa, enrollment_year)
        )
        conn.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error adding student: {e}")
        return jsonify({'message': f'Error adding student: {e}'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Deletes a student from the 'table_timur' table by student ID.
    Returns a JSON message indicating success or failure.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Failed to connect to the database'}), 500
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM table_timur WHERE student_id = %s", (student_id,))
        if cur.rowcount > 0:
            conn.commit()
            return jsonify({'message': f'Student with ID {student_id} deleted successfully'}), 200
        else:
            return jsonify({'message': f'Student with ID {student_id} not found'}), 404
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error deleting student: {e}")
        return jsonify({'message': f'Error deleting student: {e}'}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
