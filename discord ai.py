import os
import discord
import requests
import json
import random
from replit import db


client = discord.Client()

news_words = ["Whats new?","whats new","news","whats going on in the world","tell me something new","tell me some news"]

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing","covid","corona","virus"]

starter_encouragements = ["Cheer up! It'll all be okay before you know it.","Hang in there","Stay strong! You will get through this!"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_nnews():
  response = requests.get("https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=497e897d62a54f2bbb3e826a323f1ae7")
  json_data1 = response.json()
  nnews = json_data1["articles"]
  nnews = [i["url"] for i in nnews]
  nnews = '\n'.join(nnews)
  return(nnews)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))

@client.event
async def on_message(mess):
  if mess.author == client.user:
    return

  if any(wrd in mess.content for wrd in news_words):
    nnews = get_nnews()
    await mess.channel.send(nnews)

  if mess.content.startswith('$inspire'):
    quote = get_quote()
    await mess.channel.send(quote)
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in mess.content for word in sad_words):
      await mess.channel.send(random.choice(options))

  if mess.content.startswith('$hello'):
    await mess.channel.send('Hello there!')

  if mess.content.startswith("$new"):
    encouraging_message = mess.content.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await mess.channel.send("New encouraging message added.")

  if mess.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(mess.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await mess.channel.send(encouragements)

  if mess.content.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await mess.channel.send(encouragements)

  if mess.content.startswith("$responding"):
    value = mess.content.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await mess.channel.send("Responding is on.")

    else:
      db["responding"] = False
      await mess.channel.send("Responding is off.")


my_secret = os.environ.get("TOKEN")
client.run(my_secret)