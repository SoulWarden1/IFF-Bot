from datetime import datetime
import discord
from discord.ext import commands
from random import randint
import logging
import time

import asyncio

from helpCmd import helpCog
from adminCmd import adminCog
from iffCmd import iffCog
from randomCmd import randomCog
from backgroundTasks import backgroundTasks
import varStore

from dotenv import load_dotenv
from os import getenv
load_dotenv()

token = getenv("TOKEN")

# intents = discord.Intents.default()
intents = discord.Intents.all()
intents.members = True

# Sets up bot
description = """A bot developed by SoulWarden for the IFF"""
activity = discord.Activity(type=discord.ActivityType.watching, name="me start up")
bot = commands.Bot(
    command_prefix="?",
    description=description,
    intents=intents,
    activity=activity,
    status=discord.Status.online,
    owner_ids=set(varStore.owners),
    help_command=None,
)

bot.cogList = ["adminCmd", "helpCmd", "iffCmd", "randomCmd", "backgroundTasks"]
# bot.statuses = ["Avyn", "Alvyn", "Arvin", "Alvym"]

# Loads all cogs
bot.load_extension("helpCmd")
bot.load_extension("adminCmd")
bot.load_extension("iffCmd")
bot.load_extension("randomCmd")
bot.load_extension("backgroundTasks")

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
try:
    handler = logging.FileHandler(
        filename="IFF Bot/storage/discord.log",
        encoding="utf-8",   
        mode="w",
    )
except:
    handler = logging.FileHandler(
        filename="/home/pi/Desktop/iffBot/storage/discord.log",
        encoding="utf-8",
        mode="w",
    )
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# Bot starting
@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print(f"Started at {current_time}")

    try:
        f = open(
            f"IFF Bot/storage/memberList.txt",
            "r",
        )
    except:
        f = open("/home/pi/Desktop/iffBot/storage/memberList.txt", "r")
        varStore.platform = True

    file_lines = f.read()
    varStore.members = file_lines.split("\n")
    varStore.members.remove("")
    print("Member list updated")

    try:
        f = open(
            "IFF Bot/storage/pastSelectId.txt",
            "r",
        )
    except:
        f = open("/home/pi/Desktop/iffBot/storage/pastSelectId.txt", "r")
    varStore.pastSelectId = f.read()
    print("Past id loaded")


dmChannelId = 950245454317236304
nineCooldown = []
fourCooldown = []

@bot.event
async def on_message(message: discord.Message = None):
    if message.author == bot.user:
        return
    if message.author.bot:
        return

    if message.guild is None and not message.author.bot:
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        channel = bot.get_channel(dmChannelId)
        embed = discord.Embed(
            title=f"{message.author}",
            description=f"**Sent at:** {current_time}\n**ID: **{message.author.id}",
            color=0xFFA500,
        )
        embed.add_field(name=f"Message: ", value=f"{message.content}", inline=False)
        await channel.send("<@499816773122654219>")
        msg = await channel.send(embed=embed)
        

        varStore.botDms[msg.id] = message.author.id
        print(varStore.botDms)
    else:
        # 9e rekt
        if varStore.insult:
            global nineCooldown
            channel = bot.get_channel(varStore.companyChannel)
            insults = [
                f"{message.author.mention}, get out of our chat 9e scum",
                f"What are you doing here {message.author.mention}, this is 8e turf",
                f"Go back to the crap 9e chat where you belong {message.author.mention}",
                f"Who's this 9e clown",
                f"9e is too lowly to be talking in a chat as great as this, get outta here {message.author.mention}",
                f"{message.author.mention}, please keep your skill issue to yourself its embarrassing"
            ]
            try:
                nineCom = discord.utils.get(
                    message.guild.roles, name="9e Grenadiers de la Garde"
                )
            except:
                if message.author.id != bot.id:
                    print("User dm sent, so no role was found")
            else:
                if (
                    message.channel.id == varStore.companyChannel
                    and nineCom in message.author.roles
                    and nineCooldown.count(message.author.id) == 0
                ):
                    choice = randint(0, len(insults) - 1)
                    nineCooldown.append(message.author.id)
                    await channel.send(f"{insults[choice]}")
                    await asyncio.sleep(60)
                    nineCooldown.remove(message.author.id)

            # 4e rekt
            global fourCooldown
            channel = bot.get_channel(varStore.companyChannel)
            insults = [
                f"{message.author.mention}, get out of our chat 4e, come back when you hit something",
                f"What are you doing here {message.author.mention}, go talk in your dead 4e chat",
                f"Go back to the crap 4e chat where you belong {message.author.mention}",
                f"Who's this 4e clown",
                f"{message.author.mention}, please keep your skill issue to yourself its embarrassing"
            ]
            try:
                fourCom = discord.utils.get(
                    message.guild.roles, name="4e Batterie d'Artillerie à Pied"
                )
            except:
                print("User dm sent, so no role was found")
            else:
                if (
                    message.channel.id == varStore.companyChannel
                    and fourCom in message.author.roles
                    and fourCooldown.count(message.author.id) == 0
                ):
                    choice = randint(0, len(insults) - 1)
                    fourCooldown.append(message.author.id)
                    await channel.send(f"{insults[choice]}")
                    await asyncio.sleep(60)
                    fourCooldown.remove(message.author.id)
                
    if message.channel.id == 950245454317236304 and message.reference is not None and message.author.id in varStore.owners:
        repliedId = message.reference.message_id
        dmUserId = varStore.botDms[repliedId]
        user = bot.get_user(dmUserId)
        await user.send(message.content)
        
        channel = bot.get_channel(dmChannelId)
        await channel.send("Message sent")

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if (
        reaction.message.channel.id == 907599229629911104
        and reaction.message.id == varStore.leaderPingMsgId
    ):
        msg = await (reaction.message.channel).fetch_message(reaction.message.id)
        thumbUp = discord.utils.get(msg.reactions, emoji="\N{THUMBS UP SIGN}")
        thumbDown = discord.utils.get(msg.reactions, emoji="\N{THUMBS DOWN SIGN}")
        thumbUpCount = str(thumbUp.count - 1)
        thumbDownCount = str(thumbDown.count - 1)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS UP SIGN}":
                thumbUpIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbUpNames = []

                for user in thumbUpIds:
                    thumbUpNames.append(user.name)
                thumbUpNameStr = " ,".join(thumbUpNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS DOWN SIGN}":
                thumbDownIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbDownNames = []

                for user in thumbDownIds:
                    thumbDownNames.append(user.name)
                thumbDownNameStr = ", ".join(thumbDownNames)

        if thumbUpNameStr == "":
            thumbUpNameStr = "No one :("
        if thumbDownNameStr == "":
            thumbDownNameStr = "No one :("

        embed = discord.Embed(
            title="Leadership Attendance",
            description="React with :thumbsup: or :thumbsdown: if you're coming tonight",
            color=0x109319,
        )
        embed.add_field(name="Coming: ", value=f"\u200b{thumbUpNameStr}", inline=False)
        embed.add_field(name="Count: ", value=f"\u200b{thumbUpCount}", inline=False)
        embed.add_field(
            name="Not coming: ", value=f"\u200b{thumbDownNameStr}", inline=False
        )
        embed.add_field(name="Count: ", value=f"\u200b{thumbDownCount}", inline=False)

        await msg.edit(embed=embed)


