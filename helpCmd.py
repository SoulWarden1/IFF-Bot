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
            helpMsg=discord.Embed(title="IFF Bot - Help", url="https://discord.com/channels/592559858482544641/806427204896292864", description="All available commands for the IFF bot. Run _help [command] for further information", color=0x109319)
            helpMsg.add_field(name="Ping", value="Test command for testing bot response time", inline=False)
            helpMsg.add_field(name="Dice", value="Input a number, rolls a dice with that many sides", inline=False)
            helpMsg.add_field(name="mcid", value="Input the username of a minecraft player, outputs their UUID", inline=False)
            helpMsg.add_field(name="mcname", value="Input the uuid of a minecraft player, outputs their username", inline=False)
            helpMsg.add_field(name="id", value="Input the discord id of a user, output their username", inline=False)
            helpMsg.add_field(name="Math", value="Allows for short maths equations to be done", inline=False)
            helpMsg.add_field(name="Trello", value="Posts the link to the trello", inline=False)
            helpMsg.add_field(name="Avatar", value="Posts the image of a pinged users avatar", inline=False)
            helpMsg.add_field(name="ID", value="Converts a pinged user to their ID", inline=False)
            helpMsg.add_field(name="Usernames", value="Converts an inputted ID to username", inline=False)
            helpMsg.set_footer(text="Made by SoulWarden#8946")
            helpMsg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=helpMsg)
            
    @help.command(pass_context=True, aliases=["NCO"])
    async def nco(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - NCO Commands", description="All available commands for NCO's. Run _help [command] for further information",color=0x109319)
        embed.add_field(name="Roll", value="Auto rolls the person doing the 8e announcement", inline=False)
        embed.add_field(name="Company Welcome", value="Welcomes a pinged user to the company (8e only currently)", inline=False)
        embed.add_field(name="Annoucement", value="Automatically posts an annoucement with an inputted message (8e only currently)", inline=False)
        embed.add_field(name="Wargames", value="Automatically creates a wargames rotation with pinged users", inline=False)
        embed.add_field(name="Attendance", value="Displays total and company attendance numbers as well as all users in vc's (including mercs and recruits)", inline=False)
        embed.add_field(name="Leadership attendance", value="Creates the leadership attendance form (8e only)", inline=False)
        embed.add_field(name="Split", value="Splits the users in the current voice chat to the other company channel", inline=False)
        embed.add_field(name="Merge", value="Merges the users in both company voice chats to the primary one", inline=False)
        embed.add_field(name="Parade", value="Moves all users in the current connected voice chat to parade ground", inline=False)
        embed.add_field(name="Force parade", value="Moves **all** users in holdfast channels to parade ground", inline=False)
        embed.add_field(name="Spread", value="Moves all users in parade ground to their respective company channel", inline=False)
        embed.add_field(name="Muster", value="Creates the muster roll", inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            
    @help.command(pass_context=True, aliases=["Wargames", "wg", "Wg"])
    async def wargames(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Wargames", description="The wargames command",color=0x109319)
        embed.add_field(name="Command", value="_wargames [user1] [user2] [user3] [user4] [user5] [user6]", inline=False)
        embed.add_field(name="Aliases", value="wargames, Wargames, wg, Wg", inline=False)
        embed.add_field(name="Description", value="Takes up to 6 inputted users and creates a wargames leader rotation", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
                
    @help.command(pass_context=True,aliases=["Dice"])
    async def dice(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Dice", description="The dice command",color=0x109319)
        embed.add_field(name="Command", value="_dice [num]", inline=False)
        embed.add_field(name="Aliases", value="dice, Dice", inline=False)
        embed.add_field(name="Description", value="Takes the inputed number and rolls a virtual dice with that number of sides", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
    @help.command(pass_context=True,aliases=["Username","user","User","name","Name"])
    async def username(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - ID", description="The username command",color=0x109319)
        embed.add_field(name="Command", value="_username [user id]", inline=False)
        embed.add_field(name="Aliases", value="Username, user, User, name, Name", inline=False)
        embed.add_field(name="Description", value="Takes the inputed id and converts it into a username", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
    @help.command(pass_context=True)
    async def mcid(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - McId", description="The mcid command",color=0x109319)
        embed.add_field(name="Command", value="_mcid [Minecraft Username]", inline=False)
        embed.add_field(name="Aliases", value="mcid", inline=False)
        embed.add_field(name="Description", value="Takes the inputed minecraft username and converts it into the UUID", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True)
    async def mcname(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - mcname", description="The mcname command",color=0x109319)
        embed.add_field(name="Command", value="_mcname [Minecraft Username]", inline=False)
        embed.add_field(name="Aliases", value="mcid", inline=False)
        embed.add_field(name="Description", value="Takes the inputed minecraft username and converts it into the UUID", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
    @help.command(pass_context=True, aliases=["Math","Maths","maths"])
    async def math(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Math", description="The math command",color=0x109319)
        embed.add_field(name="Command", value="_math [equation]", inline=False)
        embed.add_field(name="Aliases", value="math, Math, Maths, maths", inline=False)
        embed.add_field(name="Description", value="Takes in a short equation and calculates result. Example: _math 2*3-2, _math 3+2/2, _math 5^2/3)", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
            
    @help.command(pass_context=True, aliases=["comWelcome","comwel","ComWel","Comwel","companywelcome","Companywelcome"])
    async def comWell(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Company Welcome", description="The company welcome command",color=0x109319)
        embed.add_field(name="Command", value="_comWel [Recruit]", inline=False)
        embed.add_field(name="Aliases", value="comWelcome, comwel, ComWel, Comwel, companywelcome, Companywelcome", inline=False)
        embed.add_field(name="Description", value="Takes the inputed user id and posts a welcome message in a specified channel", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
    @help.command(pass_context=True, aliases=["Lazy","lazy","Announcement","announce","Announce"])
    async def announcement(self, ctx):
        embed=discord.Embed(title="IFF Bot - Help - Announcement", description="The annoucement command",color=0x109319)
        embed.add_field(name="Command", value="_announcement [message]", inline=False)
        embed.add_field(name="Aliases", value="announcement, Lazy, lazy, Announcement, announce, Announce", inline=False)
        embed.add_field(name="Description", value="Posts an announcement preset, user must input a message to go along with it. User can manually ping if they want", inline=True)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(helpCog(bot))
