import requests

participants = {
"participants": "Piotr Podgorski 28;"
                "Adam A 29;"
                "Beata B 30;"
                "Celina C 10;"
                "Dominika D 12;"
                "Ela E 14;"
                "Fryderyk F 22;"
                "Gabi G 23;"
                "Henryk H 21;"
                "Iga I 11;"
                "Jola J 0;"
                "Kamil K 4;"
                "Lidia L 11;"
                "Monika m 22;"
                "Nikola N 12;"
                "Ola O 1;"
}
r = requests.post("http://127.0.0.1:8000/participants/csv/"
                  ,json=participants)

print(r.status_code, r.reason)