# Flask app setup
from flask import Flask, request, jsonify, make_response
from google.cloud import datastore, storage
from jose import jwt
import requests
import json
from urllib.request import urlopen
import ssl

app = Flask(__name__)
app.secret_key = ''

# Google Cloud Datastore and Storage clients
client = datastore.Client()
storage_client = storage.Client()
bucket_name = "avatars-malikhuma6"



# Auth0 Configuration
CLIENT_ID = ''
CLIENT_SECRET = ''
DOMAIN = ''
ALGORITHMS = ["RS256"]

# SSL bypass context for local development
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Error handling class
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    """Handle AuthError exceptions and return consistent error responses."""
    if ex.status_code == 401:
        # Return only the flat "Unauthorized" error for 401
        return jsonify({"Error": "Unauthorized"}), 401
    elif ex.status_code == 403:
        # Return only the flat "You don't have permission on this resource" error for 403
        return jsonify({"Error": "You don't have permission on this resource"}), 403
    elif ex.status_code == 400:
        return jsonify({"Error": "The request body is invalid"}), 400
    elif ex.status_code == 404:
        return jsonify({"Error": "Not found"}), 404
    else:
        return jsonify({"Error": "An error occurred"}), ex.status_code


# Helper: Verify the JWT
def verify_jwt(request):
    """Verify the JWT and return the payload."""
    if 'Authorization' not in request.headers:
        raise AuthError({"code": "missing_auth_header", "description": "Authorization header is required"}, 401)

    auth_header = request.headers['Authorization'].split()
    if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
        raise AuthError({"code": "invalid_auth_header", "description": "Authorization header must be 'Bearer <token>'"}, 401)

    token = auth_header[1]
    if not token or token.count('.') != 2:
        raise AuthError("Unauthorized", 401)




    try:
        jsonurl = urlopen(f"https://{DOMAIN}/.well-known/jwks.json", context=ssl_context)
        jwks = json.loads(jsonurl.read())
    except Exception:
        raise AuthError({"code": "jwks_fetch_error", "description": "Unable to fetch JWKS"}, 401)

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break

    if not rsa_key:
        raise AuthError({"code": "no_rsa_key", "description": "No RSA key found"}, 401)

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            issuer=f"https://{DOMAIN}/",
            audience=CLIENT_ID
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "The token has expired"}, 401)
    except jwt.JWTClaimsError as e:
        print("JWT Claims Error:", str(e))  # Debugging
        raise AuthError({"code": "invalid_claims", "description": "Incorrect claims. Check issuer/audience."}, 401)
    except Exception as e:
        raise AuthError({"code": "invalid_token", "description": f"Unable to parse token: {str(e)}"}, 401)

# User Login
@app.route('/users/login', methods=['POST'])
def login_user():
    """Log in a user and return a JWT."""
    content = request.get_json()
    if not content or 'username' not in content or 'password' not in content:
        return jsonify({"Error": "The request body is invalid"}), 400

    body = {
        'grant_type': 'password',
        'username': content["username"],
        'password': content["password"],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'openid profile email'  # Ensures id_token is returned
    }

    headers = {'content-type': 'application/json'}
    url = f"https://{DOMAIN}/oauth/token"
    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        id_token = token_data.get("id_token")
        if id_token:
            return jsonify({"token": id_token}), 200
        else:
            return jsonify({"Error": "Unauthorized"}), 401
    elif response.status_code == 400:
        return jsonify({"Error": "The request body is invalid"}), 400
    else:
        return jsonify({"Error": "Unauthorized"}), 401  # Standardized error message

