import requests

BASE_URL = "http://localhost:8080"
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6ImFkbWluMSIsIm5hbWUiOiJhZG1pbjFAb3N1LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci80MzljYjc4MzAwNjBkMjFiNTkxZjE2NDVjODRmNGQ4Nz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmFkLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA1VDA0OjExOjMwLjkxNloiLCJlbWFpbCI6ImFkbWluMUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzIxZjBkMzlmMjE5YWViOGY4MmUifQ.AzkGWAulVcvdeG3Z2S1kkcKg02Deh5R_KicTDB2snh8pqfZT3p_goLMePGKORld9HxD7HerVoqhz5zv-B8YXcZNP5fwhUhhEjGj7ZGy2suH50fVqrxP41AI7cNy598hSI_nhx8EoxODMIY9fGGcc7ICUjPjHfayfPtUpiyS5FHDfGSiFM-oqG1XCj06cuPsV5Z5NVz6ed2UBGr5epXnBg8VklGMUfy3NOEOZvlj8VGrvm1-1uTn7iISmG4DtTXs05A8N-xFp3SlxFPAAO9ZYMoDOciQk7-JeuB8QwoCUuBzpjg75UmEredEgs2hXA_1ukVj14EeymeKyF5R_UtUjCA"  # Replace with your admin token
INSTRUCTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6Imluc3RydWN0b3IxIiwibmFtZSI6Imluc3RydWN0b3IxQG9zdS5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvMTA0OGYwMTE5OTRkMjM2N2I1NzI3ZGViN2NkYjM1NGI_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZpbi5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNC0xMi0wNVQwNDoxMTozMS41MDNaIiwiZW1haWwiOiJpbnN0cnVjdG9yMUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzIzZWE2NzEzN2YwMmU1MTMzNzUifQ.C0w7qyPZKeolPQQbaBExXulxcbF0vrJQmQZLpJVn7wORF8A6ckexIGEiOCnAxhO_29mKBsSFns5ZbyQdy3rSZQC1aNWfIN0e_-JaSn3vfn-vAEBwjePFDpijY_Rhr3aV7-DSqK6iHUE33pGPn_R9rjxpp6xqhcGVyCyqNPvmfx9_5hh003t5UXuvK4lFdErFG6nEZsiLr6anFz_Fw6gIll0mYrsuovVlhMxjlE8OkfH-Xn9yTw8XmZvx-I8CTG3ARID7rWs8PwDhiiQnviNNyV9xiyp9DbfQT5Cn6EBy7u1kmpOct7xrOjT58uPivRbo9SRYZ1IQQCoq9t53gZAFvg"
INVALID_TOKEN = "Bearer invalid_token"
VALID_COURSE_ID = 5981907992969216	
NON_EXISTENT_COURSE_ID = 9999999999999999

def test_add_students():
    """Test adding students to a course."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    body = {
        "add": [4856008086126592, 5081054809423872],  # Use valid student IDs from your database
        "remove": []
    }
    print(f"Testing add students with body: {body}")
    response = requests.patch(url, headers=headers, json=body)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 200, "Adding students failed!"
    print("Test add students passed.")



def test_remove_students():
    """Test removing students from a course."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    body = {
        "add": [],
        "remove": [4856008086126592]  # Use a student ID you just added
    }
    print(f"Testing remove students with body: {body}")
    response = requests.patch(url, headers=headers, json=body)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    assert response.status_code == 200, "Removing students failed!"
    print("Test remove students passed.")


def test_conflict_data():
    """Test conflict with overlapping add and remove arrays."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    body = {
        "add": [5642368648740864],
        "remove": [5642368648740864]
    }
    response = requests.patch(url, headers=headers, json=body)
    assert response.status_code == 409
    print("Test conflict data passed.")

def test_invalid_student_ids():
    """Test invalid student IDs in add or remove arrays."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    body = {
        "add": [9999999999999999],
        "remove": []
    }
    response = requests.patch(url, headers=headers, json=body)
    assert response.status_code == 409
    print("Test invalid student IDs passed.")

def test_unauthorized_access():
    """Test unauthorized user trying to update enrollment."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": INVALID_TOKEN}
    body = {
        "add": [5642368648740864],
        "remove": []
    }
    response = requests.patch(url, headers=headers, json=body)
    assert response.status_code == 401
    print("Test unauthorized access passed.")

if __name__ == "__main__":
    test_add_students()
    test_remove_students()
    test_conflict_data()
    test_invalid_student_ids()
    test_unauthorized_access()
