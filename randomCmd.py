import json
import discord
from discord.ext import commands
import varStore
import requests
from random import randint, choice
import asyncio
from dotenv import load_dotenv
from os import getenv
import os
import time
import badwords


class randomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Testing ping command with latency
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["pong", "Ping", "Pong"])
    async def ping(self,ctx):
        if ctx.invoked_with == "ping":
            start_time = time.time()
            message = await ctx.send("Testing Ping...")
            end_time = time.time()

            await message.edit(content=f"Pong!\nResponse Time: {round(self.bot.latency * 1000)}ms\nAPI Latency: {round(((end_time - start_time)-self.bot.latency) * 1000)}ms\nTotal Latency: {round((end_time - start_time) * 1000)}ms")
            #await ctx.reply(f"Pong! (Response time: {round(self.bot.latency*1000, 2)}ms)")
        elif ctx.invoked_with == "pong":
            start_time = time.time()
            message = await ctx.send("Testing Pong...")
            end_time = time.time()

            await message.edit(content=f"Ping!\nResponse Time: {round(self.bot.latency * 1000)}ms\nAPI Latency: {round(((end_time - start_time)-self.bot.latency) * 1000)}ms\nTotal Latency: {round((end_time - start_time) * 1000)}ms")
            #await ctx.reply(f"Ping! (Response time: {round(self.bot.latency*1000, 2)}ms)")
        
    #Converts id to username
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Username","user","User","name","Name"], pass_context=True)
    async def username(self, ctx, id: int):
        if len(str(id)) == 18:
            username = await self.bot.fetch_user(id)
            await ctx.reply(f"Username is {username}")
        else:
            await ctx.reply("Invalid Id")
                
    #Converts user to id
    @commands.command(aliases=["ID","Id"])
    async def id(self, ctx, user: discord.User):
        await ctx.reply(f"User ID is {user.id}")
        
    #DM spam command
    @commands.command(aliases=["Dmspam"])
    @commands.is_owner()
    async def dmspam(self, ctx, user: discord.User, times: int, *, message=None):
        user = self.bot.get_user(user.id)
        info = await ctx.reply("Spamming now")
        if message is None: 
            messages = ["Get spammed","Get rekt","Get destroyed"]
            message = messages[randint(len(messages)-1)]
            
        # for i in range(times): 
        #     await user.send(message)
        #     if i > times*0.1:
        #         await info.edit(content="Spamming now (10%)")
        #     elif i > times*0.2:
        #         await info.edit(content="Spamming now (20%)")
        #     elif i > times*0.3:
        #         await info.edit(content="Spamming now (30%)")
        #     elif i > times*0.4:
        #         await info.edit(content="Spamming now (40%)")
        #     elif i > times*0.5:
        #         await info.edit(content="Spamming now (50%)")
        #     elif i > times*0.6:
        #         await info.edit(content="Spamming now (60%)")
        #     elif i > times*0.7:
        #         await info.edit(content="Spamming now (70%)")
        #     elif i > times*0.8:
        #         await info.edit(content="Spamming now (80%)")
        #     elif i > times*0.9:
        #         await info.edit(content="Spamming now (90%)")
                
        await ctx.reply("Spam complete (100%)")
        
    #Spams command
    @commands.command()
    async def spam(self, ctx, user: discord.User, times: int, *, msg = None):
        if ctx.message.author.id in varStore.admins:
            if msg is not None:
                for i in range(times):
                    await ctx.send(f"{user.mention} {msg}")
            else:
                for i in range(times):
                    await ctx.send(f"{user.mention} get spammed")
        else:
            await ctx.reply("Nope, owner privilege get rekt")
            
    #Ghost ping
    @commands.is_owner()
    @commands.command(aliases=["gping"])
    async def ghostping(self, ctx, user: discord.User):
        await ctx.message.delete()
        await ctx.send(user.mention, delete_after = 0.1)
        
    #Send dm's through bot
    @commands.is_owner()
    @commands.command(aliases=["DM","Dm"])
    async def dm(self, ctx, user: discord.User, *, message):
        user = self.bot.get_user(user.id)
        await user.send(message)
        await ctx.reply("Message sent")
        
    #Echo command 
    @commands.command(aliases=["mirror","Mirror","Echo"])
    async def echo(self, ctx, *, message):
        if ctx.message.author.id in varStore.admins:
            try:
                await ctx.message.delete()
            finally:
                await ctx.send(message)
        else:
            await ctx.reply("Invalid perms")
        
    #Minecraft username to UUID
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def mcid(self, ctx, username: str):
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

        if response.status_code == 200:
            await ctx.reply(f"The UUID of the username is: {response.json()['id']}")
        elif response.status_code == 204:
            await ctx.reply("Username has not been used before")
        else:
            await ctx.reply(f"Error. Code {response.status_code}")
            
    #UUID to Past username
    @commands.command()
    async def mcname(self, ctx, uuid : str):
        data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
        await ctx.reply(f"Minecraft username is: " + data["name"])
        
    #Trello link
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Trello"])
    async def trello(self, ctx):
        await ctx.reply(f"Here is the link to the trello: https://trello.com/b/WusrL4NA/iff-bot")

    #Fetch Avatar
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Avatar","pfp"])
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        if avamember.id == 423913295314026507:
            await ctx.reply("Weebs are banned now")
        else:
            userAvatarUrl = avamember.avatar_url
            await ctx.send(userAvatarUrl)
        
    #Dice command with custom sides
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Dice"])
    async def dice(self, ctx, num: int):
        dice = randint(1,num)
        await ctx.reply(f"You've rolled a {dice} out of {num} sides")
    
    #Eight ball
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name = "eightball", aliases=["EightBall","8ball"])
    async def  eightball(self, ctx:commands.Context):
        msgs = ["It is certain.", "It is decidedly so.","Without a doubt.","Yes definitely.","You may rely on it","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.", "Very doubtful."]
        choice = randint(0, len(msgs)-1)
        await ctx.reply(msgs[choice])
        
    @commands.command(name = "gif", aliases=["Gif"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gif(self, ctx:commands.Context, *, searchTerm = None):
        try:
            if searchTerm.lower() not in badwords.words and ctx.author.id != 310330681047908363:
                load_dotenv()
                tenorToken = os.getenv('TENORTOKEN')
                response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=25".format(searchTerm, tenorToken))
                data = response.json()
                gif = choice(data["results"])
                await ctx.send(f"{gif['media'][0]['gif']['url']}\n(Requested by {ctx.author.name}#{ctx.author.discriminator})")
            elif ctx.author.id == 310330681047908363:
                await ctx.send("You're gay")
            else:
                await ctx.send("Please don't search that :(")
        except:
            await ctx.send("Please input a search term")  
            
    @commands.command(name = "github", aliases=["git","Git"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def github(self, ctx:commands.Context):
        await ctx.reply("The link to the github page is: https://github.com/SoulWarden1/IFF-Bot")

async def setup(bot):
    await bot.add_cog(randomCog(bot))
