import difflib
def findEmote (emoteSet: dict, emoteName: str) -> dict:
    '''
    find emote from an emote set and return its emote object (see twitch API docs)

    will return the closest match to emoteName if no exact match is found
    '''
    data = emoteSet["data"]
    #Make an array of any non matching names
    possibleEmotes = []
    for emote in range(len(data)):
        possibleEmotes.append(data[emote]['name'])
        #return if exact match was found
        if data[emote]["name"] == emoteName:
            return(data[emote])

    #find closest match and callback
    closestMatch = difflib.get_close_matches(emoteName,possibleEmotes,1,0.3)
    if len(closestMatch) == 0: return None
    return findEmote(emoteSet,closestMatch[0])
    
    



