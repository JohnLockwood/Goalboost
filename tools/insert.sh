# Insert two people (POST is curl defuault?)
curl -d '[{"firstname": "George", "lastname": "Clooney"}, {"firstname":  "Margaret", "lastname": "Thatcher"}]' -H 'Content-Type: application/json'  http://127.0.0.1:5001/api/people
