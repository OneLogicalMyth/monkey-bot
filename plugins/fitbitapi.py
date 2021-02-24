from vendor.fitbit import gather_keys_oauth2 as Oauth2
from vendor.fitbit.iniHandler import ReadCredentials,ReadTokens,WriteTokens, SaveTokens
import datetime
import requests

# Built by https://github.com/itchannel
class fitbitapi(object):

	def __init__(self, CLIENT_ID, CLIENT_SECRET, api_key, api_url):
		self.client_id = CLIENT_ID
		self.client_secret = CLIENT_SECRET
		self.api_key = api_key
		self.api_url = api_url
	def begin(self,command):

		# make the command lower for all functions
		command = command.lower()
		response = None
		needs_help = False
		if command == 'fitness leaderboard':
			return self.getleaderboard()


	def getleaderboard(self):
		print("Getting leaderboard")
		#print self.client_id
		#, self.client_secret = ReadCredentials()
		self.ACCESS_TOKEN, self.REFRESH_TOKEN = ReadTokens()
		auth2_client = fitbit.Fitbit(self.client_id,self.client_secret, oauth2=True, access_token=self.ACCESS_TOKEN, refresh_token=self.REFRESH_TOKEN,refresh_cb=SaveTokens)

		yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
		friends = auth2_client.get_friends_leaderboardnew("7d")
		#print "IVE GOT FRIENDS"
		leaderboardlist = "*Step Count (last 7 days)*\n"
		count = 0
		#googlefitapi = g_fit.googlefit().get_stats()
		results = []

		
		#new Fitbit API Code
		for friend in friends["included"]:
			for data in friends["data"]:
				if data["relationships"]["user"]["data"]["id"] == friend["id"]:
					if "attributes" in data:
						result=[friend["attributes"]["name"] + " (Fitbit)", data["attributes"]["step-summary"]]
						results.append(result)
					#Uncomment to add users with 0 steps on fitbit
					#else:
						#result=[friend["attributes"]["name"] + " (Fitbit)", 0]
						#results.append(result)

			

		#New Apple Health integration, requires a seperate IOS sync application and API endpoint (Code coming soon)
		apple_steve = self.getApple()
		for key, value in apple_steve.iteritems():
			combined = [key + " (iWatch)",round(float(value))]
			results.append(combined)

		results = sorted(results,reverse=True, key=self.getKey)

		for result in results:
			count += 1
			leaderboardlist += str(count) + ". " + result[0] + " Steps: " + str(result[1]) + ".\n"

		return leaderboardlist



	def getApple(self):
		#Function to return the Apple stats from the custom API
		URL = "https://%s?func=get" % self.api_url
		r = requests.get(url = URL)
		results = r.json()
		return results

	def getKey(self,item):
		return item[1]
