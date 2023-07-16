from datetime import datetime
import sys
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from discord.utils import get
from typing import Literal, Optional
from discord import app_commands
from random import randint
import platform

import varStore

from dotenv import load_dotenv
from os import getenv
import os
from pathlib import Path

load_dotenv()
token = os.getenv("TOKEN")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('_'),
            description="""A bot developed by SoulWarden for the IFF""",
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="me start up"),
            status=discord.Status.online,
            owner_ids=set(varStore.owners),
            help_command=None
            )
        self.cogList = ["adminCmd", "helpCmd", "iffCmd","backgroundTasks", "randomCmd", "attendance"]
        self.synced = False
        
    async def setup_hook(self): 
        for cog in self.cogList:
            await self.load_extension(cog)
        self.tree.copy_global_to(guild=discord.Object(varStore.iffGuild))
        await self.tree.sync(guild=discord.Object(varStore.iffGuild))
        print("Cogs loaded and tree synced")
        
bot = MyBot()
tree = bot.tree

# Bot starting
@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print(f"Started at {current_time}")
    
    storageFolder = Path().absolute() / "storage"
    
    memberListTxt = storageFolder / "memberList.txt"
    memberList = open(memberListTxt)
        
    file_lines = memberList.read()
    varStore.members = file_lines.split("\n")
    try:
        varStore.members.remove("")
    finally:
        memberList.close()
        print("Member list updated")

    pastIdTxt = storageFolder / "pastSelectId.txt"
    f = open(pastIdTxt)
        
    file_lines = f.read()
    varStore.pastSelectIds = file_lines.split("\n")
    try:
        varStore.pastSelectIds.remove("")
    finally:
        f.close()
        print("Past id loaded")

    # Sets prefix
    if platform.system() == 'Windows':
        bot.command_prefix = commands.when_mentioned_or('?')
        print("Platform: Windows")
    else:
        bot.command_prefix = commands.when_mentioned_or('_')
        print("Platform: Linux")
    
    print("Bot ready")

dmChannelId = 950245454317236304
nineCooldown = []
fourCooldown = []


@bot.event
async def on_message(message: discord.Message = None):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    
    # sevenRole = message.guild.get_role(783564469854142464)
    # eightRole = message.guild.get_role(845007589674188839)
    nineRole = message.guild.get_role(863756344494260224)
    fourRole = message.guild.get_role(760440084880162838)

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

    elif (
        message.channel.id == 806427204896292864
        and nineRole in message.author.roles or fourRole in message.author.roles
    ):
        await message.add_reaction("\N{Police Cars Revolving Light}")

    # elif message.channel.id == 806427204896292864:
    #     # 9e rekt
    #     if varStore.insult:
    #         global nineCooldown
    #         channel = bot.get_channel(varStore.companyChannel)
    #         insults = [
    #             f"{message.author.mention}, get out of our chat 9e scum",
    #             f"What are you doing here {message.author.mention}, this is 8e turf",
    #             f"Go back to the crap 9e chat where you belong {message.author.mention}",
    #             f"Who's this 9e clown",
    #             f"9e is too lowly to be talking in a chat as great as this, get outta here {message.author.mention}",
    #             f"{message.author.mention}, please keep your skill issue to yourself it's embarrassing",
    #             f"Of course 9e would want to talk in the superior 8e chat",
    #         ]
    #         try:
    #             nineCom = discord.utils.get(
    #                 message.guild.roles, name="9e Grenadiers de la Garde"
    #             )
    #         except:
    #             if message.author.id != bot.id:
    #                 print("User dm sent, so no role was found")
    #         else:
    #             if (
    #                 message.channel.id == varStore.companyChannel
    #                 and nineCom in message.author.roles
    #                 and nineCooldown.count(message.author.id) == 0
    #             ):
    #                 choice = randint(0, len(insults) - 1)
    #                 nineCooldown.append(message.author.id)
    #                 await channel.send(f"{insults[choice]}")
    #                 await asyncio.sleep(60)
    #                 nineCooldown.remove(message.author.id)

    #         # 4e rekt
    #         global fourCooldown
    #         channel = bot.get_channel(varStore.companyChannel)
    #         insults = [
    #             f"{message.author.mention}, get out of our chat 4e, come back when you hit something",
    #             f"What are you doing here {message.author.mention}, go talk in your dead 4e chat",
    #             f"Go back to the crap 4e chat where you belong {message.author.mention}",
    #             f"Who's this 4e clown",
    #             f"{message.author.mention}, please keep your skill issue to yourself its embarrassing",
    #             f"Of course 4e would want to talk in the superior 8e chat",
    #         ]
    #         try:
    #             fourCom = discord.utils.get(
    #                 message.guild.roles, name="4e Batterie d'Artillerie à Pied"
    #             )
    #         except:
    #             print("User dm sent, so no role was found")
    #         else:
    #             if (
    #                 message.channel.id == varStore.companyChannel
    #                 and fourCom in message.author.roles
    #                 and fourCooldown.count(message.author.id) == 0
    #             ):
    #                 choice = randint(0, len(insults) - 1)
    #                 fourCooldown.append(message.author.id)
    #                 await channel.send(f"{insults[choice]}")
    #                 await asyncio.sleep(60)
    #                 fourCooldown.remove(message.author.id)

    if (
        message.channel.id == 950245454317236304
        and message.reference is not None
        and message.author.id in varStore.owners
    ):
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
        shrug = discord.utils.get(msg.reactions, emoji="\N{SHRUG}")
        thumbUpCount = str(thumbUp.count - 1)
        thumbDownCount = str(thumbDown.count - 1)
        shrugCount = str(shrug.count - 1)

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
                thumbDownNameStr = ", ".join(thumbDownNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{SHRUG}":
                shrugIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                shrugNames = []

                for user in shrugIds:
                    shrugNames.append(user.name)
                shrugStr = ", ".join(shrugNames)

        if thumbUpNameStr == "":
            thumbUpNameStr = "No one :("
        if thumbDownNameStr == "":
            thumbDownNameStr = "No one :)"
        if shrugStr == "":
            shrugStr = "No one :("

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
        embed.add_field(name="Maybe coming: ", value=f"\u200b{shrugStr}", inline=False)
        embed.add_field(name="Count: ", value=f"\u200b{shrugCount}", inline=False)

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
        shrug = discord.utils.get(msg.reactions, emoji="\N{SHRUG}")
        thumbUpCount = str(thumbUp.count - 1)
        thumbDownCount = str(thumbDown.count - 1)
        shrugCount = str(shrug.count - 1)

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
                thumbDownNameStr = ", ".join(thumbDownNames)

        for reactions in msg.reactions:
            if str(reactions) == "\N{SHRUG}":
                shrugIds = [
                    user async for user in reactions.users() if user != bot.user
                ]
                shrugNames = []

                for user in shrugIds:
                    shrugNames.append(user.name)
                shrugStr = ", ".join(shrugNames)

        if thumbUpNameStr == "":
            thumbUpNameStr = "No one :("
        if thumbDownNameStr == "":
            thumbDownNameStr = "No one :)"
        if shrugStr == "":
            shrugStr = "No one :("

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
        embed.add_field(name="Maybe coming: ", value=f"\u200b{shrugStr}", inline=False)
        embed.add_field(name="Count: ", value=f"\u200b{shrugCount}", inline=False)

        await msg.edit(embed=embed)


# Prints out errors to console
@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound, )

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            await ctx.send('I could not find that member. Please try again.')

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
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
    
