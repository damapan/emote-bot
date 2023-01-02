import requests

def saveImage(imageURL: str  , fileName: str) -> None:
    '''
    Fetch and image from 'imageURL' and saves it to 'fileName' \n
    Include file format and filepath in 'fileName' \n
    E.x fileName = "path/image name.jpg"
    '''
    #fetch image from url
    response = requests.get(imageURL, stream=True)

    #verify retrieval
    if not response.ok:
        print(response)
        return

    #make file
    with open(fileName, "wb") as image:
        #write image to file 
        for block in response.iter_content(1):
            if not block:
                break
            image.write(block)



#Test method
if __name__ == "__main__":
    saveImage("https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_665235901db747b1bd395a5f1c0ab8a9/static/light/3.0" , "lechon.png")