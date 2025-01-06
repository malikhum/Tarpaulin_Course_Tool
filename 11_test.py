import requests

# Replace with your actual tokens and server URL
BASE_URL = "http://localhost:8080"
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6ImFkbWluMSIsIm5hbWUiOiJhZG1pbjFAb3N1LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci80MzljYjc4MzAwNjBkMjFiNTkxZjE2NDVjODRmNGQ4Nz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmFkLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA1VDA0OjExOjMwLjkxNloiLCJlbWFpbCI6ImFkbWluMUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzIxZjBkMzlmMjE5YWViOGY4MmUifQ.AzkGWAulVcvdeG3Z2S1kkcKg02Deh5R_KicTDB2snh8pqfZT3p_goLMePGKORld9HxD7HerVoqhz5zv-B8YXcZNP5fwhUhhEjGj7ZGy2suH50fVqrxP41AI7cNy598hSI_nhx8EoxODMIY9fGGcc7ICUjPjHfayfPtUpiyS5FHDfGSiFM-oqG1XCj06cuPsV5Z5NVz6ed2UBGr5epXnBg8VklGMUfy3NOEOZvlj8VGrvm1-1uTn7iISmG4DtTXs05A8N-xFp3SlxFPAAO9ZYMoDOciQk7-JeuB8QwoCUuBzpjg75UmEredEgs2hXA_1ukVj14EeymeKyF5R_UtUjCA"  # Replace with your admin token
NON_ADMIN_TOKEN = "Bearer xxx"
INVALID_TOKEN = "Bearer invalid_token"
VALID_COURSE_ID = 5083538508480512  # Replace with an actual course ID
NON_EXISTENT_COURSE_ID = 9999999999999999

def test_successful_deletion():
    """Test successful deletion by an admin."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}"
    headers = {"Authorization": ADMIN_TOKEN}
    response = requests.delete(url, headers=headers)
    
    assert response.status_code == 204, f"Expected 204, got {response.status_code}"
    print("Test successful deletion passed.")


def test_unauthorized_user():
    """Test deletion by a non-admin user."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}"
    headers = {"Authorization": NON_ADMIN_TOKEN}
    response = requests.delete(url, headers=headers)

    assert response.status_code == 403, f"Expected 403, got {response.status_code}"
    assert response.json()["Error"] == "You don't have permission on this resource", "Error message mismatch."
    print("Test unauthorized user passed.")


def test_missing_or_invalid_jwt():
    """Test deletion with missing or invalid JWT."""
    url = f"{BASE_URL}/courses/{VALID_COURSE_ID}"
    headers = {"Authorization": INVALID_TOKEN}
    response = requests.delete(url, headers=headers)

    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json()["Error"] == "Unauthorized", "Error message mismatch."
    print("Test missing or invalid JWT passed.")


def test_course_not_found():
    """Test deletion for a non-existing course."""
    url = f"{BASE_URL}/courses/{NON_EXISTENT_COURSE_ID}"
    headers = {"Authorization": ADMIN_TOKEN}
    response = requests.delete(url, headers=headers)

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert response.json()["Error"] == "Not found", "Error message mismatch."
    print("Test course not found passed.")


if __name__ == "__main__":
    try:
        test_successful_deletion()
    except AssertionError as e:
        print(f"Test failed: {e}")
    
    try:
        test_unauthorized_user()
    except AssertionError as e:
        print(f"Test failed: {e}")
    
    try:
        test_missing_or_invalid_jwt()
    except AssertionError as e:
        print(f"Test failed: {e}")
    
    try:
        test_course_not_found()
    except AssertionError as e:
        print(f"Test failed: {e}")
