# server-management
A simple ticket bot which I use to manage my service server.

# Instructions:
Make an .env file and insert the following:
TOKEN: The discord bot application token.
M_URL: MongoDB URL
For e.g:
TOKEN = "abcdefghijk"
M_URL = "mongodb://localhost:27017"

-> In the config file, change the following:
--> owner_id: Server owner user ID.
--> ticketcat_id: The category where all the ticket channels will be stored.
--> review_id: The channel where all the reviews will be going.
DO NOT EDIT THE cogs VARIABLE IF YOU DON'T KNOW WHAT YOU ARE DOING!
