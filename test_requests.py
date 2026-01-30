import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000/students'
OUTPUT_FILE = 'results.txt'

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("--- REST API Test Results ---\n\n")

def log(message):
    """Виводить повідомлення в консоль і записує у файл."""
    print(message)
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def run_tests():
    try:
        log("1. GET ALL (Initial):")
        response = requests.get(BASE_URL)
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log("2. POST 3 Students:")
        students_to_create = [
            {"first_name": "Ivan", "last_name": "Petrenko", "age": 20},
            {"first_name": "Maria", "last_name": "Kovalenko", "age": 22},
            {"first_name": "Oleg", "last_name": "Bondar", "age": 21}
        ]
        
        for s in students_to_create:
            resp = requests.post(BASE_URL, json=s)
            log(f"Created: {resp.status_code}, Body: {resp.json()}")
        log("-" * 30)

        log("3. GET ALL (After POST):")
        response = requests.get(BASE_URL)
        students = response.json()
        log(f"Status: {response.status_code}, Body: {json.dumps(students, indent=2)}")
        log("-" * 30)
        id_1, id_2, id_3 = 1, 2, 3

        log(f"4. PATCH Student ID {id_2} (Update age to 25):")
        patch_data = {"age": 25}
        response = requests.patch(f"{BASE_URL}/{id_2}", json=patch_data)
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log(f"5. GET Student ID {id_2}:")
        response = requests.get(f"{BASE_URL}/{id_2}")
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log(f"6. PUT Student ID {id_3} (Update all fields):")
        put_data = {"first_name": "Oleg_Updated", "last_name": "Bondar_New", "age": 30}
        response = requests.put(f"{BASE_URL}/{id_3}", json=put_data)
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log(f"7. GET Student ID {id_3}:")
        response = requests.get(f"{BASE_URL}/{id_3}")
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log("8. GET ALL (Before Delete):")
        response = requests.get(BASE_URL)
        log(f"Status: {response.status_code}, Body: {json.dumps(response.json(), indent=2)}")
        log("-" * 30)

        log(f"9. DELETE Student ID {id_1}:")
        response = requests.delete(f"{BASE_URL}/{id_1}")
        log(f"Status: {response.status_code}, Body: {response.json()}")
        log("-" * 30)

        log("10. GET ALL (Final):")
        response = requests.get(BASE_URL)
        log(f"Status: {response.status_code}, Body: {json.dumps(response.json(), indent=2)}")
        log("-" * 30)

        log("TEST COMPLETED. Results saved to results.txt")

    except Exception as e:
        log(f"CRITICAL ERROR: Is the server running? {e}")

if __name__ == "__main__":
    run_tests()