# Get All Users Endpoint
@app.route("/users", methods=["GET"])
def get_all_users():
    """Get all users if the requester is an admin."""
    try:
        payload = verify_jwt(request)
        user_sub = payload.get("sub")
        print("User sub from JWT:", user_sub)

        query = client.query(kind="user")
        query.add_filter("sub", "=", user_sub)
        user_entity = list(query.fetch())
        print("Fetched user entity:", user_entity)

        if not user_entity or user_entity[0].get("role") != "admin":
            raise AuthError("You don't have permission on this resource", 403)


        print("User role is admin. Fetching all users...")
        all_users_query = client.query(kind="user")
        all_users = list(all_users_query.fetch())
        response = [{"id": entity.key.id, "role": entity.get("role"), "sub": entity.get("sub")} for entity in all_users]
        return jsonify(response), 200

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get details of a user."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")
        print(f"User sub from JWT: {user_sub}")

        # Fetch the requested user from Datastore
        user_key = client.key("user", user_id)
        user_entity = client.get(user_key)

        # If the user doesn't exist, return 403
        if not user_entity:
            raise AuthError("You don't have permission on this resource", 403)

        # Check if the requester is an admin or the user themselves
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity:
            raise AuthError("You don't have permission on this resource", 403)

        requesting_user_role = requesting_user_entity[0].get("role")

        if requesting_user_role != "admin" and user_entity.get("sub") != user_sub:
            raise AuthError("You don't have permission on this resource", 403)

        # Prepare the response
        response = {
            "id": user_entity.key.id,
            "role": user_entity.get("role"),
            "sub": user_entity.get("sub")
        }

        # Add avatar_url if the user has an avatar
        avatar_blob_name = f"avatars/{user_id}"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(avatar_blob_name)
        if blob.exists():
            response["avatar_url"] = f"{request.host_url}users/{user_id}/avatar".rstrip('/')

        # Add courses for instructors and students
        if user_entity.get("role") in ["instructor", "student"]:
            course_query = client.query(kind="course")
            if user_entity.get("role") == "instructor":
                course_query.add_filter("instructor_id", "=", user_id)
            elif user_entity.get("role") == "student":
                course_query.add_filter("student_ids", "=", user_id)

            courses = list(course_query.fetch())
            response["courses"] = [f"{request.host_url}courses/{course.key.id}".rstrip('/') for course in courses]

        return jsonify(response), 200

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500

@app.route('/users/<int:user_id>/avatar', methods=['POST'])
def upload_user_avatar(user_id):
    """Create or update a user's avatar."""
    try:
        # Check if the request contains a 'file' key
        if 'file' not in request.files:
            return jsonify({"Error": "The request body is invalid"}), 400

        # Verify JWT and ensure it's owned by the user
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Fetch the user entity from Datastore
        user_key = client.key("user", user_id)
        user_entity = client.get(user_key)
        if not user_entity:
            return jsonify({"Error": "User not found"}), 403

        # Ensure the requesting user is the owner of the resource
        if user_entity.get("sub") != user_sub:
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Process the uploaded file
        file = request.files['file']
        if not file.filename.endswith('.png'):
            return jsonify({"Error": "Only .png files are supported"}), 400

        # Upload the file to Google Cloud Storage
        avatar_blob_name = f"avatars/{user_id}"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(avatar_blob_name)
        blob.upload_from_file(file, content_type='image/png')

        # Generate the avatar URL
        avatar_url = f"{request.host_url}users/{user_id}/avatar".rstrip('/')
        return jsonify({"avatar_url": avatar_url}), 200

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    

@app.route('/users/<int:user_id>/avatar', methods=['GET'])
def get_user_avatar(user_id):
    """Return the user's avatar file."""
    try:
        # Verify JWT and ensure it's owned by the user
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Fetch the user entity from Datastore
        user_key = client.key("user", user_id)
        user_entity = client.get(user_key)
        if not user_entity:
            return jsonify({"Error": "User not found"}), 403

        # Ensure the requesting user is the owner of the resource
        if user_entity.get("sub") != user_sub:
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Fetch the avatar from Google Cloud Storage
        avatar_blob_name = f"avatars/{user_id}"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(avatar_blob_name)
        if not blob.exists():
            return jsonify({"Error": "Not found"}), 404

        # Return the file as the response
        return blob.download_as_bytes(), 200, {
            "Content-Type": "image/png",
            "Content-Disposition": f"inline; filename={user_id}_avatar.png"
        }

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500

