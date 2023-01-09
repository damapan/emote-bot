import discord
import requests
import os
import json
from TwitchEmotes.findEmote import findEmote
from TwitchEmotes.saveImage import saveImage
from TwitchEmotes.getChannelEmotes import getEmoteSet, getChannelSet

intents = discord.Intents.default()
intents.message_content = True
intents.emojis = True

privateGuildID = open("Constants/privateGuildID.txt", "r").read()
botToken = open("Constants/botToken.txt","r").read()
botRequestHeader = {
                "Authorization": "Bot {0}".format(botToken)
            }

class TwitchChannelSelect(discord.ui.View):

    def __init__(self, channelName: list, emoteName: str):
        
        #create a discord view with a selection box
        self.emoteName = emoteName
        super().__init__()
        select = discord.ui.Select()

        #adds a list of potential channels to a select box
        self.emoteIDs = []
        potentialChannels = getChannelSet(channelName)
        for i in range(len(potentialChannels)):

            #gets the channel thumbnail
            saveImage(potentialChannels[i]['thumbnail_url'], f"{i}.png")
            emoteID = json.loads(client.postEmote(f'Thumbnail{i}',f"{i}.png",privateGuildID).text)['id']
            os.remove(f"{i}.png")

            #posts thumbnail as emote to a private server
            emote = requests.get("https://discord.com/api/v10/guilds/{0}/emojis/{1}".format(privateGuildID, emoteID), headers=botRequestHeader)
            emote = json.loads(emote.text)
            self.emoteIDs.append(emote['id'])

            #adds posted thumbnail to select box
            emote = discord.PartialEmoji(name=emote['name'] , id=emote['id'])
            select.add_option(label=potentialChannels[i]['name'], emoji=emote, value=str(potentialChannels[i]['id']))
            
        self.add_item(select)
        select.callback = self.selectCallback
    
    def deleteEmotes(self):
        '''
        delete all emotes created for the select box
        '''
        for id in self.emoteIDs:
            requests.delete("https://discord.com/api/v10/guilds/{0}/emojis/{1}".format(privateGuildID, id), headers=botRequestHeader)

    async def selectCallback(self, interaction: discord.Interaction):
        #stop view from recieving interactions
        self.stop()

        #Have user confirm their emote
        channelID = interaction.data['values'][0]
        await client.confirmTwitchEmote(interaction, emoteName=self.emoteName, channelID=channelID)

class EmoteConfirm(discord.ui.View):
    '''Create a discord view to confirm adding an emote to a server'''

    async def confirmCallback(self, interaction: discord.Interaction):
        #stops the view from receiving interactions
        self.stop()

        #adds Emote to server
        await client.addTwitchEmote(interaction, self.emoteName, self.emoteUrl)

    async def rejectCallback(self, interaction: discord.Interaction):
        #stops the view from receiving interactions
        self.stop()

        #Closing message
        await interaction.response.send_message("Have a nice day!", ephemeral=True)

    def __init__(self, emoteName, emoteUrl):
        self.emoteName = emoteName
        self.emoteUrl = emoteUrl
        super().__init__()

        #create a button to confirm adding emote
        confirmButton = discord.ui.Button(label="Go ahead", style= discord.ButtonStyle.green)
        confirmButton.callback = self.confirmCallback

        #create a button to reject adding emote
        rejectButton = discord.ui.Button(label="No thanks", style= discord.ButtonStyle.red)
        rejectButton.callback = self.rejectCallback

        self.add_item(confirmButton)
        self.add_item(rejectButton)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self,message: discord.Message):
        print('Message from {0.author}: {0.content}'.format(message))
        print(message.guild)

        #uncomment this when testing the bot
        #if message.content == "quit": exit()

    
    async def on_interaction(self,interaction: discord.Interaction):
        print(interaction)

        #check if interaction was a command
        if interaction.data.keys().__contains__('name'):
            print(interaction.data)

            #check if the command is to add twitch emote
            if interaction.data['name'] == 'addtwitchemote' : 
                #adds a global or channel emote

                if interaction.data['options'][0]['name'] == "global":
                    emoteName = interaction.data['options'][0]['options'][0]['value']
                    await self.confirmTwitchEmote(interaction, emoteName )

                if interaction.data['options'][0]['name'] == "fromchannel" :
                    channelName = interaction.data['options'][0]['options'][0]['value']
                    emoteName = interaction.data['options'][0]['options'][1]['value']
                    await self.confirmTwitchChannel(interaction, emoteName, channelName)


            
    async def confirmTwitchChannel(self,interaction: discord.Interaction, emoteName, channelName):
        '''Creates a message for the user to confirm their channel selection'''

        message = "Which channel would you like to get the emote from?\n"      
        v = TwitchChannelSelect(channelName, emoteName=emoteName)
        await interaction.response.send_message (message, view= v, ephemeral=True)    

        #deletes emotes created by the view for the selection
        v.deleteEmotes()


    async def confirmTwitchEmote(self, interaction: discord.Interaction, emoteName, channelID=None):
        '''creates a message for the user to confirm adding an emote\n
        for global emotes leave \'channelID\' as None
        '''

        emote = findEmote( getEmoteSet(channelID), emoteName)
        if emote is None:
            await interaction.response.send_message("I could not find a close match to what you were looking for", ephemeral=True)
            return


        #finds the twitch emote and creats a file object
        emoteUrl = emote['images']['url_4x']
        emoteName = emote['name']
        saveImage(emoteUrl,"confirmEmote.png")

        emoteConfirm = open("confirmEmote.png", "rb")
        f = discord.File(emoteConfirm)
        emoteConfirm.close()
        f.close()
        #sent a conformiation message with the emote
        v = EmoteConfirm(emoteName,emoteUrl)
        await interaction.response.send_message (f'The closest emote I could find was \"{emoteName}\", should I add it?', file=f, view= v, ephemeral=True)
        os.remove("confirmEmote.png")


    async def addTwitchEmote(self, interaction:discord.Interaction, emoteName, emoteUrl):
        '''Adds the twitch emote to the server'''
        saveImage(emoteUrl, "{0}.png".format(emoteName))

        response = self.postEmote(emoteName, f"{emoteName}.png", interaction.guild_id)
        if response.ok:
            await interaction.response.send_message("Done!", ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, something went wrong",ephemeral= True)
        os.remove("{0}.png".format(emoteName))
    
    def postEmote(self,emoteName, filePath:str, guildID):
        '''Post an emote to the guild with the provided ID'''

        with open(filePath, "rb") as e: 
            import base64

            binary_fc       = e.read()  # fc aka file_content
            base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
            ext     = filePath.split('.')[-1]
            dataurl = f'data:image/{ext};base64,{base64_utf8_str}'

            newEmote = {
                'name': emoteName,
                'image': dataurl}
            response = requests.post("https://discord.com/api/v10/guilds/{0}/emojis".format(guildID), headers=botRequestHeader,json=newEmote)     
        return response       


#running the bot
client = MyClient(intents=intents)
client.run(botToken)