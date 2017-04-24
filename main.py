# python bot
"""
?
desc
?

"""
import telebot
import config

from flask import Flask

app = Flask(__name__)
bot = telebot.TeleBot(config.token)
  
def log(message, answer):
	print("\n -----")
	from datetime import datetime
	print(datetime.now())
	print("""Message from {0} {1} (id = {2}).
		\nText: {3}.""".format(message.from_user.first_name, 
		message.from_user.last_name, 
		str(message.from_user.id), 
		message.text))
	print("Answer: {0}".format(answer))

@bot.message_handler(commands=['start'])
def handle_start(message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('/start', '/stop')
        user_markup.row('photo', 'audio', 'sticker')
        bot.send_message(message.from_user.id, "Welcome!", reply_markup = user_markup)
        
@bot.message_handler(commands=['stop'])
def handle_stop(message):
        hide_markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "..", reply_markup = hide_markup)


@bot.message_handler(commands=['help'])
def handle_command(message):
	bot.send_message(message.chat.id, "Let's greet each other!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
	import re
	answer = "Did not compute!"
	if message.text.lower() == 'hello':
		answer = "Hello to you, too!"
		bot.send_message(message.chat.id, answer)
	elif re.match('http', message.text.lower()):
		import urllib.request
		import html5lib
		from bs4 import BeautifulSoup
		answer = "Getting images"
		bot.send_message(message.chat.id, answer)
		page = urllib.request.urlopen(message.text.lower()).read()
		soup = BeautifulSoup(page, "html5lib")
		soup.prettify()
		i = 1
		for img in soup.find_all('img'):
			src = str(img.get('src'))
			if src and src != 'None':
				print(src)
				if not re.match('http', src):
					from urllib.parse import urlparse
					parsed_uri = urlparse(message.text.lower())
					domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
					src = "{0}{1}".format(domain, src)
				name = "img/{0}.jpg".format(i)
				i += 1
				f = open(name,'wb')
				f.write(urllib.request.urlopen(src).read())
				f.close()
				bot.send_chat_action(message.chat.id, 'upload_photo')
				img = open(name, 'rb')
				bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
				img.close()		
	else:
		bot.send_message(message.chat.id, answer)
	log(message, answer)
		
bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    app.run()








