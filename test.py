from google.cloud import datastore

# Initialize client without namespace
client = datastore.Client()

print("Datastore Client Project:", client.project)
print("Datastore Client Namespace:", client.namespace)


def list_users():
    query = client.query(kind="user")
    users = list(query.fetch())
    if not users:
        print("No users found!")
    for user in users:
        print("User:", user)

list_users()
