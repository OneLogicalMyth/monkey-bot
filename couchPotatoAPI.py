import requests
import json
import urllib


class couchPotato:


	def __init__(self, url, apikey):
		self.rooturl = url
		self.apikey = apikey





	def printapi(self):

		return self.apikey



	def searchMovies(self,name):
		url = self.rooturl + '/api/' + self.apikey + '/search?q=' + urllib.quote_plus(name)
		print url
		request = requests.get(url)
		json_data = json.loads(request.text)
		movies = []
		for movie in json_data["movies"]:
			imovie = {}
			print "Movie Name: " + movie["titles"][0]
			imovie["title"] = movie["titles"][0]
			if movie["in_library"]:
				print "Allready on Plex"
				imovie["status"] = "onplex"
			elif movie["in_wanted"]:
				print movie["in_wanted"]["status"]
				imovie["status"] = "On Wanted List"
			else :
				imovie["status"] = "Can be Added"
			if "imdb" in movie:
				print "ID: " + str(movie["imdb"])
				imovie["imdb"] = movie["imdb"]

			movies.append(imovie)
		return movies










