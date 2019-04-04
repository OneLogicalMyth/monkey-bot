from vendor.fitbit import fitbit
from vendor.fitbit import gather_keys_oauth2 as Oauth2
import datetime

# Built by https://github.com/itchannel
class fitbitapi(object):

	def begin(self,command):

		# make the command lower for all functions
		command = command.lower()
		response = None
		needs_help = False

		if command == 'fitness leaderboard':
			return self.getleaderboard()


	def getleaderboard(self):

		print config.FitBit.CLIENT_ID
		#self.client_id = config.FitBit.CLIENT_ID
		#print self.client_id
		#, self.client_secret = ReadCredentials()
		self.ACCESS_TOKEN, self.REFRESH_TOKEN = ReadTokens()
		auth2_client = fitbit.Fitbit(self.CLIENT_ID,self.CLIENT_SECRET, oauth2=True, access_token=self.ACCESS_TOKEN, refresh_token=self.REFRESH_TOKEN,refresh_cb=SaveTokens)

		yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))
		friends = auth2_client.get_friends_leaderboard("7d")

		#print friends
		leaderboardlist = ""
		count = 0
		#googlefitapi = g_fit.googlefit().get_stats()
		results = []

		for friend in friends["friends"]:
			result = [friend["user"]["displayName"],friend["summary"]["steps"]]
			results.append(result)

		result = [googlefitapi[0],googlefitapi[1]]
		results.append(result)
		results = sorted(results,reverse=True, key=self.getKey)

		for result in results:
			count += 1
			leaderboardlist += str(count) + ". " + result[0] + " Steps: " + str(result[1]) + ".\n"
		del googlefitapi

		return leaderboardlist

	def getKey(self,item):
		return item[1]
