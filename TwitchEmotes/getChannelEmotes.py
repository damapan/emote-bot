import requests
import json

with open("Constants/twitchOAuth.txt", "r") as access:
    oAuth = access.read() 

with open("Constants/twitchClientID.txt", "r") as access:
    clientID = access.read() 

def getChannelID(channelName: str) -> int:
    response = requests.get(
                    url = "https://api.twitch.tv/helix/search/channels",
                    headers={
                        'Authorization': 'Bearer ' + oAuth,
                        'Client-Id': clientID,
                    },
                    params={
                        'query': channelName
                    })

    data = json.loads(response.text)['data']
    return (data[0]['id'])

def getEmoteSet(channelID: int) -> dict:
    url = 'https://api.twitch.tv/helix/chat/emotes/global'
    if channelID is not None:
        url = "https://api.twitch.tv/helix/chat/emotes?broadcaster_id=" + str(channelID)
    response = requests.get(
                    url = url ,
                    headers={
                        'Authorization': 'Bearer ' + oAuth,
                        'Client-Id': clientID,
                    })
    return json.loads(response.text)


def getChannelSet(channelName:str, rangeLength: int=3):
    response = requests.get(
                url = "https://api.twitch.tv/helix/search/channels",
                headers={
                    'Authorization': 'Bearer ' + oAuth,
                    'Client-Id': clientID,
                },
                params={
                    'query': channelName
                })

    data = json.loads(response.text)['data']
    channels = []
    for i in range(min(rangeLength, len(data))):
        channels.append( {'name': data[i]['display_name'], 'thumbnail_url': data[i]['thumbnail_url'], 'id': data[i]['id'] } )
    return channels


#test script
if __name__ == '__main__':
    print(getEmoteSet(36177185))
    print(getChannelSet("itronmouse"))
