import discord
from discord.ext import commands
import calendar
import time
import datetime
import asyncio
import sqlite3
import re
import os
from bot_token import token
import help_str
import flask
import keep_alive
import pytz
from Mk import MK

# © Copyright 2021 - 2022, Jake34959, All Rights Reserved.

prefix = "."
maker_name = ("Jake From State Farm")
maker_id = #VARIABLE REDACTED

bot = commands.Bot(command_prefix=prefix,intents=discord.Intents.all(),description='Bot')
bot.remove_command('help')  # removes default help command!
# Const attributes
bot.prefix = prefix
bot.db = 'Mods.db'
bot.print_log = "print_log.txt"
bot.message_log = "message_log.txt"
bot.message_logxl = "message_logxl.txt"
con=sqlite3.connect(bot.db)
cur=con.cursor()
#Rewrite Start : THU FEB 3 2022, 05:34:50
#Rewrite Done : SUN MAR 6 2022, 17:16:56
#REWRITTEN : 21 / 21
#1 | Done |
def write_to_db():
    con.commit()
#2 | Done |
def connect_to_db():
    con=sqlite3.connect(bot.db)
    cur=con.cursor()
#3 | Done |
@bot.event
async def on_ready():
    maker = (bot.get_user(maker_id))
    print("Logged in as")
    print(bot.user.name)
    print ("Running Bot From State Farm MK{}".format(MK))
    connect_to_db()
    print("Database connected.")
    await maker.send(content="Logged in as" + "\n{}".format(bot.user.name) +
    "\nRunning Bot From State Farm MK{}".format(MK) + "\nData loaded successfully.")
    time.sleep(2)
    print("We are fully operational sir.")
    await maker.send(content="We are fully operational sir.")
#4 | Done |
def get_timeStamp() -> str:
    return datetime.datetime.fromtimestamp(time.time(), pytz.timezone("Canada/Pacific")).strftime('%Y-%m-%d @ %H:%M:%S')
#5 | Done |
def cmdcheck(ctx, memberid, guild):
    connect_to_db()
    c= cur.execute("Select * from mods")
    embed = None
    auth_users=[]
    for q in c:
        if q[1]:
            auth_users.append(q[1])
    if memberid not in auth_users:
        embed = discord.Embed(title="You are not authorized to use this bot",color=0xe23a1d)
    if guild is None:
        embed = discord.Embed(title="You can't use this command outside of servers.",color=0xe23a1d)
    return embed
#6 | Done |
@bot.command(pass_context=True)
async def help(ctx):
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return

    embed = discord.Embed(title="Bot From State Farm",description="Checks messages for key words and notifies you!",color=0x30abc0)
    embed.add_field(name="Bot Commands",value=help_str.description_str.format(prefix=bot.prefix))
    embed.add_field(name="watched", value=help_str.watched_str, inline=False)
    embed.add_field(name="Add to watched list",value=help_str.watchword_str.format(prefix=bot.prefix),inline=False)
    embed.add_field(name="Remove from watched list",value=help_str.deleteword_str.format(prefix=bot.prefix),inline=False)
    embed.set_footer(text=help_str.footer_str)
    await ctx.message.channel.send(embed=embed)