@app.route('/users/<int:user_id>/avatar', methods=['DELETE'])
def delete_user_avatar(user_id):
    """Delete a user's avatar."""
    try:
        # Verify JWT and ensure it's owned by the user
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Fetch the user entity from Datastore
        user_key = client.key("user", user_id)
        user_entity = client.get(user_key)
        if not user_entity:
            return jsonify({"Error": "User not found"}), 403

        # Ensure the requesting user is the owner of the resource
        if user_entity.get("sub") != user_sub:
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Delete the avatar from Google Cloud Storage
        avatar_blob_name = f"avatars/{user_id}"
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(avatar_blob_name)
        if not blob.exists():
            return jsonify({"Error": "Not found"}), 404

        blob.delete()

        # Return a 204 No Content response on success
        return '', 204

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    
@app.route('/courses', methods=['POST'])
def create_course():
    """Create a new course."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Fetch the requester entity to ensure they are an admin
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity or requesting_user_entity[0].get("role") != "admin":
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Parse and validate the request body
        content = request.get_json()
        required_fields = ["subject", "number", "title", "term", "instructor_id"]

        # Check if any required field is missing
        if not all(field in content for field in required_fields):
            return jsonify({"Error": "The request body is invalid"}), 400

        # Check if the instructor_id corresponds to an instructor in the Datastore
        instructor_key = client.key("user", content["instructor_id"])
        instructor_entity = client.get(instructor_key)
        if not instructor_entity or instructor_entity.get("role") != "instructor":
            return jsonify({"Error": "The request body is invalid"}), 400

        # Create a new course
        new_course = datastore.Entity(key=client.key("course"))
        new_course.update({
            "subject": content["subject"],
            "number": content["number"],
            "title": content["title"],
            "term": content["term"],
            "instructor_id": content["instructor_id"]
        })
        client.put(new_course)

        # Generate the response with the course details
        response = {
            "id": new_course.key.id,
            "subject": content["subject"],
            "number": content["number"],
            "title": content["title"],
            "term": content["term"],
            "instructor_id": content["instructor_id"],
            "self": f"{request.host_url}courses/{new_course.key.id}".rstrip('/')
        }

        return jsonify(response), 201

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    

@app.route('/courses', methods=['GET'])
def get_all_courses():
    """Get all courses with pagination."""
    try:
        # Retrieve query parameters for pagination
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 3))

        # Query courses from Datastore
        query = client.query(kind="course")
        query.order = ["subject"]  # Sort by subject
        courses = list(query.fetch(offset=offset, limit=limit))

        # Prepare the response
        course_list = []
        for course in courses:
            course_list.append({
                "id": course.key.id,
                "subject": course.get("subject"),
                "number": course.get("number"),
                "title": course.get("title"),
                "term": course.get("term"),
                "instructor_id": course.get("instructor_id"),
                "self": f"{request.host_url}courses/{course.key.id}".rstrip('/')
            })

        # Prepare the "next" link if there are more courses
        total_courses = len(list(client.query(kind="course").fetch()))
        next_url = None
        if offset + limit < total_courses:
            next_offset = offset + limit
            next_url = f"{request.host_url}courses?limit={limit}&offset={next_offset}".rstrip('/')

        # Create the response JSON
        response = {
            "courses": course_list
        }
        if next_url:
            response["next"] = next_url

        return jsonify(response), 200

    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500


@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by its ID."""
    try:
        # Fetch the course entity from Datastore
        course_key = client.key("course", course_id)
        course_entity = client.get(course_key)

        # If the course doesn't exist, return 404
        if not course_entity:
            return jsonify({"Error": "Not found"}), 404

        # Prepare the response
        response = {
            "id": course_entity.key.id,
            "subject": course_entity.get("subject"),
            "number": course_entity.get("number"),
            "title": course_entity.get("title"),
            "term": course_entity.get("term"),
            "instructor_id": course_entity.get("instructor_id"),
            "self": f"{request.host_url}courses/{course_entity.key.id}".rstrip('/')
        }

        return jsonify(response), 200

    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500


