import requests

url = "http://localhost:8000/ner"

data = {
    "text": "Kaspersky   believes  both  Shamoon  and  StoneDrill  groups  are  aligned  in  their  interests  ,  but  are  two  separate  actors  ,  which  might  also  indicate  two  different  groups  working  together."
}

response = requests.post(url, json=data)
print(response.text)