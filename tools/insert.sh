# Insert two people (POST is curl defuault?)
curl -d '[{"firstname": "Denzel", "lastname": "Washington"}]' -H 'Content-Type: application/json'  http://127.0.0.1:5001/api/people
