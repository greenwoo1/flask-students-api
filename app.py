import csv
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
CSV_FILE = 'students.csv'
FIELDNAMES = ['id', 'first_name', 'last_name', 'age']

def init_csv():
    """Створює CSV файл з заголовками, якщо він не існує."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def read_students():
    """Читає всіх студентів з CSV файлу."""
    students = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
    return students

def write_students(students):
    """Перезаписує CSV файл списком студентів."""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(students)

def get_next_id():
    """Генерує наступний ID (інкремент)."""
    students = read_students()
    if not students:
        return 1
    max_id = max(int(s['id']) for s in students)
    return max_id + 1

init_csv()


@app.route('/students', methods=['GET'])
def get_students():
    """
    1. Отримати список усіх студентів.
    2. Отримати студентів за прізвищем (query param ?last_name=...).
    """
    students = read_students()
    
    last_name_query = request.args.get('last_name')
    if last_name_query:
        filtered_students = [s for s in students if s['last_name'] == last_name_query]
        if not filtered_students:
            return jsonify({'error': 'Students with this last name not found'}), 404
        return jsonify(filtered_students), 200

    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    """Отримати інформацію про конкретного студента за ID."""
    students = read_students()
    student = next((s for s in students if int(s['id']) == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student), 200

@app.route('/students', methods=['POST'])
def create_student():
    """Створити нового студента."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = {'first_name', 'last_name', 'age'}
    received_fields = set(data.keys())

    if received_fields != required_fields:
        return jsonify({'error': 'Invalid fields. Required: first_name, last_name, age'}), 400

    new_student = {
        'id': str(get_next_id()),
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'age': str(data['age'])
    }

    students = read_students()
    students.append(new_student)
    write_students(students)

    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student_full(student_id):
    """Оновити інформацію про студента (повне оновлення)."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = {'first_name', 'last_name', 'age'}
    received_fields = set(data.keys())

    if received_fields != required_fields:
        return jsonify({'error': 'Invalid fields for PUT. Required: first_name, last_name, age'}), 400

    students = read_students()
    student_index = next((i for i, s in enumerate(students) if int(s['id']) == student_id), None)

    if student_index is None:
        return jsonify({'error': 'Student not found'}), 404

    students[student_index]['first_name'] = data['first_name']
    students[student_index]['last_name'] = data['last_name']
    students[student_index]['age'] = str(data['age'])
    
    write_students(students)
    return jsonify(students[student_index]), 200

@app.route('/students/<int:student_id>', methods=['PATCH'])
def update_student_age(student_id):
    """Оновити вік студента."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if set(data.keys()) != {'age'}:
        return jsonify({'error': 'Invalid fields for PATCH. Required only: age'}), 400

    students = read_students()
    student_index = next((i for i, s in enumerate(students) if int(s['id']) == student_id), None)

    if student_index is None:
        return jsonify({'error': 'Student not found'}), 404

    students[student_index]['age'] = str(data['age'])
    
    write_students(students)
    return jsonify(students[student_index]), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Видалити студента."""
    students = read_students()
    student_index = next((i for i, s in enumerate(students) if int(s['id']) == student_id), None)

    if student_index is None:
        return jsonify({'error': 'Student not found'}), 404

    deleted_student = students.pop(student_index)
    write_students(students)

    return jsonify({'message': f"Student ID {student_id} deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
