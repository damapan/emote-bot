import requests
import json

with open("Constants/twitchOAuth.txt", "r") as access:
    oAuth = access.read() 

with open("Constants/twitchClientID.txt", "r") as access:
    clientID = access.read() 

def getChannelID(channelName: str) -> int:
    '''
    Get the channel ID of a twtich channel by name
    '''

    #search for the channel
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
    #return its ID
    return (data[0]['id'])

def getEmoteSet(channelID: int) -> dict:
    '''Get the set of all emotes created by a channel
    '''

    #use global set if no channel ID is given
    url = 'https://api.twitch.tv/helix/chat/emotes/global'
    if channelID is not None:
        url = "https://api.twitch.tv/helix/chat/emotes?broadcaster_id=" + str(channelID)
    response = requests.get(
                    url = url ,
                    headers={
                        'Authorization': 'Bearer ' + oAuth,
                        'Client-Id': clientID,
                    })

    #return dict of emotes
    return json.loads(response.text)


def getChannelSet(channelName:str, rangeLength: int=3):
    '''Get the first 'rangeLength' channels 
    that come up when 'channelName' is searched for on twitch'''

    #search for channels by name
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

    #return the first "rangeLength" results
    return channels


#test script
if __name__ == '__main__':
    print(getEmoteSet(36177185))
    print(getChannelSet("itronmouse"))
