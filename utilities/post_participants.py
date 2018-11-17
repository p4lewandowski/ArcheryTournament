import requests

participants = {
"participants": "Piotr Podgorski 28;Adam A 29;Beata B 30"
}
r = requests.post("http://127.0.0.1:8000/participants/csv/"
                  ,json=participants)

print(r.status_code, r.reason)