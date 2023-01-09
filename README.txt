BEFORE RUNNING THE BOT:
--------------------------------------------------------------------------------------------------------------------------------------------------------
The bot requires a folder named 'Constants' with 4 files in it to run

1. A twitch application id, to create a twitch application visit https://dev.twitch.tv/

2. A twtich user access token stored in a file name 'twitchOAuth.txt'
info on obtaining a user access token can be found on twitch's api documentation
https://dev.twitch.tv/docs/authentication/getting-tokens-oauth 

3. A private, unused discord server with its server id stored in a file named 'privateGuildID.txt'

4. A discord application with its bot token stored in a file named botToken.txt
For more information on creating a discord application and getting a bot token visit
https://discord.com/developers/applications
--------------------------------------------------------------------------------------------------------------------------------------------------------
The set of slash commands defined in the file 'makeTwitchEmote.json' needs to be uploaded to discord as well
for information on how to do this, visit 
https://discord.com/developers/docs/interactions/application-commands#create-global-application-command 

________________________________________________________________________________________________________________________________________________________

How to use the bot:
once all the files have been set up and the command has been uploaded, the bot can be added to a server using the link below
https://discord.com/api/oauth2/authorize?client_id={application id goes here}&permissions=1610992704&scope=bot%20applications.commands

The server will now have 2 slash commands added to it
"/addtwitchemote fromchannel"
This command needs a channel name and an emote name, and once excecuted the bot will find 3 possible channels the user can select from.
Once the user has selected a channel it will try to find an emote matching the name provided and get the user to confirm adding it to the server.

"/addtwitchemote global"
This command needs an emote name, and once excecuted the bot will try to find a global twitch emote matching the name provided
and get the user to confirm adding it to the server.