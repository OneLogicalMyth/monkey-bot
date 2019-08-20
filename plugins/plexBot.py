import requests
import json
import urllib


class plex(object):
    
    def __init__(self, plexURL, apikey,whitelistedusers):
        self.plexURL = plexURL
        self.apiKey = apikey
        self.users = whitelistedusers
        
    def begin(self,command,user):
        # make the command lower for all functions
        command = command.lower()
        response = None
        needs_help = False
        print command
        #if user not in self.users:
		    #return "This function is currently only avaliable to contributors to say thanks"
        if 'plex watching' in command:
		    return self.getWatching()
        elif 'plex popular' in command:
		    return self.getPopular()
        elif 'plex library' in command:
		    return self.getLibraryStats()
        elif command[-1] == '?':
		    return "No."
        else:
		    return "Invalid Command"


    def getWatching(self):
        plex = plexAPI(self.plexURL, self.apiKey)
        tvtoday = plex.Watching()
        showlist = []
        for show in tvtoday:
            fields = []
            #Removed user integration due to emails being shown fields.append({"short": False, "title": show["showname"] , "value": "*Library:* " + show["type"] + "\n*User:* " + show["user"] + "\n*Current Quality*: " + show["quality_profile"] })
            fields.append({"short": False, "title": show["showname"] , "value": "*Library:* " + show["type"] + "\n*Current Quality*: " + show["quality_profile"] })
            showlist.append({"fallback": "blah", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True

    def getLibraryStats(self):
        plex = plexAPI(self.plexURL, self.apiKey)
        stats = plex.LibraryStats()
        showlist = []
        for show in stats:
            fields = []
            if show["section_type"] == "show":
                fields.append({"short": False, "title": show["section_name"] , "value": "*Type:* " + show["section_type"] + "\n*Show Count:* " + show["count"] + "\n*Episode Count:* " + show["child_count"] })
            elif show["section_type"] == "photo":
                fields.append({"short": False, "title": show["section_name"] , "value": "*Type:* " + show["section_type"] + "\n*Album Count:* " + show["count"] + "\n*Photo Count:* " + show["parent_count"] })
            else:
                fields.append({"short": False, "title": show["section_name"] , "value": "*Type:* " + show["section_type"] + "\n*Item Count:* " + show["count"] })
            showlist.append({"fallback": "blah", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True

    def getPopular(self):
        plex = plexAPI(self.plexURL, self.apiKey)
        movies, tvshows = plex.Popular()
        showlist = []
        fields = []
        for movie in movies:         
            fields.append({"short": False, "title": movie["title"] , "value": "Users Viewed: " + movie["users_watched"] })
        showlist.append({"fallback": "blah", "pretext": "Top Movies Viewed on Plex (Last 30 days)", "fields": fields})
        fields = []
        for show in tvshows:         
            fields.append({"short": False, "title": show["title"] , "value": "Users Viewed: " + show["users_watched"] })
        showlist.append({"fallback": "blah", "pretext": "Top TV Shows Viewed on Plex (Last 30 days)", "fields": fields})
        #message = [{"fallback": "blah", "pretext": "The following shows will download today:", "fields": showlist}]
        message = showlist
        return message, True



class plexAPI:

    def __init__(self, url, apikey):
        self.rooturl = url
        self.apikey = apikey


    def Watching(self):
        url = self.rooturl + '/api/v2?apikey=' + self.apikey + '&cmd=get_activity'
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data["response"]["result"] !="success":
            return False
        elif json_data["response"]["result"] == "success":
            shows = []
            for show in json_data["response"]["data"]["sessions"]:
                print show
                ishow = {}
                ishow["showname"] = show["full_title"]
                ishow["type"] = show["library_name"]
                ishow["user"] = show["friendly_name"]
                ishow["quality_profile"] = show["quality_profile"]
                shows.append(ishow)
            return shows


    def LibraryStats(self):
        url = self.rooturl + '/api/v2?apikey=' + self.apikey + '&cmd=get_libraries'
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data["response"]["result"] !="success":
            return False
        elif json_data["response"]["result"] == "success":
            shows = []
            for library in json_data["response"]["data"]:
                print library
                ishow = {}
                ishow["section_name"] = library["section_name"]
                ishow["section_type"] = library["section_type"]
                ishow["count"] = library["count"]
                if library["section_type"] == "show":
                    ishow["child_count"] = library["child_count"]
                elif library["section_type"] == "photo":
                    ishow["parent_count"] = library["parent_count"]

                shows.append(ishow)
            return shows

    def Popular(self):
        url = self.rooturl + '/api/v2?apikey=' + self.apikey + '&cmd=get_home_stats'
        request = requests.get(url)
        json_data = json.loads(request.text)
        if json_data["response"]["result"] !="success":
            return False
        elif json_data["response"]["result"] == "success":
            popmovies = []
            poptvshows = []
            for show in json_data["response"]["data"]:
                if show["stat_id"] == "popular_movies":
                    
                    for movie in show["rows"]:
                        imovie = {}
                        imovie["title"] = movie["title"]
                        imovie["users_watched"] = str(movie["users_watched"])
                        popmovies.append(imovie)

                elif show["stat_id"] == "popular_tv":
                    for item in show["rows"]:
                        ishow = {}
                        ishow["title"] = item["title"]
                        ishow["users_watched"] = str(item["users_watched"])
                        poptvshows.append(ishow)

            return popmovies, poptvshows