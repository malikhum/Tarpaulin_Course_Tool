import requests

BASE_URL = "http://localhost:8080/courses"
COURSE_ID = "5083538508480512"  # Replace with an actual course ID from your datastore
INVALID_COURSE_ID = "9999999999999999"
ADMIN_TOKEN = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ino1Ty1TNEJ4SU0wZlFoN1dZalhRSSJ9.eyJuaWNrbmFtZSI6ImFkbWluMSIsIm5hbWUiOiJhZG1pbjFAb3N1LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci80MzljYjc4MzAwNjBkMjFiNTkxZjE2NDVjODRmNGQ4Nz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRmFkLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI0LTEyLTA1VDA0OjExOjMwLjkxNloiLCJlbWFpbCI6ImFkbWluMUBvc3UuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczovL2Rldi10N3hmdDJkbno1eTB6MXBlLnVzLmF1dGgwLmNvbS8iLCJhdWQiOiJQcGRWSFdZNFJVOXR4QWg3T0dnUEVCNEZPb2YwNnZvMyIsImlhdCI6MTczMzM3MTg5MSwiZXhwIjoxNzMzNDA3ODkxLCJzdWIiOiJhdXRoMHw2NzUwYzIxZjBkMzlmMjE5YWViOGY4MmUifQ.AzkGWAulVcvdeG3Z2S1kkcKg02Deh5R_KicTDB2snh8pqfZT3p_goLMePGKORld9HxD7HerVoqhz5zv-B8YXcZNP5fwhUhhEjGj7ZGy2suH50fVqrxP41AI7cNy598hSI_nhx8EoxODMIY9fGGcc7ICUjPjHfayfPtUpiyS5FHDfGSiFM-oqG1XCj06cuPsV5Z5NVz6ed2UBGr5epXnBg8VklGMUfy3NOEOZvlj8VGrvm1-1uTn7iISmG4DtTXs05A8N-xFp3SlxFPAAO9ZYMoDOciQk7-JeuB8QwoCUuBzpjg75UmEredEgs2hXA_1ukVj14EeymeKyF5R_UtUjCA"  # Replace with your admin token
NON_ADMIN_TOKEN = "Bearer xxx"  # Replace with a non-admin token

HEADERS_ADMIN = {
    "Authorization": ADMIN_TOKEN,
    "Content-Type": "application/json"
}

HEADERS_NON_ADMIN = {
    "Authorization": NON_ADMIN_TOKEN,
    "Content-Type": "application/json"
}


# def test_valid_partial_update():
#     """Test a valid partial update to the course term."""
#     body = {"term": "spring-25"}
#     response = requests.patch(f"{BASE_URL}/{COURSE_ID}", headers=HEADERS_ADMIN, json=body)
#     print("Status Code:", response.status_code)
#     print("Response Body:", response.text)
#     assert response.status_code == 200
#     json_data = response.json()
#     assert json_data["term"] == "spring-25"
#     print("Test valid partial update passed.")



# def test_update_with_instructor_id():
#     """Test updating the instructor ID."""
#     body = {"instructor_id": 5644004762845184}
#     response = requests.patch(f"{BASE_URL}/{COURSE_ID}", headers=HEADERS_ADMIN, json=body)
#     assert response.status_code == 200
#     json_data = response.json()
#     assert json_data["instructor_id"] == 5644004762845184
#     print("Test update with instructor ID passed.")


# def test_empty_request_body():
#     """Test sending an empty request body."""
#     body = {}
#     response = requests.patch(f"{BASE_URL}/{COURSE_ID}", headers=HEADERS_ADMIN, json=body)
#     assert response.status_code == 200
#     json_data = response.json()
#     assert json_data["term"] == "spring-25"  # Verify term remains unchanged
#     print("Test empty request body passed.")


# def test_invalid_instructor_id():
#     """Test updating with an invalid instructor ID."""
#     body = {"instructor_id": 9999999999999999}
#     response = requests.patch(f"{BASE_URL}/{COURSE_ID}", headers=HEADERS_ADMIN, json=body)
#     assert response.status_code == 400
#     json_data = response.json()
#     assert json_data["Error"] == "The request body is invalid"
#     print("Test invalid instructor ID passed.")


def test_unauthorized_user():
    """Test updating a course with an unauthorized user."""
    body = {"term": "summer-25"}
    response = requests.patch(f"{BASE_URL}/{COURSE_ID}", headers=HEADERS_NON_ADMIN, json=body)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
    
    # Check for either 401 or 403
    assert response.status_code in [401, 403], "Expected status code 401 or 403"
    if response.status_code == 403:
        print("Test unauthorized user passed with 403.")
    elif response.status_code == 401:
        print("Test unauthorized user passed with 401.")




def test_course_not_found():
    """Test trying to update a non-existing course."""
    body = {"term": "winter-25"}
    response = requests.patch(f"{BASE_URL}/{INVALID_COURSE_ID}", headers=HEADERS_ADMIN, json=body)
    assert response.status_code == 404
    json_data = response.json()
    assert json_data["Error"] == "Not found"
    print("Test course not found passed.")


if __name__ == "__main__":
    # test_valid_partial_update()
    # test_update_with_instructor_id()
    # test_empty_request_body()
    # test_invalid_instructor_id()
    test_unauthorized_user()
    test_course_not_found()
