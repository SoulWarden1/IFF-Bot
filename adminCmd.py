import discord
from discord.ext import commands
import varStore
from datetime import datetime
from backgroundTasks import backgroundTasks

class adminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.group(pass_context=True, aliases=["ad"], invoke_without_subcommand=True)
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No command specified")
            return
             
    #Shutdown command
    @admin.command(pass_context=True, aliases=["Close","Quit","quit","shutdown","Shutdown"])
    async def close(self,ctx):
        await ctx.send("Shutting Down")
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"myself shutdown")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await self.bot.close()
        print("Bot Closed")
        quit()
    
    #Update member list variable
    @admin.command(pass_context=True, aliases=["up"])
    async def update(self, ctx, file: str):
        try:
            f = open(f"IFF Bot/storage/memberList.txt", "r")
        except:
            f = open("/home/pi/Desktop/iffBot/storage/memberList.txt","r")
        file_lines = f.read()
        varStore.members = file_lines.split("\n")
        #varStore.members.remove(" ")
        await ctx.reply("Member list updated")
        
    #Gets status of cogs
    @admin.command(pass_context=True, aliases=["CogStatus","cogstatus"])
    async def cogStatus(self, ctx):
        embed = discord.Embed(title=f'Cog Status', description=f"The status of cogs in the bot", color=0xFFA500)
        for x in self.bot.cogList:
            try:
                self.bot.load_extension(x)
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(name=f"{x}", value=f"Loaded", inline=False)
            except commands.ExtensionNotFound:
                embed.add_field(name=f"{x}", value=f"Not found", inline=False)
            else:
                embed.add_field(name=f"{x}", value=f"Unloaded", inline=False)
        await ctx.send(embed=embed)
    
    #Sets custom bot status
    @admin.command(pass_context=True, aliases=["Status"])
    async def status(self, ctx, *, status: str):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{status}")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.reply("Status updated")
        cog = self.bot.get_cog("backgroundTasks")
        cog.statusRotation.cancel()
    
    #Turns back on status auto rotation
    @admin.command(pass_context=True, aliases=["rotate"])
    async def rotateStatus(self, ctx):
        cog = self.bot.get_cog("backgroundTasks")
        cog.statusRotation.start()
        await ctx.reply("Status rotation active")
        
    #Makes bot join a vc
    @admin.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
       
    #Makes bot leave a vc 
    @admin.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        
    #Bot rgb color
    @admin.command()
    async def rgb(self,ctx):
        cog = self.bot.get_cog("backgroundTasks")
        if cog.rgb.is_running:
            cog.rgb.start()
            await ctx.reply("Starting")
        else:
            cog.rgb.stop()
            await ctx.reply("Stopping")
            
    @admin.command()
    async def insult(self,ctx):
        if varStore.insult == True:
            varStore.insult == False
            await ctx.reply("Insults disabled")
        elif varStore.insult == False:
            varStore.insult == True
            await ctx.reply("Insults enabled")
        
    #Get variable group
    @admin.group(pass_context=True, aliases=["Get"])
    async def get(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No variable specified")
            return
        
    #Prints a list of all member id's and usernames
    @get.command(aliases=["Members", "mem"])
    async def members(self,ctx):
        usernames = []
        for user in varStore.members:
            try:
                username = await self.bot.fetch_user(user)
                usernames.append(username.name)
            except:
                pass
            
        await ctx.send(f"**Member usernames:** {usernames} \n**Member Ids:** {varStore.members}")
        #await ctx.send(varStore.members)
    
    #Gets the last chosen person for the announcement
    @get.command(pass_context=True, aliases=["Pastid"])
    async def pastid(self, ctx):
        await ctx.reply(f"Last chosen id was: {varStore.pastSelectId}")
    
    #Gets a list of guilds the bot is in
    @get.command(pass_context=True, aliases=["guild","Guild","Guilds","server","servers","Server","Servers"])
    async def guilds(self, ctx):
        servers = []
        for guild in self.bot.guilds:
            servers.append(f"{guild.name}")
        await ctx.send(f"**Number of guilds:** {len(servers)}")
        await ctx.send("\n".join(servers))
        
    #Get the current time
    @get.command(pass_context=True, aliases=["Time"])
    async def time(self, ctx):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await ctx.reply(f"Current time is {current_time}")
    
    #Get a list of cogs
    @get.command(pass_content=True, aliases = ["Cogs","Cog","cog"])
    async def cogs(self,ctx):
        await ctx.reply(f"Cogs are {self.bot.cogList}")
        
    #Get the current platform of the bot
    @get.command(pass_context = True, aliases = ["Platform","plat"])
    async def platform(self, ctx):
        if varStore.platform == False:
            await ctx.reply("Currently running on windows")
        else:
            await ctx.reply("Currently running on the raspberry pi")
        
def setup(bot):
    bot.add_cog(adminCog(bot))
    