# For giving return members their roles back
@bot.event
async def on_member_remove(member):
    iffGuild = bot.get_guild(592559858482544641)
    iffRole = get(iffGuild.roles, id = 611927973838323724)
    
    storageFolder = Path().absolute() / "storage"
    leftMembersFile = storageFolder / "leftMembers.txt"
    
    # Checks if the guild is the IFF guild and if they have the IFF role
    if member.guild != iffGuild or iffRole not in member.roles:
        return
    
    # Checks if the user is already in the left members list and removes any previous versions
    with open(leftMembersFile, "r") as file:
        lines = file.readlines()
        lines_to_remove = []
        
        for i,line in enumerate(lines):
            if line.strip() == str(member.id):
                lines_to_remove.append(i)
                lines_to_remove.append(i+1)
                
    with open(leftMembersFile, "w") as file:
        for i, line in enumerate(lines):
            if i not in lines_to_remove:
                file.write(line)
    
    roleIds = []
    
    # Gets all the roles from a user and makes a list of strings with the role id's
    for role in member.roles:
        roleIds.append(str(role.id))
    
    # Converts the list into a string seperated by commas
    roleIds = ",".join(roleIds)

    # Writes the user ID with the following line containing the role id's
    with open(leftMembersFile, "a") as file:
        file.write(str(member.id) + "\n" + roleIds + "\n")
        
@bot.event
async def on_member_join(member):
    storageFolder = Path().absolute() / "storage"
    leftMembersFile = storageFolder / "leftMembers.txt"
    iffBotTestChannel = bot.get_channel(954194296809095188)
    
    with open(leftMembersFile, "r") as file:
        lines = file.readlines()
        
        for line in lines:
            if line.strip() == str(member.id):
                await iffBotTestChannel.send(f"{member.display_name} has previously been in the IFF server and can have their roles returned with </return_role:1125667822815694950>")
                break
        
    
    
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
@bot.command()
@commands.is_owner()
async def clear(ctx):
    tree.clear_commands(guild=discord.Object(id = varStore.iffGuild))
    await tree.sync(guild=discord.Object(id = varStore.iffGuild))
    await ctx.reply("Tree cleared")
    
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
            await bot.reload_extension(x)
            embed.add_field(name=f"**#{count}**", value=f"{x} reloaded", inline=False)
            count += 1
        await ctx.send(embed=embed)
        print("All cogs reloaded")
    else:
        await bot.reload_extension(f"{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)
        print(f"{extension} reloaded")

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
                await bot.unload_extension(x)
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
        await bot.unload_extension(extension)
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
                await bot.load_extension(x)
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
        await bot.load_extension(extension)
        embed = discord.Embed(
            title="Load", description=f"{extension} cog loaded", color=0x109319
        )
        await ctx.reply(embed=embed)


bot.run(token)
