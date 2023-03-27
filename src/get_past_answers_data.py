import requests
import json


main_url = 'https://betsapi.sraka.online/literalnies'

answers = []

for i in range(438):
	data = requests.get(f'{main_url}?_id={i}').json()
	answers.extend([answer['slowo'] for answer in data])

answers = list(set(answers))
print(answers)
# answers = [answer['slowo'] for answer in answers]

with open('data/answers.json', 'w') as file:
	json.dump(answers, file)
