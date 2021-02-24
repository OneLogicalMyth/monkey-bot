# Installing the Bot
Visit the bot page for your Slack organisation at: https://YourSlackName.slack.com/apps/A0F7YS25R

Take a note of the bot API token and update the monkey-bot.py file with it.

Now supports Python3!
  
Install the requirements:
`pip install -r requirements.txt`


# Running the Bot from Python
As a non-root user run the bot with the following command:
`python monkey-bot.py`

# Running the Bot from Docker
Ensure you mount the config file so it can be accessed from docker as shown below
`docker run -v /etc/monkey-bot.conf:/etc/monkey-bot.conf imagename`
