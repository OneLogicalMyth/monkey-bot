import json
import os
import re
import sys
import time
import traceback

from slackclient import SlackClient
from plugins import *

# get root directory
file = sys.argv[0]
rootpath = os.path.dirname(file)


# load config file
with open('/etc/monkey-bot.conf', 'r') as f:
    config = json.load(f)


# instantiate Slack client
slack_client = SlackClient(config["SlackToken"])
RTM_READ_DELAY = 2  # 2 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


# starterbot's user ID in Slack: value is assigned after the bot starts up
bot_id = None


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            # if direct message you don't need @BotName
            if event["channel"].startswith('D') and not event["user"] == bot_id:
                return event["text"], event["channel"], event["user"]

            # Add Tools monitoring
            if event["channel"].startswith(config["Monitoring"]["channel"]) and not event["user"] == bot_id:
                return event["text"], event["channel"], event["user"]
            # look for @BotName in channel
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"], event["user"]

    return None, None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel, user):
    """
        Executes bot command if the command is known
    """
    response = None
    default_response = "ERROR"
    # grabs calling user info
    user_info = slack_client.api_call(
        "users.info",
        user=user
    )
    user_display_name = user_info["user"]["profile"]["display_name"]

    # debug
    print("The bot was mentioned in the channel '{}' by the user '{}' with the command of '{}'".format(channel, user, command.encode("utf-8")))

    # begin processing commands
    response, attachment_response = joke.joke().begin(command, user)

    # Handle Tool Channel links
    if channel.startswith(config["Monitoring"]["channel"]):
        github = GitBot.GitBot(config["Monitoring"]["github_api"], config["Monitoring"]["username"], config["Monitoring"]["password"], config["Monitoring"]["github_toolfile"])
        response = github.begin(command.encode("utf-8"), user)

    if command.startswith('port'):
        response, attachment_response = portlookup.portlookup().start(command, rootpath)

    if command.startswith('fitness meps'):
        z = myzone.myzone(config["myzone"]["username"], config["myzone"]["password"], config["myzone"]["nicknames"])
        response = z.leaderboard()

    if command.startswith('fitness leaderboard'):
        obj_fitbit = fitbitapi.fitbitapi(config["FitBit"]["CLIENT_ID"], config["FitBit"]["CLIENT_SECRET"], config["AppleHealth"]["api_key"], config["AppleHealth"]["api_url"])
        response = obj_fitbit.begin(command)
    if command.startswith('minecraft'):
        response, attachment_response = minecraft.minecraft().lookup(command, config["MineCraft"])
    # RTFM quick guide
    if command.startswith('rtfm'):
        response, attachment_response = rtfm.rtfm().lookup(command, rootpath)

    # CouchPotato Functionality
    if "couchPotato" in config:
        if command.startswith('movie'):
            couchPot = couchPotatoBot.couchPotato(config["CouchPotato"]["couchURL"], config["CouchPotato"]["couchApi"], config["whitelistedusers"])
            response = couchPot.begin(command, user)
    elif "radarr" in config:
        if command.startswith('movie'):
            radarr = radarrBot.radarr(config["radarr"]["radarrURL"], config["radarr"]["radarrApi"], config["whitelistedusers"])
            response = radarr.begin(command, user)
    if "sickRage" in config:
        if command.startswith('tv'):
            sickChill = sickPotatoBot.sickChill(config["sickRage"]["sickURL"], config["sickRage"]["sickApi"], config["whitelistedusers"])
            response, attachment_response = sickChill.begin(command, user)
    elif "sonarr" in config:
        if command.startswith('tv'):
            sonarr = sonarrBot.sonarr(config["sonarr"]["sonarrURL"], config["sonarr"]["sonarrApi"], config["whitelistedusers"])
            response, attachment_response = sonarr.begin(command, user)

    if command.startswith('plex'):
        plex = plexBot.plex(config["plex"]["plexURL"], config["plex"]["plexApi"], config["whitelistedusers"])
        response, attachment_response = plex.begin(command.encode("utf-8"), user)

    if command.startswith('stocks'):
        stock = stockBot.stocks(config["Stocks"]["stockURL"], config["Stocks"]["stockApi"])
        response, attachment_response = stock.begin(command.encode("utf-8"), user)

    # ensure the help command is always last
    if command.startswith('help') or response is None:
        attachment_response = True
        response = bothelp.help().get_help(command)

    # end processing commands

    # Sends the response back to the channel
    if attachment_response:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            as_user=True,
            attachments=response or default_response
        )
    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            as_user=True,
            unfurl_links=False,
            text=response or default_response
        )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False, auto_reconnect=True):
        print("Monkey Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            try:
                command, channel, user = parse_bot_commands(slack_client.rtm_read())
                if command:
                    command = command.lower()
                    handle_command(command, channel, user)
            except Exception as e:
                print(traceback.format_exc())
                print("ERROR: The command '" + str(command) + "' was sent by '" + str(user) + "' but failed, exception is '" + str(e) + "'")
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
