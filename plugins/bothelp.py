

class help(object):

	def get_help(self,command):

		attachments = []

		if command.startswith('help fitness'):
			attachments.append(self.fitness())

		if command.startswith('help rtfm'):
			attachments.append(self.rtfm())

		if command.startswith('help minecraft'):
			attachments.append(self.minecraft())

		if command.startswith('help port'):
			attachments.append(self.port())

		if command.startswith('help all'):
			attachments.append(self.fitness())

		if command == 'help' or len(attachments) == 0:
			attachments.append({
			"fallback": "help all",
			"title": "Help Commands",
			"text": "The following help topics are available. Just do `help topic`.",
			"fields": [
				{
				"title": "Help Topics",
				"value": "fitness\nport\nrtfm\nminecraft\n\nYou can also do `help all`.",
				"short": True
				}			
			]
			})

		return attachments

	def port(self):

		return {
				"fallback": "You can try 'port 123'",
				"title": "Port Commands",
				"text": "The following commands can be used.",
				"fields": [
					{
					"title": "Port Number Lookup",
					"value": "port ###\n\nWhere ### equals the port number.",
					"short": True
					}
				]
				}

	def fitness(self):

		return {
				"fallback": "You can try 'fitness leaderboard'",
				"title": "Fitness Commands",
				"text": "The following commands can be used.",
				"fields": [
					{
					"title": "Pentest Monkeys Leaderboard",
					"value": "fitness leaderboard",
					"short": True
					}
				]
				}
	def rtfm(self):

		 return {
                                "fallback": "You can try 'rtfm rdp'",
                                "title": "rtfm Commands",
                                "text": "The following commands can be used.",
                                "fields": [
                                        {
                                        "title": "RTFM Lookup",
                                        "value": "rtfm value",
                                        "short": True
                                        }
                                ]
                                }

	def minecraft(self):

                 return {
                                "fallback": "You can try 'minecraft'",
                                "title": "minecraft Commands",
                                "text": "The following commands can be used.",
                                "fields": [
                                        {
                                        "title": "Server Lookup",
                                        "value": "minecraft",
                                        "short": True
                                        }
                                ]
                                }

