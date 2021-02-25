import json
import requests


class userlookup(object):

    def get(self, token):

        out = requests.get('https://slack.com/api/users.list', params=token)
        final = out.json()
        userlookup = {}

        if 'members' in final:
            for member in final["members"]:
                if member["is_bot"] is False and member["deleted"] is False and member["id"] != "USLACKBOT":
                    userlookup[member["id"]] = {"email": member["profile"]["email"], "name": member["profile"]["real_name"]}

        return userlookup
