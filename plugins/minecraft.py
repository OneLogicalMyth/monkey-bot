import urllib, json
class minecraft(object):


        def lookup(self,command):
		message = 'Sorry I do not understand what your trying to search.'
                attachment = False

                if command.startswith('minecraft'):

			url = "https://api.mcsrvstat.us/2/5.196.123.114"
			response = urllib.urlopen(url)
			data = json.loads(response.read())
			outputs = []
                        outputs.append({"short": False, "title": "MOTD", "value": "{}".format(data["motd"]["clean"][0])})
                        outputs.append({"short": False, "title": "Online", "value": "{}".format(data["online"])})
			outputs.append({"short": False, "title": "Server", "value": "monkey-bot.dcrs.tech:25565"})
			players = ""
			if "list" in data["players"]:
				for player in data["players"]["list"]:
					players += "{}\n".format(player)
                        	outputs.append({"short": False, "title": "Current Players", "value": "{}".format(players)})
			else:
				outputs.append({"short": False, "title": "Current Players", "value": "No Players Connected"})
                	message = [{"fallback": "Minecraft Update", "pretext": "Current Pentest Monkey Server", "fields": outputs}]
			attachment = True




                return message, attachment

