import requests

BASE_URL = "http://localhost:8080"
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6ImFkbWluMSIsIm5hbWUiOiJhZG1pbjFAb3N1LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci80MzljYjc4MzAwNjBkMjFiNTkxZjE2NDVjODRmNGQ4Nz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmFkLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA1VDA0OjExOjMwLjkxNloiLCJlbWFpbCI6ImFkbWluMUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzIxZjBkMzlmMjE5YWViOGY4MmUifQ.AzkGWAulVcvdeG3Z2S1kkcKg02Deh5R_KicTDB2snh8pqfZT3p_goLMePGKORld9HxD7HerVoqhz5zv-B8YXcZNP5fwhUhhEjGj7ZGy2suH50fVqrxP41AI7cNy598hSI_nhx8EoxODMIY9fGGcc7ICUjPjHfayfPtUpiyS5FHDfGSiFM-oqG1XCj06cuPsV5Z5NVz6ed2UBGr5epXnBg8VklGMUfy3NOEOZvlj8VGrvm1-1uTn7iISmG4DtTXs05A8N-xFp3SlxFPAAO9ZYMoDOciQk7-JeuB8QwoCUuBzpjg75UmEredEgs2hXA_1ukVj14EeymeKyF5R_UtUjCA"  # Replace with your admin token
INSTRUCTOR_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6Imluc3RydWN0b3IyIiwibmFtZSI6Imluc3RydWN0b3IyQG9zdS5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvOWE4MDA2NmVmODE3MDZlNDhiZWFmMjMxOGRlZGMwNjI_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZpbi5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNC0xMi0wNVQwNDoxMTozMS45MjBaIiwiZW1haWwiOiJpbnN0cnVjdG9yMkBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzI1Y2MzZDA2OGYzM2QxMWQxOGMifQ.ZkwD0IDbETyKYmMIc9A9cVEE-WUcMxeDL673SB5JXdjX4gnZZqoQt90XPrbhzhD-0I3FDFv7GLCpN76hqinMRR4ScZ8UL9ti0AjSDASJwS01plio5VG3aDXmA9LXVpNS6zpF21oG0Iio3s2NLliE4rfJu0AHriot6Cffd4NQuSkJSXe6GloZdFm6QWmaisHmAjV8MwdPEs314n9042zxxiiNRltrfH6WmVbZuJUovR6XQbn6MYR8PDSocwDhw05whMyjjQIYhEFZt16wpjxtC5KCl9CziUun1tP0zHEsAYGkoLSzdrfoMM2DDU3CHLJe9gfJy8I9M1nI-W6e3BuNLw"
INVALID_TOKEN = "Bearer invalid_token"
VALID_COURSE_ID = 5981907992969216  # Replace with your course ID
NON_EXISTENT_COURSE_ID = 9999999999999999
STUDENT_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6InN0dWRlbnQxIiwibmFtZSI6InN0dWRlbnQxQG9zdS5jb20iLCJwaWN0dXJlIjoiaHR0cHM6Ly9zLmdyYXZhdGFyLmNvbS9hdmF0YXIvMTJlNjM2MDllMDNkY2RiNzM1NGQyNWM3MjJjZDllMmQ_cz00ODAmcj1wZyZkPWh0dHBzJTNBJTJGJTJGY2RuLmF1dGgwLmNvbSUyRmF2YXRhcnMlMkZzdC5wbmciLCJ1cGRhdGVkX2F0IjoiMjAyNC0xMi0wNVQwNDoxMTozMi4yNzJaIiwiZW1haWwiOiJzdHVkZW50MUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MiwiZXhwIjoxNzMzNDA3ODkyLCJzdWIiOiJhdXRoMHw2NzUwYzMzNGQ1MmY3ZDlkOGI5ZjE4OWIifQ.Fc3js75VP_HZBPP6ue6BE8kg6U8yq2Nu0ZOaVc6OUwyv-uFneb4F6hWd0cS1frc-sq5v-3kDpGKR7eP52W-2m3r5R-LUvEmC2QRoVVXmMgIkwhbcUlVNof4yBrKMXXoTDRYjWVRQscqrP2PSy13tH4XZROjiHFmw_j5M0sj4KKCgQ5KENWbMSJ7UfjOjYmdmQODrx84yUIIzD6mnkbzvGkxl7itH6Mx3o8ZeldP7cvlGIRnUGSlcAxk3Rj44IVu1CRFhSKn7tqiYyzPfxK5QoChjo9ZYpAvQVi75sp7XGPXnp2Bvv1f9TwLGePe7Fdkbnh8I6dvUt4zIvhJTnP8iRg"

def test_admin_access():
    """Test admin accessing the enrollment list."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print("Test admin access passed. Response:", response.json())

def test_instructor_access():
    """Test instructor accessing the enrollment list."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": INSTRUCTOR_TOKEN}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print("Test instructor access passed. Response:", response.json())

def test_invalid_token():
    """Test request with an invalid token."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": INVALID_TOKEN}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    print("Test invalid token passed. Response:", response.json())

def test_nonexistent_course():
    """Test accessing enrollment for a non-existent course."""
    url = f"{BASE_URL}/courses/{NON_EXISTENT_COURSE_ID}/students"
    headers = {"Authorization": ADMIN_TOKEN}
    response = requests.get(url, headers=headers)
    assert response.status_code == 404
    print("Test non-existent course passed. Response:", response.json())

def test_unauthorized_access():
    """Test access by a user who is neither admin nor instructor."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}/students"
    headers = {"Authorization": STUDENT_TOKEN}  # Use a valid student token here
    response = requests.get(url, headers=headers)
    
    print(f"Status Code: {response.status_code}")  # Debugging
    print(f"Response Body: {response.json()}")     # Debugging
    
    assert response.status_code == 403
    print("Test unauthorized access passed.")


if __name__ == "__main__":
    test_admin_access()
    test_instructor_access()
    test_invalid_token()
    test_nonexistent_course()
    test_unauthorized_access()
