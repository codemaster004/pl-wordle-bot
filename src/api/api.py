from flask import Flask, render_template, request
import json

from casual_game import Bot

app = Flask(__name__)


@app.route('/')
def index():
	global bot, all_words
	bot = None
	bot = Bot(all_words)
	bot.load_word_lists()
	return render_template('game.html')


@app.route('/predictions', methods=['GET'])
def data():
	word = ''.join(json.loads(request.args.get('word')))
	temp_pattern = json.loads(request.args.get('pattern'))
	pattern = tuple([int(n) for n in temp_pattern])
	print(word, pattern)
	possible_words, n_words, best_words = bot.play_word(word, pattern)
	return json.dumps({'possible': possible_words, 'possibleCount': n_words, 'bestWords': best_words})


if __name__ == '__main__':
	with open('/Users/filip/Developer/Python/WordleAlg/src/data/words.json') as file:
		data = json.load(file)
		all_words = data['slowa']

	bot = Bot(all_words)
	bot.load_word_lists()
	bot.choose_word()
	app.run(debug=True)
