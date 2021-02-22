import requests
import json
import urllib

class stocks(object):
	
	def __init__(self, stockURL, apikey):
		self.stockURL = stockURL
		self.apiKey = apikey
	
	def begin(self,command,user):
		# make the command lower for all functions
		command = command.lower()
		response = None
		needs_help = False
		if 'stocks news' in command:
			return self.getNews(command.replace("stocks news ", ""))
		elif 'tv latest' in command:
			return self.getLatest()
		elif 'tv search' in command:
			return self.getSearch(command.replace("tv search", ""))
		elif 'tv download' in command:
			return self.getDownload(command.replace("tv download", ""))
		elif command[-1] == '?':
			return "No.", False
		else:
			return "Invalid Command", False


	def getNews(self, searchstr):
		stock = stockAPI(self.stockURL, self.apiKey, searchstr)
		news = stock.News()
		newslist = []
		for newsitem in news:
			fields = []
			fields.append({"short": False, "title": "Headline" , "value": newsitem["headline"]})
			fields.append({"short": False, "title": "Summary" , "value": newsitem["summary"]})
			fields.append({"short": False, "title": "URL" , "value": newsitem["url"]})
			newslist.append({"fallback": "Stock News", "fields": fields})
		message = newslist
		return message, True



class stockAPI:

	def __init__(self, url, apikey, searchstr):
		self.url = url
		self.apikey = apikey
		self.searchstr = searchstr

	def News(self):
		if self.searchstr:
			url = self.url + "news?category=" + self.searchstr + "&token=" + self.apikey
		else:
			url = self.url + "news?category=general&token=" + self.apikey
		print(url)
		r = requests.get(url)
		json_data = json.loads(r.text)
		news = []
		count = 0
		for newsitem in json_data:
			if count == 5:
				break
			item = {}
			item["headline"] = newsitem["headline"]
			item["url"] = newsitem["url"]
			item["summary"] = newsitem["summary"]
			news.append(item)
			count+= 1
		return news
