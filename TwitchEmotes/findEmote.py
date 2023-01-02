import json
import difflib
def findEmote (emoteSet: dict, emoteName: str) -> dict:
    '''
    find emote from an emote set and return its emote object (see twitch API docs)

    will return the closest match to emoteName if no exact match is found
    '''
    data = emoteSet["data"]
    possibleEmotes = []
    for emote in range(len(data)):
        possibleEmotes.append(data[emote]['name'])
        if data[emote]["name"] == emoteName:
            return(data[emote])

    closestMatch = difflib.get_close_matches(emoteName,possibleEmotes,1)
    if len(closestMatch) == 0: return None
    return findEmote(emoteSet,closestMatch[0])
    
    