#7 | Done |
@bot.command(pass_context=True)
async def adduser(ctx):
    if ctx.message.mentions is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    user = ctx.message.mentions[0].id
    memberid = ctx.message.author.id
    mentuser = ctx.message.mentions[0].name
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c=cur.execute("Select * from mods")
    u_list=""
    file_list=[]
    for q in c:
        if q[1] == memberid:
            if q[3]:
                u_list=("{}".format(q[3]))
                u_list = list(map(int,(u_list.split())))
                if user not in u_list:
                    newq3 = ('"{0} {1}"'.format(q[3], user))
                    cur.execute("UPDATE mods SET Users = {0} WHERE ID = {1}".format(newq3, memberid))
                    write_to_db()
                    connect_to_db()
                    c=cur.execute("Select * from files")
                    for q in c:
                        if q[0]:
                            file_list.append(q[0])
                    if user not in file_list:
                        cur.execute("INSERT INTO files (User) VALUES ({})".format(user))
                        write_to_db()
                        with open("{}.txt".format(user), 'a+') as wuf:
                            wuf.write("start of log for {}".format(mentuser))
                        embed=discord.Embed(title="{} added to watch list & log file created".format(mentuser),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                    else:
                        embed=discord.Embed(title="{} added to watch list".format(mentuser),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                elif user in u_list:
                    embed = discord.Embed(title="You are already watching {}".format(mentuser),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)
                    return
            elif not q[3]:
                newq3 = ('"{}"'.format(user))
                cur.execute("UPDATE mods SET Users = {0} WHERE ID = {1}".format(newq3, memberid))
                write_to_db()
                connect_to_db()
                c=cur.execute("Select * from files")
                file_list=[]
                for q in c:
                    if q[0]:
                        file_list.append(q[0])
                if user not in file_list:
                    cur.execute("INSERT INTO files (User) VALUES ({})".format(user))
                    write_to_db()
                    with open("{}.txt".format(user), 'a+') as wuf:
                        wuf.write("start of log for {}".format(mentuser))
                    embed=discord.Embed(title="{} added to watch list & log file created".format(mentuser),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)
                else:
                    embed=discord.Embed(title="{} added to watch list".format(mentuser),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)

    write_to_db()
#8 | Done |
@bot.command(pass_context=True)
async def removeuser(ctx):
    if ctx.message.mentions is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    user = ctx.message.mentions[0].id
    memberid = ctx.message.author.id
    mentuser = ctx.message.mentions[0].name
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    member=bot.get_user(memberid)
    if user is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c = cur.execute("Select * from mods")
    for q in c:
        if q[1] == memberid:
            if q[3]:
                u_list=("{}".format(q[3]))
                w_users = list(map(int,(u_list.split())))
                if user in w_users:
                    w_users.remove(user)
                    if w_users != []:
                        w_users = " ".join(map(str, w_users))
                        newq3 = '"{}"'.format(w_users)
                    elif w_users == []:
                        newq3 = None
                    if newq3:
                        cur.execute("UPDATE mods SET Users = {0} WHERE ID = {1}".format(newq3, memberid))
                        write_to_db()
                        loggingfile = discord.File('{}.txt'.format(user))
                        embed=discord.Embed(title="{} removed from watch list".format(mentuser),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                        await member.send(file=loggingfile)
                    elif not newq3:
                        cur.execute("UPDATE mods SET Users = NULL WHERE ID = {}".format(memberid))
                        write_to_db()
                        loggingfile = discord.File('{}.txt'.format(user))
                        embed=discord.Embed(title="{} removed from watch list. You're no longer watching anyone".format(mentuser),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                        await member.send(file=loggingfile)
            else:
                embed=discord.Embed(title="You are not watching {}".format(mentuser),color=0x39c12f)
                await ctx.message.channel.send(embed=embed)
                return
    write_to_db()
#9 | Done |
@bot.command(pass_context=True)
async def addword(ctx, word: str = None):
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    if word is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    word = word.lower()
    connect_to_db()
    c = cur.execute("Select * from mods")
    for q in c:
        if q[1] == memberid:
            if q[2]:
                w_words = list(q[2].split())
                if word not in w_words:
                    newq2 = ('"{0} {1}"'.format(q[2], word))
                    cur.execute("UPDATE mods SET Words = {0} WHERE ID = {1}".format(newq2, memberid))
                    write_to_db()
                    embed=discord.Embed(title="{} added to watch list".format(word),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)
                    return
                else:
                    embed=discord.Embed(title="You are already watching {}".format(word),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)
            else:
                newq2 = ('"{}"'.format(word))
                cur.execute("UPDATE mods SET Words = {0} WHERE ID = {1}".format(newq2, memberid))
                write_to_db()
                embed=discord.Embed(title="{} added to watch list".format(word),color=0x39c12f)
                await ctx.message.channel.send(embed=embed)
                return
    write_to_db()
#10 | Done |
@bot.command(pass_context=True)
async def removeword(ctx, word: str = None):
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    if word is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    word = word.lower()
    connect_to_db()
    c = cur.execute("Select * from mods")
    w_words=[]
    for q in c:
        if q[1] == memberid:
            if q[2]:
                w_words = list(q[2].split())
                if word in w_words:
                    w_words.remove(word)
                    if w_words:
                        sep=' '
                        w_words_fmt = sep.join(w_words)
                        newq2 = ('"{}"'.format(w_words_fmt))
                        cur.execute("UPDATE mods SET Words = {0} where ID = {1}".format(newq2, memberid))
                        write_to_db()
                        embed=discord.Embed(title="{} removed from watch list".format(word),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                        return
                    elif not w_words:
                        cur.execute("UPDATE mods SET Words = NULL where ID = {}".format(memberid))
                        write_to_db()
                        embed=discord.Embed(title="{} removed from watch list. You're no longer watching any words".format(word),color=0x39c12f)
                        await ctx.message.channel.send(embed=embed)
                        return
                else:
                    embed=discord.Embed(title="You are not watching {}".format(word),color=0x39c12f)
                    await ctx.message.channel.send(embed=embed)
            elif type (q[2]) == None:
                embed=discord.Embed(title="You aren't watching any words",color=0x39c12f)
                await ctx.message.channel.send(embed=embed)
    write_to_db()
#11 | Done |
@bot.command(pass_context=True)
async def watched(ctx):
    member = ctx.message.author
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c = cur.execute("Select * from mods")
    q3_names_list=[]
    for q in c:
        if q[1] == memberid:
            if q[2]:
                q2= list(q[2].split())
            else:
                q2= []
            if q[3]:
                q3= list(map(int,(q[3].split())))
                for item in q3:
                    user = await bot.fetch_user(item)
                    q3_names = user.display_name
                    q3_names_list.append(q3_names)
            else:
                q3_names_list = []
            if q[2] and q[3]:
                sep = ', '
                watched_ls = (q2 + q3_names_list)
                watched_str = sep.join(watched_ls)
                embed=discord.Embed(title="{} your watched words / phrases and users".format(member.name),color=0x76c7e9)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="Watching", value=watched_str, inline=False)
                await ctx.message.channel.send(embed=embed)
            elif q[2] and not q[3]:
                sep = ', '
                watched_ls = (q2)
                watched_str = sep.join(watched_ls)
                embed=discord.Embed(title="{} your watched words / phrases. You have no watched users".format(member.name),color=0x76c7e9)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="Watching", value=watched_str, inline=False)
                await ctx.message.channel.send(embed=embed)
            elif not q[2] and q[3]:
                sep = ', '
                watched_ls = (q3_names_list)
                watched_str = sep.join(watched_ls)
                embed=discord.Embed(title="{} your watched watched users. You have no watched words / phrases".format(member.name),color=0x76c7e9)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name="Watching", value=watched_str, inline=False)
                await ctx.message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="No words/phrases and users currently watched.",color=0x9f9f9f)
                await ctx.message.channel.send(embed=embed)
                return
    write_to_db()
#12 | Done |
@bot.command(pass_context=True)
async def forcesave(ctx):
    """Forces the bot to write current saved user data into their respective JSON files."""
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    write_to_db()
    connect_to_db()
    embed = discord.Embed(title="Force save complete.", color=0xe23a1d)
    await ctx.message.channel.send(embed=embed)
#13 | Not Done |
@bot.command(pass_context=True)
async def loguser(ctx):
    if ctx.message.mentions is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    user = ctx.message.mentions[0].id
    memberid = ctx.message.author.id
    mentuser = ctx.message.mentions[0].name
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c=cur.execute("Select * from files")
    file_list=[]
    for q in c:
        if q[0]:
            file_list.append(q[0])
    if user not in file_list:
        cur.execute("INSERT INTO files (User) VALUES ({})".format(user))
        write_to_db()
        with open("{}.txt".format(user), 'a+') as wuf:
            wuf.write("start of log for {}".format(mentuser))
        embed=discord.Embed(title="{}'s log file has been created".format(mentuser),color=0x39c12f)
        await ctx.message.channel.send(embed=embed)
#14 | Done |
@bot.command(pass_context=True)
async def logs(ctx):
    if ctx.message.mentions is None:
        embed = discord.Embed(
            title="Use {prefix}help for command documentation.".format(
                prefix=bot.prefix),
            color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
        return
    user = ctx.message.mentions[0].id
    member = ctx.message.author
    memberid = ctx.message.author.id
    maker = bot.get_user(maker_id)
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c = cur.execute("Select * from files")
    file_list=[]
    for q in c:
        if q[0]:
            file_list.append(q[0])
    if user in file_list:
        loggingfile = discord.File('{}.txt'.format(user))
        await member.send(file=loggingfile)
        await maker.send(content="{} pulled from the logs".format(member))
    elif user not in file_list and file_list != []:
        embed = discord.Embed(title="There is no log file for that user", color=0x9f9f9f)
        await ctx.message.channel.send(embed=embed)
    elif file_list == []:
        embed = discord.Embed(title="There are no log files to pull from")
    write_to_db()
#15 | Done |
@bot.command(pass_context=True)
async def logsml(ctx):
    member = ctx.message.author
    memberid = ctx.message.author.id
    maker = (bot.get_user(maker_id))
    if memberid == maker_id:
      mlfe = discord.File('message_log.txt')
      await member.send(file=mlfe)
    elif memberid != maker_id:
      embed = discord.Embed(
      title="You are not authorized to use this command".format(prefix=bot.prefix),color=0xe23a1d)
      await ctx.message.channel.send(embed=embed)
      await maker.send(content="ALERT {} tried to use logsml".format(member))
      return
#16 | Done |
@bot.command(pass_context=True)
async def logspl(ctx):
    member = ctx.message.author
    memberid = ctx.message.author.id
    maker = (bot.get_user(maker_id))
    if memberid == maker_id:
      plfe = discord.File('print_log.txt')
      await member.send(file=plfe)
    elif memberid != maker_id:
      embed = discord.Embed(
      title="You are not authorized to use this command".format(prefix=bot.prefix),color=0xe23a1d)
      await ctx.message.channel.send(embed=embed)
      await maker.send(content="ALERT {} tried to use logspl".format(member))
      return
#17 | Done |
@bot.command(pass_context=True)
async def logsmlxl(ctx):
    member = ctx.message.author
    memberid = ctx.message.author.id
    maker = (bot.get_user(maker_id))
    if memberid == maker_id:
      mlxlfe = discord.File('message_logxl.txt')
      await member.send(file=mlxlfe)
    elif memberid != maker_id:
      embed = discord.Embed(
      title="You are not authorized to use this command".format(prefix=bot.prefix),color=0xe23a1d)
      await ctx.message.channel.send(embed=embed)
      await maker.send(content="ALERT {} tried to use logsmlxl".format(member))
      return
#18 | Done |
@bot.event
async def on_message(message):
    """Scans messages for key words/phrases and alerts any user that might be watching them"""
    if message.author == bot.user:
        return
    if message.guild is None:
        print("Well if this is showing up something is real fucked up")
        return
    user_id = message.author.id
    ml_author="{}".format(message.author)
    ml_channel="{}".format(message.channel)
    ml_content="{}".format(message.content)
    ml_link="{}".format(message.jump_url)
    ml_time="{}".format(get_timeStamp())
    txtfilename = message.author.id
    #Notification System
    connect_to_db()
    c=cur.execute("Select * from mods")
    user_list=[]
    word_list=[]
    for q in c:
        log=0
        matches=[]
        user = (bot.get_user(q[1]))
        if type (q[3]) == str:
            user_list=list(map(int,(q[3].split())))
        elif type (q[3]) == int:
            user_list.append(q[3])
        else:
            user_list=[]
        if q[2]:
            word_list=list(q[2].split())
        else:
            word_list=""
        for item in word_list:
            pattern=re.compile(r"\b{}+\W?\S?\b".format(item), re.I)
            match=pattern.findall(message.content.lower())
            if match:
                matches.append(item)
        if matches:
            if user_id in user_list:
                embed = discord.Embed(title="A watched user said a watched word/phrase",color=0xeb8d25)
                embed.add_field(name="Author",value=ml_author,inline=False)
                embed.add_field(name="Channel",value=ml_channel,inline=False)
                embed.add_field(name="Message",value=ml_content,inline=False)
                embed.add_field(name="Link",value=ml_link,inline=False)
                await user.send(embed=embed)
                log = 1
            else:
                embed=discord.Embed(title="A watched word/phrase was detected",color=0xeb8d25)
                embed.add_field(name="Channel:",value=ml_channel,inline=False)
                embed.add_field(name="Author:",value=ml_author,inline=False)
                embed.add_field(name="Message:",value=ml_content,inline=False)
                embed.add_field(name="Link", value=ml_link,inline=False)
                await user.send(embed=embed)
                log = 2
        elif user_id in user_list:
            embed = discord.Embed(title="A watched user sent a message",color=0xeb8d25)
            embed.add_field(name="Author",value=ml_author,inline=False)
            embed.add_field(name="Channel",value=ml_channel,inline=False)
            embed.add_field(name="Message",value=ml_content,inline=False)
            embed.add_field(name="Link",value=ml_link,inline=False)
            await user.send(embed=embed)
            log = 3
    #Logging System
    c=cur.execute("Select * from files")
    file_list=""
    for q in c:
        if user_id == q[0]:
            if log:
                if log == 1:
                    print(user+" "+ml_time+"U + W/P "+ml_author+matches)
                    plcontent =("\n{}".format(user)+" "+ml_time+"U + W/P "+ml_author+matches)
                    with open(bot.print_log, 'a+') as plf:
                        plf.write("{}".format(plcontent))

                    mlcontent = ("\n{}".format(user)+" "+ml_time+"U + W/P; "+ml_channel+"  "+ml_author+"  "+ml_content+"\n"+ml_link)
                    with open(bot.message_log, 'a+') as mlf:
                        mlf.write("{}".format(mlcontent))

                    mlxlcontent = ("\n"+"~{}".format(user)+ml_time+"~"+"~U + W/P~"+ml_channel+"~"+ml_author+"~"+ml_content+"~"+ml_link)
                    with open(bot.message_logxl, 'a+') as mlxlf:
                        mlxlf.write("{}".format(mlxlcontent))
                    wucontent = ("\n"+ml_time+" "+ml_channel+" "+ml_author+" "+ml_content+"\n"+ml_link)
                    with open("{}.txt".format(txtfilename), 'a+') as wuf:
                        wuf.write("{}".format(wucontent))
                elif log == 2:
                    print("{}".format(user)+ " "+ml_time+" W/P "+matches)
                    plcontent = ("\n{}".format(user)+" "+ml_time+" W/P "+matches)
                    with open(bot.print_log, 'a+') as plf:
                        plf.write("{}".format(plcontent))

                    mlcontent = ("\n{}".format(user)+" "+ml_time+" W/P; "+ml_channel+"  "+ml_author+"  "+ml_content+"\n"+ml_link)
                    with open(bot.message_log, 'a+') as mlf:
                        mlf.write("{}".format(mlcontent))

                    mlxlcontent = ("\n"+"~{}".format(user)+ml_time+"~"+"~W/P~"+ml_channel+"~"+ml_author+"~"+ml_content+"~"+ml_link)
                    with open(bot.message_logxl, 'a+') as mlxlf:
                        mlxlf.write("{}".format(mlxlcontent))
                elif log == 3:
                    print("{}".format(user)+ " "+ml_time+" U "+ml_author)
                    plcontent = ("\n{}".format(user)+" "+ml_time+" U "+ml_author)
                    with open(bot.print_log, 'a+') as plf:
                        plf.write("{}".format(plcontent))

                    mlcontent = ("\n{}".format(user)+" "+ml_time+" U; "+ml_channel+"  "+ml_author+"  "+ml_content+"\n"+ml_link)
                    with open(bot.message_log, 'a+') as mlf:
                        mlf.write("{}".format(mlcontent))

                    mlxlcontent = ("\n"+"~{}".format(user)+ml_time+"~"+"~U~"+ml_channel+"~"+ml_author+"~"+ml_content+"~"+ml_link)
                    with open(bot.message_logxl, 'a+') as mlxlf:
                        mlxlf.write("{}".format(mlxlcontent))

                    wucontent = ("\n"+ml_time+" "+ml_channel+" "+ml_author+" "+ml_content+"\n"+ml_link)
                    with open("{}.txt".format(txtfilename), 'a+') as wuf:
                        wuf.write("{}".format(wucontent))
            else:
                wucontent = ("\n"+ml_time+" "+ml_channel+" "+ml_author+" "+ml_content+"\n"+ml_link)
                with open("{}.txt".format(txtfilename), 'a+') as wuf:
                    wuf.write("{}".format(wucontent))
    write_to_db()
    await bot.process_commands(message)
#19 | Done |
@bot.command(pass_context=True)
async def givemod(ctx):
    memberid = ctx.message.author.id
    mentioned=ctx.message.mentions[0]
    user =ctx.message.mentions[0].id
    if memberid != maker_id:
        embed = discord.Embed(
            title="Command only usable by Jake From State Farm".format(prefix=bot.prefix),color=0xe23a1d)
        await ctx.message.channel.send(embed=embed)
        return
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    c=cur.execute("Select * from mods")
    admin_id_list=[]
    for q in c:
        if q[1]:
            admin_id_list.append(q[1])
    if user in admin_id_list:
        embed = discord.Embed(title="{} is already an admin".format(mentioned), color=0x39c12f)
        await ctx.message.channel.send(embed=embed)
        return

    await ctx.message.channel.send(content="Awaiting Host Verification")
    print("Are you sure you would like to make {} an admin".format(mentioned))
    host_verification = input("type yes to confirm type no to cancel.\n")

    if host_verification == "yes":
        c=cur.execute("Select * from mods")
        cur.execute("INSERT INTO mods(Name,ID) VALUES('{0}',{1})".format(mentioned.display_name,user))
        print("{} is now on the admin list".format(mentioned))
        embed = discord.Embed(title="{} has been added to Admin list".format(mentioned),color=0x39c12f)
        embed.set_footer(text="@{} can now use Bot From State Farm. Use `.help` to see what you can do".format(mentioned))
        await ctx.message.channel.send(embed=embed)
        write_to_db()
    elif host_verification == "no":
        embed = discord.Embed(title="Host Verification denied")
        await ctx.message.channel.send(embed=embed)
        return

    else:
        embed = discord.Embed(title="Operation Canceled")
        await ctx.message.channel.send(embed=embed)
        return
#20 | Done |
@bot.command(pass_context=True)
async def removemod(ctx):
    memberid = ctx.message.author.id
    mentioned=ctx.message.mentions[0]
    user =ctx.message.mentions[0].id
    connect_to_db()
    c=cur.execute("Select * from mods")
    if memberid != maker_id:
        embed = discord.Embed(
            title="Command only usable by Jake From State Farm".format(prefix=bot.prefix),color=0xe23a1d)
        await ctx.message.channel.send(embed=embed)
        return
    admin_id_list=[]
    for q in c:
        if q[1]:
            admin_id_list.append(q[1])
    if user not in admin_id_list:
        embed = discord.Embed(title="{} is not an admin".format(mentioned), color=0x39c12f)
        await ctx.message.channel.send(embed=embed)
        return


    await ctx.message.channel.send(content="Awaiting Host Verification")
    print("Are you sure you would like to remove {} as an admin".format(mentioned))
    host_verification = input("type yes to confirm type no to cancel.\n")

    if host_verification == "yes":
        c=cur.execute("Select * from mods")
        cur.execute("DELETE from mods WHERE ID={}".format(user))
        print("{} is no longer on the admin list".format(mentioned))
        embed = discord.Embed(title="{} has been removed to Admin list".format(mentioned),color=0x39c12f)
        await ctx.message.channel.send(embed=embed)
        write_to_db()
    elif host_verification == "no":
        embed = discord.Embed(title="Host Verification denied")
        await ctx.message.channel.send(embed=embed)
        return
    else:
        embed = discord.Embed(title="Operation Canceled")
        await ctx.message.channel.send(embed=embed)
        return
    write_to_db()
#21 | Done |
@bot.command(pass_context=True)
async def mods(ctx):
    """Shows user a list of their watched words"""
    member = ctx.message.author
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    connect_to_db()
    c = cur.execute("Select * from mods")
    admin_list=[]
    for q in c:
        if q[0]:
            admin_list.append(q[0])
    sep = ', '
    admin_list = (sep.join(admin_list))
    embed = discord.Embed(title="The admin users are", color=0x76c7e9)
    embed.add_field(name="Admins", value=admin_list, inline=False)
    await ctx.message.channel.send(embed=embed)
#22 | Done |
@bot.command(pass_context=True)
async def kill(ctx):
    member = ctx.message.author
    memberid = ctx.message.author.id
    embed=(cmdcheck(ctx, memberid, ctx.message.guild))
    maker = (bot.get_user(maker_id))
    if embed:
        await ctx.message.channel.send(embed=embed)
        return
    c = cur.execute("Select * from mods")
    for q in c:
        admin_list=[]
        if q[1]:
            admin_list.append(q[1])
    if memberid == maker_id:
        embed = discord.Embed(title="Bot From State Farm saving data and logging out.",color=0xe23a1d)
        await ctx.message.channel.send(embed=embed)
        print("Saving before logging out...")
        write_to_db()
        print("Done.")
        await bot.logout()
    elif memberid in admin_list:
        embed = discord.Embed(title="Only Jake From State Farm is authorized to do this",color=0xff9200)
        embed.add_field(name="Hello {}, emergency override has been requested, awaiting host verification".format(member),
            value="Request has been made",inline=False)
        await ctx.message.channel.send(embed=embed)
        await maker.send(content="An emergency override has been requested")
        print("{}has requested an emergency override to stop this bot".format(member))
        host_verification = input("type yes to confirm type no to cancel:")
        if host_verification == "yes":
            embed = discord.Embed(title="Bot From State Farm saving data and logging out.",color=0xe23a1d)
            await ctx.message.channel.send(embed=embed)
            print("Saving before logging out...")
            write_to_db()
            print("Done.")
            await bot.logout()
        elif host_verification == "no":
            embed = discord.Embed(title="Host emergency override denied")
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.message.channel.send(content="Operation FAILED")
            return
    else:
        embed = discord.Embed(title="Only Jake From State Farm is authorized to do this".format(prefix=bot.prefix),
            color=0xe23a1d)
        await ctx.message.channel.send(embed=embed)
        return
    write_to_db()

keep_alive.keep_alive()
bot.run(token)
