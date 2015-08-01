# Insert two people (POST is curl defuault?)
curl -d '[{"firstname":  "John", "lastname": "Lockwood"}]' -H 'Content-Type: application/json'  http://127.0.0.1:5000/api/people
