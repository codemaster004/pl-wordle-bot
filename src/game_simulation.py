import json
import random
import redis
import psycopg2

from main import compare_word_with_key, does_word_fit, create_pattern_chart
from casual_game import Bot


# redis_sorted = redis.Redis(host='localhost', port=6379, db=0)
# redis_patterns = redis.Redis(host='localhost', port=6379, db=1)
# 
# conn = psycopg2.connect(
# 	host="localhost",
# 	port=5432,
# 	database="wordle",
# 	user="wordle",
# 	password="wordle"
# )
# cur = conn.cursor()


class SimulationGame(Bot):
	def __init__(self, words, answer_word, first_guess):
		super().__init__(words)
		self.answer = answer_word
		self.current_guess = first_guess
		self.game_won = False
	
	def pick_word(self):
		if self.current_guess is not None:
			return self.current_guess
		
		if len(self.words_available) == 1:
			return self.words_available[0]
		
		top_picks = self.choose_word()
		return top_picks[0][0]


if __name__ == '__main__':
	with open('data/answers.json') as file:
		answers = json.load(file)
	with open('data/words.json') as file:
		all_words = json.load(file)['slowa']
	
	OPENING_GUESS = 'soria'
	for answer in answers:
		simulation = SimulationGame(all_words, answer, OPENING_GUESS)
		while not simulation.game_won:
			simulation.pick_word()
