import urllib, json
class minecraft(object):

	def getMinecraftData(self,server):
		url = "https://api.mcsrvstat.us/2/" + server
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		outputs = []
		outputs.append({"short": False, "title": "MOTD", "value": "{}".format(data["motd"]["clean"][0])})
		outputs.append({"short": False, "title": "Online", "value": "{}".format(data["online"])})
		outputs.append({"short": False, "title": "Server", "value": server})
		players = ""

		if "list" in data["players"]:
			for player in data["players"]["list"]:
				players += "{}\n".format(player)
			outputs.append({"short": False, "title": "Current Players", "value": "{}".format(players)})
		else:
			outputs.append({"short": False, "title": "Current Players", "value": "No Players Connected"})

		return [{"fallback": "Minecraft Update", "fields": outputs}]

        def lookup(self,command,servers):
		message = 'Sorry I do not understand what your trying to search.'
                attachment = False

                if command.startswith('minecraft'):

			message = []
			for server in servers:
				message += self.getMinecraftData(server)
			attachment = True

                return message, attachment