@bot.event
async def on_reaction_remove(reaction, user):
    if (
        reaction.message.channel.id == 907599229629911104
        and reaction.message.id == varStore.leaderPingMsgId
    ):
        msg = await (reaction.message.channel).fetch_message(reaction.message.id)
        thumbUp = discord.utils.get(msg.reactions, emoji="\N{THUMBS UP SIGN}")
        thumbDown = discord.utils.get(msg.reactions, emoji="\N{THUMBS DOWN SIGN}")
        thumbUpCount = str(thumbUp.count - 1)
        thumbDownCount = str(thumbDown.count - 1)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS UP SIGN}":
                thumbUpIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbUpNames = []

                for user in thumbUpIds:
                    thumbUpNames.append(user.name)
                thumbUpNameStr = ", ".join(thumbUpNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{THUMBS DOWN SIGN}":
                thumbDownIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                thumbDownNames = []

                for user in thumbDownIds:
                    thumbDownNames.append(user.name)
                thumbDownNameStr = " ,".join(thumbDownNames)

        if thumbUpNameStr == "":
            thumbUpNameStr = "No one :("
        if thumbDownNameStr == "":
            thumbDownNameStr = "No one :("

        embed = discord.Embed(
            title="Leadership Attendance",
            description="React with :thumbsup: or :thumbsdown: if you're coming tonight",
            color=0x109319,
        )
        embed.add_field(name="Coming: ", value=f"\u200b{thumbUpNameStr}", inline=False)
        embed.add_field(name="Count: ", value=f"\u200b{thumbUpCount}", inline=False)
        embed.add_field(
            name="Not coming: ", value=f"\u200b{thumbDownNameStr}", inline=False
        )
        embed.add_field(name="Count: ", value=f"\u200b{thumbDownCount}", inline=False)

        await msg.edit(embed=embed)


# Prints out errors to console
@bot.event
async def on_command_error(ctx, error):
    print(
        f"Error occured in {ctx.guild} by {ctx.message.author.name} ({ctx.message.author.id})"
    )
    print(f"Error is: {error}")


# Prints when a guild is joined
@bot.event
async def on_guild_join(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has joined {ctx.guild} at {current_time}")


# Prints when a guild if left
@bot.event
async def on_guild_remove(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has left {ctx.guild} at {current_time}")


# Reload cogs command
@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Reload", description="Reloaded cogs: ", color=0xFF00C8
        )
        for x in bot.cogList:
            bot.reload_extension(x)
            embed.add_field(name=f"**#{count}**", value=f"{x} reloaded", inline=False)
            count += 1
        await ctx.send(embed=embed)
    else:
        bot.reload_extension(f"{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)


# Unload cogs command
@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Unload", description="Unloaded cogs", color=0x109319
        )
        for x in bot.cogList:
            try:
                bot.unload_extension(x)
            except commands.ExtensionNotLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already unloaded", inline=False
                )
                count += 1
            else:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} unloaded", inline=False
                )
                count += 1
        await ctx.send(embed=embed)
    else:
        bot.unload_extension(extension)
        embed = discord.Embed(
            title="Unload", description=f"{extension} cog unloaded", color=0x109319
        )
        await ctx.reply(embed=embed)

# Load cogs command
@bot.command()
@commands.is_owner()
async def load(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(title="Load", description="Loaded cogs", color=0x109319)
        for x in bot.cogList:
            try:
                bot.load_extension(x)
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already loaded", inline=False
                )
                count += 1
            else:
                embed.add_field(name=f"**#{count}**", value=f"{x} loaded", inline=False)
                count += 1
        await ctx.send(embed=embed)
    else:
        bot.load_extension(extension)
        embed = discord.Embed(
            title="Load", description=f"{extension} cog loaded", color=0x109319
        )
        await ctx.reply(embed=embed)


bot.run(token)
