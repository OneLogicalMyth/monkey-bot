import requests
import json
import time

class joke(object):

	def begin(self,command,user):

		response = None
		attachment = False

		if command == 'do my job':
			response = "<@" + user + "> :allo-unamused:"

		if command == 'deal with it':
			response = "<@" + user + "> just fucking deal with it!"

		if command == 'love you':
			response = "<@" + user + "> :allo-love:"

		if command == 'hack the planet':
			attachment = True
			response = [{"text": ":stuck_out_tongue_closed_eyes:","image_url": "https://media.giphy.com/media/14kdiJUblbWBXy/giphy.gif"}]

		if command == 'dad joke':
			res = requests.get("http://icanhazdadjoke.com", headers={"Accept":"application/json"})
			data = res.json()
			if data:
				response = data["joke"]

		if command == 'chuck norris':
			res = requests.get("https://api.icndb.com/jokes/random", headers={"Accept":"application/json"})
			data = res.json()
			if data:
				response = data["value"]["joke"].replace('&quot;','"')

		if command == 'trump':
				res = requests.get("https://api.tronalddump.io/random/quote", headers={"Accept":"application/hal+json"})
				data = res.json()
				if data:
					attachment = True
					response = [
							{
								"fallback": data['value'],
								"color": "#0062B9",
								"pretext": data['value'],
								"author_name": "Donald Trump",
								"title": data['_embedded']['source'][0]['url'],
								"title_link": data['_embedded']['source'][0]['url'],
								"footer": "via Twitter",
								"footer_icon": "https://1000logos.net/wp-content/uploads/2017/06/twitter-icon-2.png",
								"ts": time.mktime(time.strptime(data['appeared_at'], '%Y-%m-%dT%H:%M:%S'))
							}
						]

		return response, attachment
