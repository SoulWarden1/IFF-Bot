import discord
from discord.ext import commands

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(pass_context=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            #### Create the initial embed object ####
            helpMsg=discord.Embed(title="IFF Bot - Help", url="https://discord.com/channels/592559858482544641/806427204896292864", description="All available commands for the IFF bot. Run _help [command] for further information", color=0x17169a)
            helpMsg.add_field(name="Ping", value="Test command for testing bot response time", inline=False)
            helpMsg.add_field(name="Dice", value="Input a number, rolls a dice with that many sides", inline=False)
            helpMsg.add_field(name="mcid", value="Input the username of a minecraft player, outputs their UUID", inline=False)
            helpMsg.add_field(name="mcname", value="Input the uuid of a minecraft player, outputs their username", inline=False)
            helpMsg.add_field(name="id", value="Input the discord id of a user, output their username", inline=False)
            helpMsg.add_field(name="Trello", value="Posts the link to the trello", inline=False)
            helpMsg.add_field(name="Avatar", value="Posts the image of a pinged users avatar", inline=False)
            helpMsg.add_field(name="ID", value="Converts a pinged user to their ID", inline=False)
            helpMsg.add_field(name="Usernames", value="Converts an inputted ID to username", inline=False)
            helpMsg.add_field(name="Eight Ball", value="It's a magic eight ball", inline=False)
            helpMsg.add_field(name="Gif", value="Posts a gif related to the inputted message", inline=False)
            helpMsg.set_footer(text="Made by SoulWarden#8946")
            helpMsg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=helpMsg)
    
    @help.command(pass_context=True,aliases=["Ping"])
    async def ping(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Ping", description="The dice command",color=0x17169a)
        embed.add_field(name="Command", value="_ping", inline=False)
        embed.add_field(name="Aliases", value="ping, Ping, pong, Pong", inline=False)
        embed.add_field(name="Description", value="A testing command to see if the bot is online and outputs the latency", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Dice"])
    async def dice(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Dice", description="The dice command",color=0x17169a)
        embed.add_field(name="Command", value="_dice [num]", inline=False)
        embed.add_field(name="Aliases", value="dice, Dice", inline=False)
        embed.add_field(name="Description", value="Takes the inputed number and rolls a virtual dice with that number of sides", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    # @help.command(pass_context=True, aliases=["Math","Maths","maths"])
    # async def math(self, ctx):
    #     embed=discord.Embed(title="IFF Bot - Help - Math", description="The math command",color=0x17169a)
    #     embed.add_field(name="Command", value="_math [equation]", inline=False)
    #     embed.add_field(name="Aliases", value="math, Math, Maths, maths", inline=False)
    #     embed.add_field(name="Description", value="Takes in a short equation and calculates result. Example: _math 2*3-2, _math 3+2/2, _math 5^2/3)", inline=True)
    #     embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
            
    @help.command(pass_context=True)
    async def mcid(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - McId", description="The mcid command",color=0x17169a)
        embed.add_field(name="Command", value="_mcid [Minecraft Username]", inline=False)
        embed.add_field(name="Aliases", value="mcid", inline=False)
        embed.add_field(name="Description", value="Takes the inputed minecraft username and converts it into the UUID", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True)
    async def mcname(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - mcname", description="The mcname command",color=0x17169a)
        embed.add_field(name="Command", value="_mcname [Minecraft Username]", inline=False)
        embed.add_field(name="Aliases", value="mcid", inline=False)
        embed.add_field(name="Description", value="Takes the inputed minecraft username and converts it into the UUID", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Trello"])
    async def trello(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Trello", description="The trello command",color=0x17169a)
        embed.add_field(name="Command", value="_trello", inline=False)
        embed.add_field(name="Aliases", value="trello, Trello", inline=False)
        embed.add_field(name="Description", value="Gives the link to the trello (may be outdated)", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Avatar","pfp"])
    async def avatar(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Avatar", description="The avatar command",color=0x17169a)
        embed.add_field(name="Command", value="_avatar [user]", inline=False)
        embed.add_field(name="Aliases", value="avatar, Avatar, pfp", inline=False)
        embed.add_field(name="Description", value="Outputs the pinged users profile picture", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Username","user","User","name","Name"])
    async def username(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Username", description="The username command",color=0x17169a)
        embed.add_field(name="Command", value="_username [user id]", inline=False)
        embed.add_field(name="Aliases", value="Username, user, User, name, Name", inline=False)
        embed.add_field(name="Description", value="Takes the inputed id and converts it into a username", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["ID","Id"])
    async def id(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - ID", description="The id command",color=0x17169a)
        embed.add_field(name="Command", value="_id [user]", inline=False)
        embed.add_field(name="Aliases", value="id, ID, Id", inline=False)
        embed.add_field(name="Description", value="Gives the pinged users id", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    #IFF COMMANDS ------------------------------------------------------------------------
    @help.command(pass_context=True,aliases=["Template","temp","Temp"])
    async def template(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Template", description="The template command",color=0x17169a)
        embed.add_field(name="Command", value="_template", inline=False)
        embed.add_field(name="Aliases", value="template, Template, temp, Temp", inline=False)
        embed.add_field(name="Description", value="Dm's the user an announcement template", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Schedule", "timetable", "Timetable"])
    async def schedule(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Schedule", description="The schedule command",color=0x17169a)
        embed.add_field(name="Command", value="_schedule", inline=False)
        embed.add_field(name="Aliases", value="schedule, Schedule, timetable, Timetable", inline=False)
        embed.add_field(name="Description", value="Points the user to the IFF schedule channel", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True,aliases=["Ranks", "rank", "Rank"])
    async def ranks(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Rank", description="The rank command",color=0x17169a)
        embed.add_field(name="Command", value="_rank", inline=False)
        embed.add_field(name="Aliases", value="ranks, Ranks, rank, Rank", inline=False)
        embed.add_field(name="Description", value="Points the user to the IFF rank channel", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @help.command(pass_context=True, aliases=["Eightball", "8ball"])
    async def eightball(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Eight Ball", description="The eight ball command",color=0x17169a)
        embed.add_field(name="Command", value="_eightball", inline=False)
        embed.add_field(name="Aliases", value="eightball, Eightball, 8ball", inline=False)
        embed.add_field(name="Description", value="It's a magic eight ball, not much more too it", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True, aliases=["Gif"])
    async def gif(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Gif", description="The gif command",color=0x17169a)
        embed.add_field(name="Command", value="_gif [search term]", inline=False)
        embed.add_field(name="Aliases", value="gif, Gif", inline=False)
        embed.add_field(name="Description", value="Posts a gif related to the search term", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    #Template  
    # @help.command(pass_context=True, aliases=[""])
    # async def service(self, ctx):
    #     embed=discord.Embed(title="IFF Bot - Help - ", description="The  command",color=0x17169a)
    #     embed.add_field(name="Command", value="_", inline=False)
    #     embed.add_field(name="Aliases", value="", inline=False)
    #     embed.add_field(name="Description", value="", inline=True)
    #     embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
                   
    #NCO HELP --------------------------------------------------------
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @help.group(pass_context=True, aliases=["NCO"])
    async def nco(self,ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="IFF Bot - Help - NCO Commands", description="All available commands for NCO's. Run _help nco [command] for further information",color=0x17169a)
            embed.add_field(name="Roll", value="Auto rolls the person doing the 8e announcement", inline=False)
            embed.add_field(name="Company Welcome", value="Welcomes a pinged user to the company (8e only currently)", inline=False)
            embed.add_field(name="Announcement", value="Automatically posts an announcement with an inputted message (8e only currently)", inline=False)
            embed.add_field(name="Wargames", value="Automatically creates a wargames rotation with pinged users", inline=False)
            embed.add_field(name="Attendance", value="Displays total and company attendance numbers as well as all users in vc's (including mercs and recruits)", inline=False)
            embed.add_field(name="Leadership attendance", value="Creates the leadership attendance form (8e only)", inline=False)
            embed.add_field(name="Split", value="Splits the users in the current voice chat to the other company channel", inline=False)
            embed.add_field(name="Merge", value="Merges the users in both company voice chats to the primary one", inline=False)
            embed.add_field(name="Parade", value="Moves all users in the current connected voice chat to parade ground", inline=False)
            embed.add_field(name="Force parade", value="Moves **all** users in holdfast channels to parade ground", inline=False)
            embed.add_field(name="Spread", value="Moves all users in parade ground to their respective company channel", inline=False)
            embed.add_field(name="Muster", value="Creates the muster roll", inline=False)
            embed.add_field(name="Service", value="Automatically displays who requires serivce roles", inline=False)
            embed.add_field(name="Recruit Form", value="Posts the recruitment form", inline=False)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            
    @nco.command(pass_context=True, aliases=["Roll"])
    async def roll(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Roll", description="The roll command",color=0x17169a)
        embed.add_field(name="Command", value="_roll", inline=False)
        embed.add_field(name="Aliases", value="roll, Roll", inline=False)
        embed.add_field(name="Description", value="Randomly selects who will do the 8e announcement", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      
    @nco.command(pass_context=True, aliases=["comWelcome","comwel","ComWel","Comwel","companywelcome","Companywelcome"])
    async def comWell(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Company Welcome", description="The company welcome command",color=0x17169a)
        embed.add_field(name="Command", value="_comWel [Recruit]", inline=False)
        embed.add_field(name="Aliases", value="comWelcome, comwel, ComWel, Comwel, companywelcome, Companywelcome", inline=False)
        embed.add_field(name="Description", value="Takes the inputed user id and posts a welcome message in a specified channel", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)       
        
    @nco.command(pass_context=True, aliases=["Lazy","lazy","Announcement","announce","Announce"])
    async def announcement(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Announcement", description="The announcement command",color=0x17169a)
        embed.add_field(name="Command", value="_announcement [message]", inline=False)
        embed.add_field(name="Aliases", value="announcement, Lazy, lazy, Announcement, announce, Announce", inline=False)
        embed.add_field(name="Description", value="Posts an announcement preset, user must input a message to go along with it. User can manually ping if they want", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Wargames", "wg", "Wg"])
    async def wargames(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Wargames", description="The wargames command",color=0x17169a)
        embed.add_field(name="Command", value="_wargames [user1] [user2] [user3] [user4] [user5] [user6]", inline=False)
        embed.add_field(name="Aliases", value="wargames, Wargames, wg, Wg", inline=False)
        embed.add_field(name="Description", value="Takes up to 6 inputted users and creates a wargames leader rotation", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Attendance","attend"])
    async def attendance(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Attendance", description="The attendnace command",color=0x17169a)
        embed.add_field(name="Command", value="_attend", inline=False)
        embed.add_field(name="Aliases", value="attendance, Attendance, attend", inline=False)
        embed.add_field(name="Description", value="Provides the current total IFF attendance and company attendance plus the users connect to the voice chats", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["leadattend","leadershipAttendnace"])
    async def leadAttend(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Leadership Attendnace", description="The leadership attendnace command",color=0x17169a)
        embed.add_field(name="Command", value="_leadattend", inline=False)
        embed.add_field(name="Aliases", value="leadAttend, leadattend, leadershipAttendnace", inline=False)
        embed.add_field(name="Description", value="Generates the form for 8e leadership", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=[""])
    async def split(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Split", description="The split command",color=0x17169a)
        embed.add_field(name="Command", value="_split", inline=False)
        embed.add_field(name="Aliases", value="split, Split", inline=False)
        embed.add_field(name="Description", value="Splits the users in the current voice chat into the other company chat. The user running the command must be in the company they wish to split", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Merge"])
    async def merge(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Merge", description="The merge command",color=0x17169a)
        embed.add_field(name="Command", value="_merge", inline=False)
        embed.add_field(name="Aliases", value="merge, Merge", inline=False)
        embed.add_field(name="Description", value="Merges the users from the secondary company chat to the primary one. The user running the command must be in the company they wish to merge", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @nco.command(pass_context=True, aliases=["Parade"])
    async def parade(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Parade", description="The parade command",color=0x17169a)
        embed.add_field(name="Command", value="_parade", inline=False)
        embed.add_field(name="Aliases", value="parade, Parade", inline=False)
        embed.add_field(name="Description", value="Moves all users in the currently connect voice chat to parade ground", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Forceparade","unfuck","return"])
    async def forceparade(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Force Parade", description="The force parade command",color=0x17169a)
        embed.add_field(name="Command", value="_forceparade", inline=False)
        embed.add_field(name="Aliases", value="forceparade, Forceparade, unfuck, return", inline=False)
        embed.add_field(name="Description", value="Forces all users in the holdfast voice chats to parade ground. Use with caution", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed) 
        
    @nco.command(pass_context=True, aliases=["Spread","fuckoff"])
    async def spread(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Spread", description="The spread command",color=0x17169a)
        embed.add_field(name="Command", value="_spread", inline=False)
        embed.add_field(name="Aliases", value="spread, Spread, fuckoff", inline=False)
        embed.add_field(name="Description", value="Moves the users in parade ground to their appropriate company channels", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Muster"])
    async def muster(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Muster", description="The muster command",color=0x17169a)
        embed.add_field(name="Command", value="_muster", inline=False)
        embed.add_field(name="Aliases", value="muster, Muster", inline=False)
        embed.add_field(name="Description", value="Autogenerates the muster roll and removes the old one", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @nco.command(pass_context=True, aliases=["Service"])
    async def service(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - Service", description="The service command",color=0x17169a)
        embed.add_field(name="Command", value="_service", inline=False)
        embed.add_field(name="Aliases", value="service, Service", inline=False)
        embed.add_field(name="Description", value="Automatically calculates who requres service medals", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @nco.command(pass_context=True, aliases=["Rctform", "rctForm", "RctForm"])
    async def rctform(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO - rctform", description="The recruit form command",color=0x17169a)
        embed.add_field(name="Command", value="_rctform", inline=False)
        embed.add_field(name="Aliases", value="rctform, Rctform, rctForm, RctForm", inline=False)
        embed.add_field(name="Description", value="Posts the recruitment form in the current channel", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    #Template
    # @nco.command(pass_context=True, aliases=[""])
    # async def service(self, ctx):
    #     embed=discord.Embed(title="IFF Bot - Help - NCO - ", description="The  command",color=0x17169a)
    #     embed.add_field(name="Command", value="_", inline=False)
    #     embed.add_field(name="Aliases", value="", inline=False)
    #     embed.add_field(name="Description", value="", inline=True)
    #     embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    #     await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(helpCog(bot))
