import time
import discord
import asyncio
import urllib.request
import sqlite3

import aiml
import datetime
from collections import OrderedDict
from datetime import datetime
import json
import request
import requests
from urllib.request import urlopen
import dataj
import os
from random import randint

client = discord.Client()
kernel = aiml.Kernel()


if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile = "bot_brain.brn")
else:
    kernel.bootstrap(learnFiles = "std-startup.xml",commands="LOAD AIML B")
    kernel.saveBrain("bot_brain.brn")
    kernel.setBotPredicate("name","Nyu")
def process_responce(msg):
    ##print (msg)
    bot_response = kernel.respond(msg)
    ##print (bot_response)
    return bot_response
new_con = sqlite3.connect("alarm.db")
con = sqlite3.connect("test.db")
nc = new_con.cursor()
c = con.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS reminder_db(_id INTEGER PRIMARY KEY,time_stamp INTEGER NOT NULL,des TEXT NOT NULL,tunnel INTEGER NOT NULL)''')
##print('name[0]')
nc.execute(
    '''CREATE TABLE IF NOT EXISTS alarm_db(_id INTEGER PRIMARY KEY,time_stamp TEXT NOT NULL,des TEXT NOT NULL,tunnel INTEGER NOT NULL,repeat TEXT NOT NULL,guild INTEGER NOT NULL)''')

con.commit()
new_con.commit()
new_con.close()
con.close()
@client.event
async def on_message(message):
            # we do not want the bot to reply to itself

            if message.content.startswith("$c"):
                pos = message.content.find('$c')
                msg = message.content[pos + 2:]
                y = process_responce(msg)
                if y == "":
                    y = 'Sorry I don\'t undertand that one'
                if msg.strip() == "LOAD AIML B":
                    y = 'Loading basic_chat.aiml...done (0.27 seconds)'
                chat = str(y).format(message)
                await client.send_message(message.channel, chat)

            elif message.content.startswith('$reminder_'):
                ##print(message.channel)
                des = "Reminder"
                raw = message.content[10:].split(':')
                try:
                    hh = raw[0].strip()
                    mm =raw[1].strip()
                except IndexError:
                    msg = 'Please write in correct format \n $reminder_HH:MM:Description of Reminder'.format(message)
                    await client.send_message(message.channel, msg)
                    return
                try:
                    des = raw[2].strip()
                except IndexError:
                    des = 'Reminder'

                a = int(time.time())
                ##print(hh)
                ##print(mm)

                if dataj.RepresentsInt(hh) and dataj.RepresentsInt(mm):
                    ##print("calk")
                    requried = a + int(hh) * 3600 + int(mm) * 60 - 15
                    ##print(requried)
                    dif = requried - a
                    if dif > 60:
                        dataj.add_reminder(requried, des,int(message.channel.id))
                    elif dif < 60:
                        msg = 'Reminder time passed !'.format(message)

                    msg = 'I will send reminder  after ' + hh + ' hours ' + mm + ' minute'.format(message)
                else:
                    msg = 'Please write in correct format \n $HH:MM:Description of Reminder'.format(message)

                await client.send_message(message.channel, msg)

            elif message.content.startswith('$help'):
                msg = '```1)About Me : $AboutMe\n\n2)For Chatting : $c[Your Chat Message]\n\n3)Setting Reminder : $reminder_HH:MM:Description\n\nExample for setting reminder in 4  hours 5 minutes \n  $reminder_04:05:Example\n\n4)$a_hug,$a_kiss,$a_slap,$a_(any thing you want Nyu to do for someone)``` '.format(message)
                await client.send_message(message.channel, msg)
            elif message.content.startswith('$a_'):
                ##print("hey")
                k=randint(0, 14)
                action=message.content.split(" ")[0][3:]

                # set the apikey and limit
                apikey = "xx-id"  # test value
                lmt = 15

                # load the user's anonymous ID from cookies or some other disk storage
                # anon_id = <from db/cookies>

                # ELSE - first time user, grab and store their the anonymous ID
                r = requests.get("https://api.tenor.com/v1/anonid?key=%s" % apikey)

                if r.status_code == 200:
                    anon_id = json.loads(r.content.decode('utf-8'))["anon_id"]
                    # store in db/cookies for re-use later
                else:
                    anon_id = ""

                # our test search
                search_term = "anime"+str(action)

                # get the top 8 GIFs for the search term using default locale of EN_US
                r = requests.get(
                    "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" % (
                    search_term, apikey, lmt, anon_id))

                if r.status_code == 200:
                    # load the GIFs using the urls for the smaller GIF sizes
                    top_8gifs = json.loads(r.content.decode('utf-8'))
                else:
                    top_8gifs = None

                # continue a similar pattern until the user makes a selection or starts a new search.
                rel = []
                for doc in top_8gifs['results']:
                    rel.append(doc['url'])
                try:
                    rl = rel[k]
                except IndexError:
                    rl = rel[0]
                if not message.mentions:
                    msg = 'Who are you trying to '+ action


                else:
                    msg = message.mentions[0].mention + ' you  got a '+action+' from '+ message.author.mention +'\n'+ rl.format(message)

                    ##print (rl)
                await client.send_message(message.channel, msg)
            elif message.content.startswith('$AboutMe'):
                embed = discord.Embed(title="About Me", url="https://discordbots.org/bot/426047120781344768",description="Nyu ", color=0xff00ff)
                embed.set_author(name="Nyu",url="https://discordbots.org/bot/426047120781344768", icon_url = "https://images.discordapp.net/avatars/426047120781344768/0402c327f7e5bbfdd86bcb33dc69417e.png?size=512")
                embed.set_thumbnail(url="https://images.discordapp.net/avatars/426047120781344768/0402c327f7e5bbfdd86bcb33dc69417e.png?size=512")
                embed.add_field(name='My Server', value = 'https://discord.gg/PVRjAcX', inline=False)
                embed.add_field(name='Help', value= '$help', inline = False)
                await client.send_message(message.channel, embed=embed)
            elif message.content.startswith('$alarm_'):
                msg = message.content[7:].strip().split(':')
                repeat='1234567'
                des = 'Alarm'
                try:
                    hh = msg[0]
                    mm = msg[1]
                except IndexError:
                    error_message = 'Please write in correct format \n ```$alarm_HH:MM:Name of Alarm:week day repeat(1=monday,..,7=Sunday (default every day repeat))```' \
                                    '\nNote:\nTime sahll be in 24h format and in UTC/GMT time zone for more information type ```$help```' \
                                    '\n UTC/GMT standard time right now is '+(str(datetime.utcnow().today())).split('.')[0]
                    await client.send_message(message.channel, error_message.format(message))
                    return
                try:
                    des = msg[2].strip()
                except IndexError:
                    des='Alarm'
                try:
                     repeat = msg[3].strip()
                except IndexError:
                     repeat='1234567'
                #Check Validity of INPUT
                ##print (hh + '\n' +  mm  + '\n' +  repeat)
                if dataj.RepresentsInt(hh)==False or dataj.RepresentsInt(mm)==False or dataj.RepresentsInt(repeat) == False:
                    await client.send_message(message.channel, 'Input Valid 24H time or check repeat(1-7)'.format(message))
                    return

                if int(hh) > 24 or int(mm) > 60:
                    await client.send_message(message.channel, 'Input Valid 24H time or check repeat(1-7)_*'.format(message))
                    return

                if len(hh) == 1:
                    hh = '0'+hh
                if len(mm) == 1:
                    mm = '0'+mm
                guild_id =message.channel.server.id

                #print('add')
                dataj.add_alarm(str(hh+':'+mm),des,int(message.channel.id),"".join(OrderedDict.fromkeys(repeat)),guild_id)


                await client.send_message(message.channel,'Your Alarm is successfully set for '+hh+':'+mm+' with repeation on '+ repeat+' weekdays where 1=Monday,...,7=Sunday and 0=repeat'.format(message))

            elif message.content.startswith('$list_alarm'):
                xx = int(message.channel.server.id)
                msg = dataj.return_l(xx)

                await client.send_message(message.channel , '```'+msg+'```'.format(message))
            elif message.content.startswith('$delete_alarm'):
                msg = message.content[13:]
                rm = int(msg.strip())
                if dataj.RepresentsInt(rm)==False:
                    await client.send_message(message.channel,'SEE ALARM ID of alarm by ```$list_alarm``` \nand delete by ```$delete_alarm [ALARM ID]```'.format(message))

                await client.send_message(message.channel, dataj.delete_repeat_alarm(rm,int(message.channel.server.id)).format(message))






async def my_background_task():
    await client.wait_until_ready()


    while not client.is_closed:
        now = time.time()
        now = int(now / 100)

        con = sqlite3.connect("test.db")

        c = con.cursor()
        for row in c.execute('SELECT time_stamp FROM reminder_db'):
            ##print(row)
            ##print("bg_tup")
            k = row[0] / 100
            ##print(k)
            ##print("tup")
            if int(k) == now:
                ##print("came here")
                c.execute('SELECT des FROM reminder_db WHERE time_stamp=?', (row))
                dss=c.fetchall()
                c.execute('SELECT _id FROM reminder_db WHERE time_stamp=?', (row))
                id = c.fetchall()
                c.execute('SELECT tunnel FROM reminder_db WHERE time_stamp=?', (row))
                channel_id= c.fetchall()

                embed = discord.Embed(title="Reminder", description=str(dss[0][0]), color=0x00ff00)
                embed.set_author(name='Nyu', icon_url='https://images.discordapp.net/avatars/426047120781344768/0402c327f7e5bbfdd86bcb33dc69417e.png?size=512')
                await client.send_message( discord.Object(id=str(channel_id[0][0])), embed=embed)
                dataj.delete_reminder(id[0][0])



        await asyncio.sleep(10)  # task runs every 10 seconds

async def my_background_task_2():
    await client.wait_until_ready()
    while not client.is_closed:
        alarm_now = (str(datetime.utcnow().today()).split('.')[0])[11:]
        alarm_now = alarm_now[:5]
        weekday = str(int(datetime.utcnow().today().weekday()) + 1)
        # #print(now)
        ncon = sqlite3.connect("alarm.db")
        nc = ncon.cursor()
        # #print (counter)
        for row_alarm in nc.execute('SELECT _id,time_stamp,des,tunnel,repeat FROM alarm_db'):
            if str(row_alarm[1]) == alarm_now and str(row_alarm[4]).find(weekday) != -1:
                dss = str(row_alarm[2])


                tunnel = int(row_alarm[3])
                #print("alarm test")
                embed = discord.Embed(title="Alarm", description=str(dss), color=0x00ff00)
                embed.set_author(name='Nyu',
                                 icon_url='https://images.discordapp.net/avatars/426047120781344768/0402c327f7e5bbfdd86bcb33dc69417e.png?size=512')
                embed.add_field(name='ALARM ID', value=str(row_alarm[0]), inline=True)
                embed.add_field(name='     Time(UTC/GMT)', value=str(row_alarm[1]), inline=True)
                await client.send_message(discord.Object(id=str(tunnel)), embed=embed)
        await asyncio.sleep(60)  # task runs every 60 seconds


@client.event
async def on_ready():
     print('Logged in as')
     print(client.user.name)
     print(client.user.id)
     game=discord.Game(name='$help')
     await client.change_presence(game=game)
     print('------')

client.loop.create_task(my_background_task())
client.loop.create_task(my_background_task_2())
client.run('xyz')
