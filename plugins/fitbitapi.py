from vendor.fitbit import fitbit
from vendor.fitbit import gather_keys_oauth2 as Oauth2
from vendor.fitbit.fitbit.iniHandler import ReadCredentials,ReadTokens,WriteTokens, SaveTokens
import datetime
import requests

# Built by https://github.com/itchannel
class fitbitapi(object):

	def __init__(self, CLIENT_ID, CLIENT_SECRET, apple_key):
		self.client_id = CLIENT_ID
		self.client_secret = CLIENT_SECRET
		self.apple_key = apple_key
	def begin(self,command):

		# make the command lower for all functions
		command = command.lower()
		response = None
		needs_help = False
		if command == 'fitness leaderboard':
			return self.getleaderboard()


	def getleaderboard(self):
		print "Getting leaderboard"
		#print self.client_id
		#, self.client_secret = ReadCredentials()
		self.ACCESS_TOKEN, self.REFRESH_TOKEN = ReadTokens()
		auth2_client = fitbit.Fitbit(self.client_id,self.client_secret, oauth2=True, access_token=self.ACCESS_TOKEN, refresh_token=self.REFRESH_TOKEN,refresh_cb=SaveTokens)

		yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
		friends = auth2_client.get_friends_leaderboardnew("7d")
		#print "IVE GOT FRIENDS"
		leaderboardlist = ""
		count = 0
		#googlefitapi = g_fit.googlefit().get_stats()
		results = []
		#Legacy API Code for v1.0 now retired we clean up on next code loop
		#for friend in friends["friends"]:
		#	if "averageDailySteps" in friend["user"]:
		#		result = [friend["user"]["displayName"],friend["user"]["averageDailySteps"]]
		#	else:
		#		result = [friend["user"]["displayName"],0]
		#	results.append(result)
		
		#new Fitbit API Code
		for friend in friends["included"]:
			for data in friends["data"]:
				if data["relationships"]["user"]["data"]["id"] == friend["id"]:
					if "attributes" in data:
						result=[friend["attributes"]["name"] + " (Fitbit)", data["attributes"]["step-summary"]]
					else:
						result=[friend["attributes"]["name"] + " (Fitbit)", 0]

			results.append(result)

		#result = [googlefitapi[0],googlefitapi[1]]
		apple_steve = ["Steve (iWatch)",round(self.getApple())];
		results.append(apple_steve)
		results.append(result)
		results = sorted(results,reverse=True, key=self.getKey)

		for result in results:
			count += 1
			leaderboardlist += str(count) + ". " + result[0] + " Steps: " + str(result[1]) + ".\n"
		#del googlefitapi

		return leaderboardlist



	def getApple(self):
		URL = "https://1mg.es/stats.php?func=get"
		r = requests.get(url = URL)
		print r.text
		return float(r.text)

	def getKey(self,item):
		return item[1]
