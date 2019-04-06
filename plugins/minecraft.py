import urllib, json
class minecraft(object):


        def lookup(self,command):
		message = 'Sorry I do not understand what your trying to search.'
                attachment = False

                if command.startswith('minecraft'):

			url = "https://mcapi.us/server/status?ip=monkey-bot.pentestmonkeys.tech"
			response = urllib.urlopen(url)
			data = json.loads(response.read())
			outputs = []
                        outputs.append({"short": False, "title": "MOTD", "value": "{}".format(data["motd"])})
                        outputs.append({"short": False, "title": "Online", "value": "{}".format(data["online"])})
			outputs.append({"short": False, "title": "Server", "value": "monkey-bot.dcrs.tech"})
                        outputs.append({"short": False, "title": "Current Players", "value": "{}".format(data["players"]["now"])})

                	message = [{"fallback": "blah", "pretext": "Current Pentest Monkey Server", "fields": outputs}]
			attachment = True




                return message, attachment

