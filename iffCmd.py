from ntpath import join
import discord
from discord.ext import commands
from discord.utils import get
import varStore
from random import randint
import datetime
import asyncio

officers = [
    661521548061966357,
    660353960514813952,
    661522627646586893,
    948862889815597079,
]


class iffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Rolls the person doing the announcement
    @commands.command(aliases=["Roll"])
    # Command, Officer, NCO, Dev
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.has_role(845007589674188839)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    async def roll(self, ctx):
        roll = 0
        while True:
            randId = randint(0, len(varStore.members) - 1)
            roll += 1
            if varStore.members[randId] != varStore.pastSelectId:
                break
        channel = self.bot.get_channel(varStore.logChannel)
        await channel.send(f"Rolled {roll} times in {ctx.guild.name}")

        try:
            f = open(
                "IFF Bot/storage/pastSelectId.txt",
                "w",
            )
        except:
            f = open("/home/pi/Desktop/iffBot/storage/pastSelectId.txt", "w")
        f.write(str(varStore.members[randId]))
        f.close()
        varStore.pastSelectId = varStore.members[randId]
        selectMemberId = varStore.members[randId]
        user = await self.bot.fetch_user(selectMemberId)
        await ctx.send(
            f"<@{selectMemberId}> has been chosen to do the announcement! If you want a template, run '_template' (Although this isn't recommended)"
        )

        activity = discord.Activity(
            type=discord.ActivityType.watching, name=f"{user.name}'s announcement"
        )
        await self.bot.change_presence(status=discord.Status.online, activity=activity)

        cog = self.bot.get_cog("backgroundTasks")
        cog.statusRotation.cancel()
        await asyncio.sleep(600)
        cog = self.bot.get_cog("backgroundTasks")
        cog.statusRotation.start()

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Schedule", "timetable", "Timetable"])
    async def schedule(self, ctx):
        await ctx.reply("Check you dm's!")
        await ctx.message.author.send("Test")

    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.has_role(845007589674188839)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Lazy", "lazy", "Announcement", "announce", "Announce"])
    @commands.guild_only()
    async def announcement(self, ctx, *, message: str):
        channel = self.bot.get_channel(varStore.companyChannel)

        now = datetime.datetime.now()
        day = (now.strftime("%A")).upper()
        
        #embed=discord.Embed(title=f"{day} OCEANIC LINEBATTLE EVENT", description="description", color=0xff0000)
        #embed.add_field(name="field", value="value", inline=False)
        #await ctx.send(embed=embed)

        await channel.send(
            f"::8e: :IFF1:   **══════ {day} Oceanic Linebattle Event══════**   :IFF1: :8e: \n8:00pm AEDT :flag_au: | 7:00pm AEST :flag_au: | 5:00pm AWST :flag_au: | 10:00pm NZDT :flag_nz: \n5:00pm PHT/MYT :flag_ph: :flag_my: :flag_sg: :flag_id: :flag_bn: :flag_hk: | 4:00pm WIT :flag_id: :flag_vn: :flag_th: | 2:30pm IST :flag_in: \n6:00pm KST/JST :flag_kr: :flag_jp: | 05:00am EDT :flag_us: | 9:00am BST :flag_gb: \n \n{message} \n \nThe event starts at **8:00pm AEDT** today \n\nWe have training at **7:00pm AEDT** or 1 hour before the event so make sure you come! \n\nReact 👍 if you'll be attending \nI hope to see all of you coming!"
        )
        await ctx.reply(
            "Please add your own ping/ask a nco for one if you wish", delete_after=5
        )

    # Template command
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=["Template", "temp", "Temp"])
    async def template(self, ctx):
        now = datetime.datetime.now()
        day = (now.strftime("%A")).upper()
        await ctx.reply(
            "Check you dm's! (Making your own announcement is still prefered, only do this if you have little time)"
        )
        await ctx.message.author.send(
            f"::8e: :IFF1:   **══════ {day} OCEANIC LINEBATTLE EVENT══════**   :IFF1: :8e: \n8:00pm AEDT :flag_au: | 7:00pm AEST :flag_au: | 5:00pm AWST :flag_au: | 10:00pm NZDT :flag_nz: \n5:00pm PHT/MYT :flag_ph: :flag_my: :flag_sg: :flag_id: :flag_bn: :flag_hk: | 4:00pm WIT :flag_id: :flag_vn: :flag_th: | 2:30pm IST :flag_in: \n6:00pm KST/JST :flag_kr: :flag_jp: | 05:00am EDT :flag_us: | 9:00am BST :flag_gb: \n \n[Inspirational message] \n \nThe event starts at **8:00pm AEDT** today \n\nWe have training at **7:00pm AEDT** or 1 hour before the event so make sure you come! \n\nReact [Emoji]  if you'll be attending \nI hope to see all of you coming! \n(Ask an officer for a ping)"
        )

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Ranks", "rank", "Rank"])
    async def ranks(self, ctx):
        await ctx.reply("You can find the ranks at")

    # 8e company welcome
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.has_role(845007589674188839)
    @commands.command(
        aliases=[
            "comWelcome",
            "comwel",
            "ComWel",
            "Comwel",
            "companywelcome",
            "Companywelcome", 
        ],
        manage_roles=True,
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    async def comWel(self, ctx, rct: discord.User):
        eightStr = ""
        nineStr = ""
        try:
            file = discord.File(
                "IFF Bot/files/8e.png",
                filename="8e.png",
            )
        except:
            file = discord.File(
                "/home/pi/Desktop/iffBot/files/8e.png", filename="8e.png"
            )

        channel = self.bot.get_channel(varStore.companyChannel)
        embed = discord.Embed(
            title=f"Welcome to the 8e Infantry Company {rct.name}!",
            url="",
            description="The 8e is one of the IFF's 3 infantry companies",
            color=0x109319,
        )
        embed.set_thumbnail(url="attachment://8e.png")
        embed.add_field(
            name="Our Leadership",
            value="Our leadership is made up of Col. Joshlols, Cpt. Bronze, Lt. Ace, SMaj. SoulWarden, SMaj. Rabbi and Sgt. Quack",
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value="Feel free to ask any of them any questions or concerns you have about the IFF, the 8e company or holdfast in general ",
            inline=False,
        )
        embed.add_field(name="\u200b", value="Enjoy your stay here!", inline=True)
        embed.set_author(name=rct.display_name, icon_url=rct.avatar_url)
        await channel.send(file=file, embed=embed)

    # Wargames rotation
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.command(aliases=["Wargames", "wg", "Wg"])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    async def wargames(
        self,
        ctx,
        user1: discord.User = None,
        user2: discord.User = None,
        user3: discord.User = None,
        user4: discord.User = None,
        user5: discord.User = None,
        user6: discord.User = None,
    ):
        users = []
        # Adds all available leaders to a list
        if user1 is not None:
            users.append(user1.id)
        if user2 is not None:
            users.append(user2.id)
        if user3 is not None:
            users.append(user3.id)
        if user4 is not None:
            users.append(user4.id)
        if user5 is not None:
            users.append(user5.id)
        if user6 is not None:
            users.append(user6.id)
        middleIndex = int(len(users) / 2)
        leftUsers = users[:middleIndex]
        rightUsers = users[middleIndex:]
        leftLeaders = []
        rightLeaders = []
        leftCount = 0
        rightCount = 0

        # Creates line leader id lists
        for i in range(7):
            leftLeaders.append(leftUsers[leftCount])
            leftCount += 1
            if leftCount == len(leftUsers):
                leftCount = 0
        for i in range(7):
            rightLeaders.append(rightUsers[rightCount])
            rightCount += 1
            if rightCount == len(rightUsers):
                rightCount = 0

        try:
            file = discord.File(
                "IFF Bot/files/8e.png",
                filename="8e.png",
            )
        except:
            file = discord.File(
                "/home/pi/Desktop/iffBot/files/8e.png", filename="8e.png"
            )
        # Prints line leades
        round = 1
        embed = discord.Embed(
            title="Line leaders",
            description="The line leaders for tonight",
            color=0x109319,
        )
        embed.set_thumbnail(url="attachment://8e.png")
        leftUsers = list(dict.fromkeys(leftUsers))
        leftLeadersStr = ", ".join(str(self.bot.get_user(v)) for v in leftUsers)
        embed.add_field(
            name="Line 1",
            value=f"The line leaders here are {leftLeadersStr}",
            inline=False,
        )
        for i in range(len(leftLeaders)):
            embed.add_field(
                name=f"Round {round}",
                value=f"*{await self.bot.fetch_user(leftLeaders[i])}*",
                inline=True,
            )
            round += 1

        round = 1
        rightUsers = list(dict.fromkeys(rightUsers))
        rightLeadersStr = ", ".join(str(self.bot.get_user(v)) for v in rightUsers)
        embed.add_field(
            name="Line 2",
            value=f"The line leaders here are {rightLeadersStr}",
            inline=False,
        )
        for i in range(len(rightLeaders)):
            embed.add_field(
                name=f"Round {round}",
                value=f"*{await self.bot.fetch_user(rightLeaders[i])}*",
                inline=True,
            )
            round += 1
        await ctx.send(file=file, embed=embed)

    #Total IFF attendance cmd
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(name = "attendance", aliases=["Attendance","attend"])
    async def attendance(self, ctx:commands.Context):
        vcCatId = 948180967607136306
        iffGuild = self.bot.get_guild(592559858482544641)
        vcChannelsIds = []
        totalUsers = 0
        channelUsers = []
        sevenUsers = []
        eightUsers = []
        nineUsers = []
        fourUsers = []
        otherUsers = []
        
        for channel in iffGuild.voice_channels:
            if channel.category_id == vcCatId:
                vcChannelsIds.append(channel.id)
                
        for channelId in vcChannelsIds:
            channel = self.bot.get_channel(channelId)
            channelUsers.append(channel.members)
            totalUsers += len(channel.members)
        
        role = discord.utils.find(
            lambda r: r.name == "7e Voltigeurs de la Garde", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    sevenUsers.append(x.display_name)
                    
        
        role = discord.utils.find(
            lambda r: r.name == "8e Chasseurs de la Garde", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    eightUsers.append(x.display_name)
                    
                    
        role = discord.utils.find(
            lambda r: r.name == "9e Grenadiers de la Garde", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    nineUsers.append(x.display_name)
                    
                    
        role = discord.utils.find(
            lambda r: r.name == "4e Batterie d'Artillerie à Pied", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    fourUsers.append(x.display_name)
                    
        role = discord.utils.find(
            lambda r: r.name == "La Recrue (Recruit)", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    otherUsers.append(x.display_name)
                    
        role = discord.utils.find(
            lambda r: r.name == "Mercenary", iffGuild.roles
        )
        
        for user in channelUsers:
            for x in user:
                if role in x.roles:
                    otherUsers.append(x.display_name)
                    
        fourStr = ", ".join(fourUsers)
        sevenStr = ", ".join(sevenUsers)
        eightStr = ", ".join(eightUsers)
        nineStr = ", ".join(nineUsers)
        otherStr = ", ".join(otherUsers)
        
        ncoChannel = self.bot.get_channel(954194296809095188)
        
        embed=discord.Embed(title="IFF Attendance", description="Current IFF attendance", color=0x151798)
        embed.add_field(name=f"Total Players", value=f"{totalUsers}", inline=False)
        embed.add_field(name=f"4e Players (Total: {len(fourUsers)})", value=f"\u200b{fourStr}", inline=False)
        embed.add_field(name=f"7e Players (Total: {len(sevenUsers)})", value=f"\u200b{sevenStr}", inline=False)
        embed.add_field(name=f"8e Players (Total: {len(eightUsers)})", value=f"\u200b{eightStr}", inline=False)
        embed.add_field(name=f"9e Players (Total: {len(nineUsers)})", value=f"\u200b{nineStr}", inline=False)
        embed.add_field(name=f"Other Players (Total: {len(otherUsers)})", value=f"\u200b{otherStr}", inline=False)
        await ncoChannel.send(embed=embed)
        
    #Leadership attendance ping
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["leadattend","leadershipAttendnace"])
    async def leadAttend(self, ctx):
        leadershipChannel = self.bot.get_channel(907599229629911104)

        embed = discord.Embed(
            title="Leadership Attendance",
            description="React with :thumbsup: or :thumbsdown: if you're coming tonight",
            color=0x109319,
        )
        embed.add_field(name="Coming: ", value=f"No one :(", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Not coming: ", value=f"No one :(", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)
        embed.add_field(name="Maybe coming: ", value=f"No one :(", inline=False)
        embed.add_field(name="Count: ", value=f"0", inline=False)

        msg = await leadershipChannel.send(embed=embed)

        await msg.add_reaction("\N{THUMBS UP SIGN}")
        await msg.add_reaction("\N{THUMBS DOWN SIGN}")
        await msg.add_reaction("\N{SHRUG}")

        varStore.leaderPingMsgId = msg.id
        
    #Auto line split
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Split"])
    async def split(self,ctx):
        voiceChannelUsers = ctx.author.voice.channel.members
        
        sevenVcs = [872101027682324540, 872056405052510238]
        eightVcs = [869519564973703228, 840889769713205248]
        nineVcs = [872101199028043866, 864013586774491187, 953219379590488134]
        
        await ctx.reply("Splitting")
        
        #7e
        role = discord.utils.find(
                    lambda r: r.name == "7e Voltigeurs de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            if ctx.author.voice.channel.id == sevenVcs[0]:
                otherVc = self.bot.get_channel(sevenVcs[1])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1
            elif ctx.author.voice.channel.id == (sevenVcs[1]):
                otherVc = self.bot.get_channel(sevenVcs[0])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1

        #8e
        role = discord.utils.find(
                    lambda r: r.name == "8e Chasseurs de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            if ctx.author.voice.channel.id == eightVcs[0]:
                otherVc = self.bot.get_channel(eightVcs[1])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1
            elif ctx.author.voice.channel.id == (eightVcs[1]):
                otherVc = self.bot.get_channel(eightVcs[0])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1
                
        #9e
        role = discord.utils.find(
                    lambda r: r.name == "9e Grenadiers de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            if ctx.author.voice.channel.id == (nineVcs[0]):
                otherVc = self.bot.get_channel(nineVcs[1])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1
            elif ctx.author.voice.channel.id == (nineVcs[1]):
                otherVc = self.bot.get_channel(nineVcs[0])
                i = 0
                for user in voiceChannelUsers:
                    if i == 1:
                        await user.move_to(otherVc)
                        i = 0
                    else:
                        i = 1
                        
    #Merge command
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only() 
    @commands.cooldown(1, 10, commands.BucketType.guild)               
    @commands.command(aliases=["Merge"])
    async def merge(self, ctx):
        await ctx.reply("Merging")
        #7e
        role = discord.utils.find(
                    lambda r: r.name == "7e Voltigeurs de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            firstVc = self.bot.get_channel(872101027682324540)
            secondVc = self.bot.get_channel(872056405052510238)
            for user in secondVc.members:
                await user.move_to(firstVc)

        #8e
        role = discord.utils.find(
                    lambda r: r.name == "8e Chasseurs de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            firstVc = self.bot.get_channel(869519564973703228)
            secondVc = self.bot.get_channel(840889769713205248)
            for user in secondVc.members:
                await user.move_to(firstVc)
                
        #9e
        role = discord.utils.find(
                    lambda r: r.name == "9e Grenadiers de la Garde",
                    ctx.message.guild.roles,
                )
        if role in ctx.author.roles:
            firstVc = self.bot.get_channel(872101199028043866)
            secondVc = self.bot.get_channel(864013586774491187)
            for user in secondVc.members:
                await user.move_to(firstVc)
        
        
    #Move all users in current vc to parade ground
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Parade"])
    async def parade(self, ctx):
        await ctx.reply("Moving users now")
        paradeGround = self.bot.get_channel(757782109275553863)
        connectedUsers = ctx.author.voice.channel.members
        
        for user in connectedUsers:
            await user.move_to(paradeGround)
            
    #Move everyone to parade ground
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["Forceparade","unfuck","return"])
    async def forceparade(self, ctx):
        async with ctx.channel.typing():
            await ctx.reply("Moving users now")
            vcCatId = 948180967607136306
            paradeGround = self.bot.get_channel(757782109275553863)
            
            for channel in ctx.guild.voice_channels:
                if channel.category_id == vcCatId and channel.category_id != 757782109275553863 and channel.category_id != 853615447261446144:
                    for user in channel.members:
                        await user.move_to(paradeGround)
        await ctx.reply("Done!")
                
    #Spread command
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Spread","fuckoff"])
    async def spread(self, ctx):
        paradeGround = self.bot.get_channel(757782109275553863)
        sevenChannel = self.bot.get_channel(872101027682324540)
        eightChannel = self.bot.get_channel(869519564973703228)
        nineChannel = self.bot.get_channel(872101199028043866)
        fourChannel = self.bot.get_channel(660358590925897769)
        
        await ctx.reply("Spreading users now")
        
        for user in paradeGround.members:
            sevenRole = discord.utils.find(
                lambda r: r.name == "7e Voltigeurs de la Garde",
                ctx.message.guild.roles,
            )
            
            eightRole = discord.utils.find(
                lambda r: r.name == "8e Chasseurs de la Garde",
                ctx.message.guild.roles,
            )
            
            nineRole = discord.utils.find(
                lambda r: r.name == "9e Grenadiers de la Garde",
                ctx.message.guild.roles,
            )
            
            fourRole = discord.utils.find(
                lambda r: r.name == "4e Batterie d'Artillerie à Pied",
                ctx.message.guild.roles,
            )      
            
            if sevenRole in user.roles:
                await user.move_to(sevenChannel)
            elif eightRole in user.roles:
                await user.move_to(eightChannel)
            elif nineRole in user.roles:
                await user.move_to(nineChannel)
            elif fourRole in user.roles:
                await user.move_to(fourChannel)
            else:
                await ctx.reply("Please move the mercs/recruits to the appropriate channel") 
    
    #Service medal calculator     
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Service"])
    async def service(self, ctx):
        iffRole = get(ctx.guild.roles, id = 611927973838323724)
        retiredRole = get(ctx.guild.roles, id= 707125172699660288)
        retiredLeadership = get(ctx.guild.roles, id= 887542975821905970)
        bronzeMeritRole =  get(ctx.guild.roles, id= 795254224660725771)
        silverMeritRole = get(ctx.guild.roles, id= 914254355610337341)
        goldMeritRole = get(ctx.guild.roles, id= 914256745491230720)
        platMeritRole = get(ctx.guild.roles, id= 914257554723442688)
        bronzeMerit = [] #6 months
        silverMerit = [] #1 years
        goldMerit = [] #2 years
        platMerit = [] #3 years
                      
        for user in ctx.guild.members:
            if iffRole in user.roles and retiredRole not in user.roles and retiredLeadership not in user.roles:
                duration = int((datetime.datetime.now() - user.joined_at).days)
                if duration >= 183:
                    if bronzeMeritRole not in user.roles:
                        bronzeMerit.append(user.display_name)
                if duration >= 365:
                    if silverMeritRole not in user.roles:
                        silverMerit.append(user.display_name)
                if duration >= 730:
                    if goldMeritRole not in user.roles:
                        goldMerit.append(user.display_name)
                if duration >= 1095:
                    if platMeritRole not in user.roles:
                        platMerit.append(user.display_name)
                    
        embed=discord.Embed(title="Service Medals", description="All the users who need to be awarded service medals", color=0xff0000)
        embed.add_field(name="Bronze Military Merit", value=", ".join(bronzeMerit) + "\u200b", inline=False)
        embed.add_field(name="Silver Military Merit", value=", ".join(silverMerit) + "\u200b", inline=False)
        embed.add_field(name="Gold Military Merit", value=", ".join(goldMerit) + "\u200b", inline=False)
        embed.add_field(name="Platinum Military Merit", value=", ".join(platMerit) + "\u200b", inline=False)
        await ctx.send(embed=embed)
        
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Rctform", "rctForm", "RctForm"])
    async def rctform(self, ctx):
        await ctx.send("""
        **Copy/Paste and answer the following questions to access the server**
Please check <#853180535303176213>, <#910247350923059211> and <#853180574957043712> before you answer
```**What is your new Holdfast ingame name?** IFF | Name

**What region/timezone are you from? (e.g. Australia, South East Asia, NA, etc.)**

**How did you find out about the IFF?**

**Have you joined the in-game IFF regiment registry?**

**Do you agree with our rules and discord ToS?**
@Recruiter ```""")
        
    #Muster role
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Muster"])
    async def muster(self, ctx):
        async with ctx.channel.typing():
            fourCoList = []
            sevenCoList = []
            eightCoList = []
            nineCoList = []
            fourNcoList = []
            sevenNcoList = []
            eightNcoList = []
            nineNcoList = []
            fourCplList = []
            sevenCplList = []
            eightCplList = []
            nineCplList = []
            fourEnlistedList = []
            sevenEnlistedList = []
            eightEnlistedList = []
            nineEnlistedList = []

            fourEnlistedCount = 0
            sevenEnlistedCount = 0
            eightEnlistedCount = 0
            nineEnlistedCount = 0
            
            # 4e -----------------------------------------------
            role = discord.utils.find(
                lambda r: r.name == "4e Batterie d'Artillerie à Pied", ctx.message.guild.roles
            )
            for user in ctx.guild.members:
                if role in user.roles:
                    # Co list
                    role = discord.utils.find(
                        lambda r: r.name == "Commissioned Officer", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        if '"Cpt. ' in user.display_name:
                            nick = (user.display_name).replace('"Cpt. ', "Capitaine ")
                            fourCoList.append(nick)
                        elif '"Lt.' in user.display_name:
                            nick = (user.display_name).replace('"Lt. ', "Lieutenant ")
                            fourCoList.append(nick)
                    fourCoList.sort(reverse=True)

                    # NCO list
                    role = discord.utils.find(
                        lambda r: r.name == "Non-Commissioned Officer",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "'SMaj." in user.display_name:
                            nick = (user.display_name).replace("'SMaj. ", "Sergeant Major ")
                            fourNcoList.append(nick)
                        elif "'Sgt." in user.display_name:
                            nick = (user.display_name).replace("'Sgt. ", "Sergeant ")
                            fourNcoList.append(nick)
                    fourNcoList.sort(reverse=True)

                    # Cpl list
                    role = discord.utils.find(
                        lambda r: r.name == "Corporal", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        nick = user.display_name
                        nick = nick.replace(".Cpl. ", "Corporal ")
                        fourCplList.append(nick)
                    fourCplList.sort()

                    # Enlisted list
                    role = discord.utils.find(
                        lambda r: r.name == "4e Batterie d'Artillerie à Pied",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "Sdt." in user.display_name:
                            fourEnlistedCount += 1
                        elif "Fus. " in user.display_name:
                            fourEnlistedCount += 1
                        elif "Volt. " in user.display_name:
                            fourEnlistedCount += 1
                        elif "Chas. " in user.display_name:
                            nick = (user.display_name).replace("Chas. ", "Chasseur ")
                            fourEnlistedList.append(nick)
                        elif "Gda. " in user.display_name:
                            nick = (user.display_name).replace("Gda. ", "Gendarme ")
                            fourEnlistedList.append(nick)
                        elif "Lans. " in user.display_name:
                            nick = (user.display_name).replace("Lans. ", "Lanspessade ")
                            fourEnlistedList.append(nick)
                        elif "Gren. " in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadier ")
                            fourEnlistedList.append(nick)
                        elif "Gde. " in user.display_name:
                            nick = (user.display_name).replace(
                                "Gde. ", "Grenadier de Elite "
                            )
                            fourEnlistedList.append(nick)

                        fourEnlistedList.sort(reverse=True)

            # 7e -----------------------------------------------
            role = discord.utils.find(
                lambda r: r.name == "7e Voltigeurs de la Garde", ctx.message.guild.roles
            )
            for user in ctx.guild.members:
                if role in user.roles:
                    # Co list
                    role = discord.utils.find(
                        lambda r: r.name == "Commissioned Officer", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        if 'Cpt.' in user.display_name:
                            nick = (user.display_name).replace('Cpt. ', "Capitaine ")
                            sevenCoList.append(nick)
                        elif 'Lt.' in user.display_name:
                            nick = (user.display_name).replace('Lt. ', "Lieutenant ")
                            sevenCoList.append(nick)
                    sevenCoList.sort(reverse=True)

                    # NCO list
                    role = discord.utils.find(
                        lambda r: r.name == "Non-Commissioned Officer",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "'SMaj." in user.display_name:
                            nick = (user.display_name).replace("'SMaj. ", "Sergeant Major ")
                            sevenNcoList.append(nick)
                        elif "'Sgt." in user.display_name:
                            nick = (user.display_name).replace("'Sgt. ", "Sergeant ")
                            sevenNcoList.append(nick)
                    sevenNcoList.sort(reverse=True)

                    # Cpl list
                    role = discord.utils.find(
                        lambda r: r.name == "Corporal", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        nick = user.display_name
                        nick = nick.replace(".Cpl. ", "Corporal ")
                        sevenCplList.append(nick)
                    sevenCplList.sort()

                    # Enlisted list
                    role = discord.utils.find(
                        lambda r: r.name == "7e Voltigeurs de la Garde",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "Sdt." in user.display_name and "[" not in user.display_name:
                            sevenEnlistedCount += 1
                        elif "Fus. " in user.display_name and "[" not in user.display_name:
                            sevenEnlistedCount += 1
                        elif "Volt. " in user.display_name and "[" not in user.display_name:
                            sevenEnlistedCount += 1
                        elif "Chas. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Chas. ", "Chasseur ")
                            sevenEnlistedList.append(nick)
                        elif "Gda. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gda. ", "Gendarme ")
                            sevenEnlistedList.append(nick)
                        elif "Lans. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Lans. ", "Lanspessade ")
                            sevenEnlistedList.append(nick)
                        elif "Gren. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadier ")
                            sevenEnlistedList.append(nick)
                        elif "Gde. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace(
                                "Gde. ", "Grenadier de Elite "
                            )
                            sevenEnlistedList.append(nick)

                        sevenEnlistedList.sort(reverse=True)

            # 8e -------------------------------------------
            role = discord.utils.find(
                lambda r: r.name == "8e Chasseurs de la Garde", ctx.message.guild.roles
            )
            for user in ctx.guild.members:
                if role in user.roles:
                    # Co list
                    role = discord.utils.find(
                        lambda r: r.name == "Commissioned Officer", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        if '"Cpt. ' in user.display_name:
                            nick = (user.display_name).replace('"Cpt. ', "Capitaine ")
                            eightCoList.append(nick)
                        elif '"Lt.' in user.display_name:
                            nick = (user.display_name).replace('"Lt. ', "Lieutenant ")
                            eightCoList.append(nick)
                    eightCoList.sort(reverse=True)

                    # NCO list
                    role = discord.utils.find(
                        lambda r: r.name == "Non-Commissioned Officer",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "'SMaj." in user.display_name:
                            nick = (user.display_name).replace("'SMaj. ", "Sergeant Major ")
                            eightNcoList.append(nick)
                        elif "'Sgt." in user.display_name:
                            nick = (user.display_name).replace("'Sgt. ", "Sergeant ")
                            eightNcoList.append(nick)
                    eightNcoList.sort(reverse=True)

                    # Cpl list
                    role = discord.utils.find(
                        lambda r: r.name == "Corporal", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        nick = user.display_name
                        nick = nick.replace(".Cpl. ", "Corporal ")
                        eightCplList.append(nick)
                    eightCplList.sort()

                    # Enlisted list
                    role = discord.utils.find(
                        lambda r: r.name == "8e Chasseurs de la Garde",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "Sdt." in user.display_name and "[" not in user.display_name:
                            eightEnlistedCount += 1
                        elif "Fus. " in user.display_name and "[" not in user.display_name:
                            eightEnlistedCount += 1
                        elif "Volt. " in user.display_name and "[" not in user.display_name:
                            eightEnlistedCount += 1
                        elif "Chas. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Chas. ", "Chasseur ")
                            eightEnlistedList.append(nick)
                        elif "Gda. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gda. ", "Gendarme ")
                            eightEnlistedList.append(nick)
                        elif "Lans. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Lans. ", "Lanspessade ")
                            eightEnlistedList.append(nick)
                        elif "Gren. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadier ")
                            eightEnlistedList.append(nick)
                        elif "Gde. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace(
                                "Gde. ", "Grenadier de Elite "
                            )
                            eightEnlistedList.append(nick)

                        eightEnlistedList.sort(reverse=True)

            # 9e ---------------------------------------------
            role = discord.utils.find(
                lambda r: r.name == "9e Grenadiers de la Garde", ctx.message.guild.roles
            )
            for user in ctx.guild.members:
                if role in user.roles:
                    # Co list
                    role = discord.utils.find(
                        lambda r: r.name == "Commissioned Officer", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        if '"Cpt.' in user.display_name:
                            nick = (user.display_name).replace('"Cpt. ', "Capitaine ")
                            nineCoList.append(nick)
                        elif '"Lt.' in user.display_name:
                            nick = (user.display_name).replace('"Lt. ', "Lieutenant ")
                            nineCoList.append(nick)
                    nineCoList.sort(reverse=True)

                    # NCO list
                    role = discord.utils.find(
                        lambda r: r.name == "Non-Commissioned Officer",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "'SMaj." in user.display_name:
                            nick = (user.display_name).replace("'SMaj. ", "Sergeant Major ")
                            nineNcoList.append(nick)
                        elif "'Sgt." in user.display_name:
                            nick = (user.display_name).replace("'Sgt. ", "Sergeant ")
                            nineNcoList.append(nick)
                    nineNcoList.sort(reverse=True)

                    # Cpl list
                    role = discord.utils.find(
                        lambda r: r.name == "Corporal", ctx.message.guild.roles
                    )
                    if role in user.roles:
                        nick = user.display_name
                        nick = nick.replace(".Cpl. ", "Corporal ")
                        nineCplList.append(nick)
                    nineCplList.sort()

                    # Enlisted list
                    role = discord.utils.find(
                        lambda r: r.name == "9e Grenadiers de la Garde",
                        ctx.message.guild.roles,
                    )
                    if role in user.roles:
                        if "Sdt." in user.display_name and "[" not in user.display_name:
                            nineEnlistedCount += 1
                        elif "Fus. " in user.display_name and "[" not in user.display_name:
                            nineEnlistedCount += 1
                        elif "Volt. " in user.display_name and "[" not in user.display_name:
                            nineEnlistedCount += 1
                        elif "Chas. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Chas. ", "Chasseur ")
                            nineEnlistedList.append(nick)
                        elif "Gda. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gda. ", "Gendarme ")
                            nineEnlistedList.append(nick)
                        elif "Lans. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Lans. ", "Lanspessade ")
                            nineEnlistedList.append(nick)
                        elif "Gren. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadier ")
                            nineEnlistedList.append(nick)
                        elif "Gde. " in user.display_name and "[" not in user.display_name:
                            nick = (user.display_name).replace(
                                "Gde. ", "Grenadier de Elite "
                            )
                            nineEnlistedList.append(nick)

                        nineEnlistedList.sort(reverse=True)

            sevenCoStr = "\n".join(sevenCoList)
            eightCoStr = "\n".join(eightCoList)
            nineCoStr = "\n".join(nineCoList)
            fourCoStr = "\n".join(fourCoList)
            sevenNcoStr = "\n".join(sevenNcoList)
            eightNcoStr = "\n".join(eightNcoList)
            nineNcoStr = "\n".join(nineNcoList)
            fourNcoStr = "\n".join(fourNcoList)
            sevenCplStr = "\n".join(sevenCplList)
            eightCplStr = "\n".join(eightCplList)
            nineCplStr = "\n".join(nineCplList)
            fourCplStr = "\n".join(fourCplList)
            sevenEnlistedStr = "\n".join(sevenEnlistedList)
            eightEnlistedStr = "\n".join(eightEnlistedList)
            nineEnlistedStr = "\n".join(nineEnlistedList)
            fourEnlistedStr = "\n".join(fourEnlistedList)

            # Command skin 1 pic
            try:
                cmdImg = discord.File(
                    "IFF Bot/files/cmd_skin.png",
                    filename="cmd_skin.png",
                )
            except:
                cmdImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/cmd_skin.png", filename="cmd_skin.png"
                )
                
            # Command skin 2 pic
            try:
                cmd2Img = discord.File(
                    "IFF Bot/files/cmd_skin2.png",
                    filename="cmd_skin2.png",
                )
            except:
                cmd2Img = discord.File(
                    "/home/pi/Desktop/iffBot/files/cmd_skin2.png", filename="cmd_skin2.png"
                )

            # 4e skin pic
            try:
                fourImg = discord.File(
                    "IFF Bot/files/4e_skin.jpeg",
                    filename="4e_skin.jpeg",
                )
            except:
                fourImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/4e_skin.jpeg", filename="4e_skin.jpeg"
                )

            # 7e skin pic
            try:
                sevenImg = discord.File(
                    "IFF Bot/files/7e_skin.png",
                    filename="7e_skin.png",
                )
            except:
                sevenImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/7e_skin.png", filename="7e_skin.png"
                )

            # 8e skin pic
            try:
                eightImg = discord.File(
                    "IFF Bot/files/8e_skin.png",
                    filename="8e_skin.png",
                )
            except:
                eightImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/8e_skin.png", filename="8e_skin.png"
                )

            # 9e skin pic
            try:
                nineImg = discord.File(
                    "IFF Bot/files/9e_skin.png",
                    filename="9e_skin.png",
                )
            except:
                nineImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/9e_skin.png", filename="9e_skin.png"
                )
                
            # Admin skin pic
            try:
                adminImg = discord.File(
                    "IFF Bot/files/admin_skin.png",
                    filename="admin_skin.png",
                )
            except:
                adminImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/admin_skin.png", filename="admin_skin.png"
                )
                
            # Cav skin pic
            try:
                cavImg = discord.File(
                    "IFF Bot/files/cav_skin.png",
                    filename="cav_skin.png",
                )
            except:
                cavImg = discord.File(
                    "/home/pi/Desktop/iffBot/files/cav_skin.png", filename="cav_skin.png"
                )
                

            # ADD FOUR E

            # Command Col----------------------------------------------------
            cmd1Embed=discord.Embed(title="Imperial Frontier Force 1ic", description="", color=0xffff00)
            cmd1Embed.set_thumbnail(url="attachment://cmd_skin.png")
            cmd1Embed.add_field(name="Colonel Joshlols", value="8e Chasseurs de la Garde Commander\nJäger Karabiner Infanterie Commander", inline=False)
            
            # Command 2ic----------------------------------------------------
            cmd2Embed=discord.Embed(title="Imperial Frontier Force 2ic", description="", color=0xffff00)
            cmd2Embed.set_thumbnail(url="attachment://cmd_skin2.png")
            cmd2Embed.add_field(name="Aide de Camp Ballistic", value="Head Adjutant\n9e Grenadiers de la Garde's biggest fan", inline=False)
            
            # 7e ---------------------------------------------------------------------
            sevenEmbed = discord.Embed(
                title="7e Voltigeurs de la Garde",
                description="Muster roll for 7e",
                color=0xb12222,
            )
            sevenEmbed.set_thumbnail(url="attachment://7e_skin.png")
            sevenEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{sevenCoStr}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Non-Commissioned Officers",
                value=f"\u200b{sevenNcoStr}",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Corporals", value=f"\u200b{sevenCplStr}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{sevenEnlistedStr}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Soldats → Voltigeurs",
                value=f"\u200b{sevenEnlistedCount}",
                inline=False,
            )

            # 8e ---------------------------------------------------------------------
            eightEmbed = discord.Embed(
                title="8e Chasseurs de la Garde",
                description="Muster roll for 8e",
                color=0x1f8b4c,
            )
            eightEmbed.set_thumbnail(url="attachment://8e_skin.png")
            eightEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{eightCoStr}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Non-Commissioned Officers",
                value=f"\u200b{eightNcoStr}",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Corporals", value=f"\u200b{eightCplStr}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{eightEnlistedStr}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Soldats → Voltigeurs",
                value=f"\u200b{eightEnlistedCount}",
                inline=False,
            )

            # 9e ---------------------------------------------------------------------
            nineEmbed = discord.Embed(
                title="9e Grenadiers de la Garde",
                description="Muster roll for 9e",
                color=0x206694,
            )
            nineEmbed.set_thumbnail(url="attachment://9e_skin.png")
            nineEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{nineCoStr}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Non-Commissioned Officers", value=f"\u200b{nineNcoStr}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Corporals", value=f"\u200b{nineCplStr}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{nineEnlistedStr}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Soldats → Voltigeurs",
                value=f"\u200b{nineEnlistedCount}",
                inline=False,
            )
            
            # 4e ---------------------------------------------------------------------
            fourEmbed = discord.Embed(
                title="4e Batterie d'Artillerie à Pied",
                description="Muster roll for 4e",
                color=0x87cfeb,
            )
            fourEmbed.set_thumbnail(url="attachment://4e_skin.jpeg")
            fourEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{fourCoStr}", inline=False
            )
            fourEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            fourEmbed.add_field(
                name=f"Non-Commissioned Officers", value=f"\u200b{fourNcoStr}", inline=False
            )
            fourEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            fourEmbed.add_field(
                name=f"Corporals", value=f"\u200b{fourCplStr}", inline=False
            )
            fourEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            fourEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{fourEnlistedStr}", inline=False
            )
            fourEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            fourEmbed.add_field(
                name=f"Soldats → Voltigeurs",
                value=f"\u200b{fourEnlistedCount}",
                inline=False,
            )
            
            #Could automate admins in future
            #Admins ------------------------------------------------------
            adminEmbed=discord.Embed(title="I 'Administration Regimentaire", description="", color=0xe74c25)
            adminEmbed.set_thumbnail(url="attachment://admin_skin.png")
            adminEmbed.add_field(name="Commissioned Officer", value="Adjutant Peenoire", inline=False)
            adminEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            adminEmbed.add_field(name="Non-Commissioned Officer", value="Sous-Adjutant Ping\nSous-Adjutant Minz", inline=False)
            
            #Specials ------------------------------------------------------
            specEmbed=discord.Embed(title="Non-Infantry Specialisation Leadership", description="Leadership for the specialisations and Auxiliary you may gain quals for and play as during events.", color=0xf8e61c    )
            specEmbed.set_thumbnail(url="attachment://cav_skin.png")
            specEmbed.add_field(name="Jäger Karabiner Infanterie", value="Colonel Joshlols", inline=False)
            specEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            specEmbed.add_field(name="Garde Chevau-Léger", value="Capitaine Bronze\nLieutenant Ace", inline=False)
            specEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            specEmbed.add_field(name="Auxiliaire de vie à Pied", value="Capitaine Tobakshi (Aux)\nGendarme Milk (Sapper)", inline=False)

        await ctx.send(file=cmdImg,embed=cmd1Embed)
        await ctx.send(file=cmd2Img,embed=cmd2Embed)
        await ctx.send(file=sevenImg, embed=sevenEmbed)
        await ctx.send(file=eightImg, embed=eightEmbed)
        await ctx.send(file=nineImg, embed=nineEmbed)
        await ctx.send(file=fourImg, embed=fourEmbed)
        await ctx.send(file=adminImg, embed=adminEmbed)
        await ctx.send(file=cavImg, embed=specEmbed)

def setup(bot):
    bot.add_cog(iffCog(bot))
