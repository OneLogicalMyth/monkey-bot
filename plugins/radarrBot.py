import requests
import json
import urllib
class radarr(object):

        def __init__(self, couchURL, apikey,whitelistedusers):
                self.couchURL = couchURL
                self.apiKey = apikey
		self.users = whitelistedusers
        def begin(self,command,user):
                # make the command lower for all functions
                command = command.lower()
                response = None
                needs_help = False
		if user not in self.users:
			return "This function is currently only avaliable to contributors to say thanks"
                if 'movies search' in command:
			return self.doSearch(command.replace("movies search", ""))
		elif 'movie search' in command:
			return self.doSearch(command.replace("movie search", ""))
		elif 'movie download' in command:
			return self.doDownload(command.replace("movie download", ""))
		elif 'movies download' in command:
                        return self.doDownload(command.replace("movies download", ""))
		elif 'movies wanted' in command:
			return self.doWanted(command.replace("movies wanted", ""))
		elif command[-1] == '?':
			return "No."
		else:
			return "Invalid Command"	


	def doSearch(self,searchstr):
		couch = radarrAPI(self.couchURL, self.apiKey)
		if searchstr == "":
			return "Invalid search string please specify a search term such as 'movies search iron man'"
		searchList = couch.searchMovies(searchstr)
		if searchList == "Error":
			return "No results found for the specified search"
		message = "I found the following movies:\n"
		for movie in searchList:
		    message += "<http://www.imdb.com/title/" + movie["imdb"] + "|" + movie["title"] + "(" + movie["year"]  +")" + "> Status: " + movie["status"]+ "   :id:" + movie["imdb"] + "\n"

		return message

	def doDownload(self,id):
		couch = radarrAPI(self.couchURL, self.apiKey)
		if id == "":
			return "Invalid ID"
		movieDownload = couch.downloadMovie(id)
		return movieDownload

	def doWanted(self,id):
		couch = radarrAPI(self.couchURL, self.apiKey)
		movieWanted = couch.getWanted()
		if movieWanted == False:
			return "Error occurred"
		message = "*Current Movies in the watch list:*\n"
		for movie in movieWanted:
			message += "* " + movie["title"] + "(" + movie["year"] +")\n"
		return message

class radarrAPI:
	

        def __init__(self, url, apikey):
            self.rooturl = url
            self.apikey = apikey

	def printapi(self):
		 return self.apikey

	def searchMovies(self,name):
		url = self.rooturl + '/api/v3/movie/lookup?apikey=' + self.apikey + '&term=' + urllib.quote_plus(name)
		request = requests.get(url)
		json_data = json.loads(request.text)
		if len(json_data) < 1:
			return "Error"
		else:
			movies = []
			for movie in json_data:
				imovie = {}
				# print "Movie Name: " + movie["titles"][0]
				imovie["title"] = movie["title"]
				if movie["folderName"] != "":
					#print "Already on Plex"
					imovie["status"] = "On Plex already"
				else :
					imovie["status"] = "Can be Added"
				if "imdbId" in movie:
					#print "ID: " + str(movie["imdb"])
					imovie["imdb"] = movie["imdbId"]
				else:
					imovie["imdb"] = "unknown"
				if "year" in movie:
					imovie["year"] = str(movie["year"])
				else:
					imovie["year"] = "0000"
				movies.append(imovie)
		return movies


	def getWanted(self):
                url = self.rooturl + '/api/v3/movie/id?' + self.apikey + '/media.list?type=movie&status=active'
                request = requests.get(url)
                json_data = json.loads(request.text)
                if json_data["success"] == False:
                        return False
                elif json_data["success"] == True:
			movies = []
			for movie in json_data["movies"]:
				imovie = {}
				imovie["title"] = movie["title"]
				imovie["year"] = str(movie["info"]["year"])
				movies.append(imovie)
                        return movies



	def downloadMovie(self,id):
		#url = self.rooturl + '/api/v3/movie/'+ urllib.quote_plus(id) + "?apikey=" + self.apikey
		url = self.rooturl + '/api/v3/movie/lookup?apikey=' + self.apikey + '&term=imdb:' + id
		request = requests.get(url)
		json_data = json.loads(request.text)
		#print(request.text)
		if len(json_data) < 1:
			return "Failed to download movie, is the ID valid?"
		else:
			postdata = {
				"title" : json_data[0]["title"],
				"tmdbId": json_data[0]["tmdbId"],
				"qualityProfileId": "6",
				"monitored": "true",
				"rootFolderPath" : "/movies/",
				"apiKey": self.apikey,
				"titleSlug": json_data[0]["titleSlug"],
				"images": json_data[0]["images"]

			}
			url = self.rooturl + '/api/v3/movie?apikey=' + self.apikey
			newHeaders = {'Content-type': 'application/json'}
			bob = json.dumps(postdata)
			request2 = requests.post(url, data=bob, headers=newHeaders)
			if request2.status_code == 400:
				return "Movie already in plex library or awaiting release"
			else:
				return "Movie added to wanted list, it will be downloaded as soon as a release becomes avaliable"
