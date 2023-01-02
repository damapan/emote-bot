import json
import requests
commandsUrl = "https://discord.com/api/v10/applications/968932806027776000/commands/1058699508462145576"
headers = {
    "Authorization": "Bot {0}".format(open("token.txt").read())
}

#response = requests.get("https://discord.com/api/v10/guilds/{0}".format("940333713764519967"), headers=headers)
with open("makeTwitchEmote.json") as command:
    response = requests.patch(url = commandsUrl, json= json.loads(command.read()), headers=headers)
print(response.text)

#blep id 1058699508462145576