@app.route('/courses/<int:course_id>', methods=['PATCH'])
def update_course(course_id):
    """Perform a partial update on a course."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Ensure the requester is an admin
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity or requesting_user_entity[0].get("role") != "admin":
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Fetch the course entity from Datastore
        course_key = client.key("course", course_id)
        course_entity = client.get(course_key)

        # If the course doesn't exist, return 404
        if not course_entity:
            return jsonify({"Error": "Not found"}), 404

        # Parse the request body
        content = request.get_json()

        # Validate and apply updates
        if "instructor_id" in content:
            instructor_key = client.key("user", content["instructor_id"])
            instructor_entity = client.get(instructor_key)
            if not instructor_entity or instructor_entity.get("role") != "instructor":
                return jsonify({"Error": "The request body is invalid"}), 400
            course_entity["instructor_id"] = content["instructor_id"]

        if "subject" in content:
            course_entity["subject"] = content["subject"]

        if "number" in content:
            course_entity["number"] = content["number"]

        if "title" in content:
            course_entity["title"] = content["title"]

        if "term" in content:
            course_entity["term"] = content["term"]

        # Save the updated course entity
        client.put(course_entity)

        # Prepare the response
        response = {
            "id": course_entity.key.id,
            "subject": course_entity.get("subject"),
            "number": course_entity.get("number"),
            "title": course_entity.get("title"),
            "term": course_entity.get("term"),
            "instructor_id": course_entity.get("instructor_id"),
            "self": f"{request.host_url}courses/{course_entity.key.id}".rstrip('/')
        }

        return jsonify(response), 200

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete a course and remove all associated enrollments."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Ensure the requester is an admin
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity or requesting_user_entity[0].get("role") != "admin":
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Fetch the course entity from Datastore
        course_key = client.key("course", course_id)
        course_entity = client.get(course_key)

        # If the course doesn't exist, return 404
        if not course_entity:
            return jsonify({"Error": "Not found"}), 404

        # Fetch and remove student enrollments in this course
        enrollment_query = client.query(kind="enrollment")
        enrollment_query.add_filter("course_id", "=", course_id)
        enrollments = list(enrollment_query.fetch())
        for enrollment in enrollments:
            enrollment_key = enrollment.key
            client.delete(enrollment_key)

        # Remove the course entity
        client.delete(course_key)

        # Return 204 No Content
        return '', 204

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500


@app.route('/courses/<int:course_id>/students', methods=['PATCH'])
def update_enrollment(course_id):
    """Enroll and/or disenroll students from a course."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Parse and validate the request body
        content = request.get_json()
        if "add" not in content or "remove" not in content:
            return jsonify({"Error": "The request body is invalid"}), 400

        add_students = set(content["add"])
        remove_students = set(content["remove"])

        # Check for overlapping student IDs between add and remove
        if add_students & remove_students:
            return jsonify({"Error": "Enrollment data is invalid"}), 409

        # Ensure the requester is authorized (admin or instructor of the course)
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity:
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        requester = requesting_user_entity[0]
        if requester.get("role") != "admin":
            # Fetch the course to validate instructor ownership
            course_key = client.key("course", course_id)
            course_entity = client.get(course_key)
            if not course_entity:
                return jsonify({"Error": "Not found"}), 404
            if course_entity.get("instructor_id") != requester.key.id:
                return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Validate all student IDs in the `add` and `remove` arrays
        all_student_ids = add_students | remove_students
        valid_students_query = client.query(kind="user")
        valid_students_query.add_filter("role", "=", "student")
        valid_students = {entity.key.id for entity in valid_students_query.fetch()}

        if not all_student_ids.issubset(valid_students):
            return jsonify({"Error": "Enrollment data is invalid"}), 409

        # Fetch the course to update enrollment
        course_key = client.key("course", course_id)
        course_entity = client.get(course_key)

        if not course_entity:
            return jsonify({"Error": "Not found"}), 404

        # Update enrollment
        enrolled_students = set(course_entity.get("student_ids", []))
        enrolled_students.update(add_students)
        enrolled_students.difference_update(remove_students)

        # Save updated course entity
        course_entity["student_ids"] = list(enrolled_students)
        client.put(course_entity)

        # Return 200 on success
        return '', 200

    except AuthError as e:
        print("AuthError occurred:", e.error)
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({"Error": "Internal server error"}), 500
    

    
@app.route('/courses/<int:course_id>/students', methods=['GET'])
def get_enrollment(course_id):
    """Get the list of students enrolled in a course."""
    try:
        # Verify JWT
        payload = verify_jwt(request)
        user_sub = payload.get("sub")

        # Fetch the course entity
        course_key = client.key("course", course_id)
        course_entity = client.get(course_key)

        if not course_entity:
            return jsonify({"Error": "Not found"}), 404

        # Check authorization: admin or instructor of the course
        requesting_user_query = client.query(kind="user")
        requesting_user_query.add_filter("sub", "=", user_sub)
        requesting_user_entity = list(requesting_user_query.fetch())

        if not requesting_user_entity:
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        requester = requesting_user_entity[0]
        if requester.get("role") != "admin" and course_entity.get("instructor_id") != requester.key.id:
            print("Unauthorized access. User is neither admin nor instructor.")  # Debugging
            return jsonify({"Error": "You don't have permission on this resource"}), 403

        # Return list of enrolled students
        enrolled_students = course_entity.get("student_ids", [])
        return jsonify(enrolled_students), 200

    except AuthError as e:
        return jsonify({"Error": e.error}), e.status_code
    except Exception as e:
        return jsonify({"Error": "Internal server error"}), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
