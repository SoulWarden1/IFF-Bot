import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import varStore
from random import randint
from datetime import datetime
import asyncio
from pathlib import Path


officers = [
    990267891330977813, #Reg HQ
    661521548061966357, #Company Cmd
    660353960514813952, #CO
    661522627646586893, #NCO
    948862889815597079,
]

class enlistForm(discord.ui.Modal, title='IFF Enlistment Form'):
    def __init__(self, start, bot):
        self.start = start
        self.bot = bot
        super().__init__()

    name = discord.ui.TextInput(
        label='What is your username you use for Holdfast?',
        placeholder='Enter username here...',
        required = True,
        max_length = 20,
    )

    region = discord.ui.TextInput(
        label="What region are you from?",
        placeholder='OCE, NA, SEA, ETC. If from SEA, please state your country',
        required = True,
        max_length = 20,
    )

    game = discord.ui.TextInput(
        label='Please list the games you are here for:',
        placeholder='Holdfast, Arma',
        required = True,
        max_length = 8,
        min_length = 2,
    )

    find = discord.ui.TextInput(
        label='How did you find out about the IFF?',
        placeholder='Enter reason/source here...',
        required = True,
        style = discord.TextStyle.long,
        max_length = 150,
    )

    rules = discord.ui.TextInput(
        label='Do you agree with our rules and discord ToS?',
        placeholder='Yes/No...',
        default = "Yes",
        required = True,
        max_length = 3,
        min_length = 2,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Setup to get roles to assign to rct
        rctRole = interaction.guild.get_role(845563588324098058)
        iffRole = interaction.guild.get_role(611927973838323724)
        nickRole = interaction.guild.get_role(893824145299746816)
        newcomerRole = interaction.guild.get_role(627801587351289856)
        bannerlordRole = interaction.guild.get_role(1058392135847661598)
        holdfastRole = interaction.guild.get_role(1058390730378334328)
        iffBotTestChannel = self.bot.get_channel(954194296809095188)
        enlistmentLogChannel = self.bot.get_channel(592560417394393098)
        end = datetime.now()

        # Sends embed contained enlistment info
        embed=discord.Embed(title=f"{interaction.user.name}'s Enlistment Form", description=f"It took {end-self.start}s to filled out. Completed on {end.strftime('%d/%m/%Y on %a %I:%M:%S %p %Z')}",color=0x141599)
        embed.add_field(name="Name", value=f"{self.name.value}", inline=False)
        embed.add_field(name="Region", value=f"{self.region.value}", inline=False)
        embed.add_field(name="Game", value=f"{self.game.value}", inline=False)
        embed.add_field(name="Find the IFF", value=f"{self.find.value}", inline=False)
        embed.add_field(name="Rules", value=f"{self.rules.value}", inline=False)
        embed.set_footer(text = f"User ID: {interaction.user.id}")
        embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)

        await interaction.response.send_message(f'Enlistment successful! Welcome to the Imperial Frontier Force, {self.name.value}! Your tags will be given shortly. If there are any issues with your tags please let an officer or nco know.', ephemeral=True)
        await enlistmentLogChannel.send(embed=embed)

        # Auto generates welcome message


        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{self.name.value}'s enlistment"))
        await asyncio.sleep(5)

        await interaction.user.remove_roles(newcomerRole, reason = "Bot removing newcomer role")
        await interaction.user.edit(nick=f"Rct. {self.name.value}")
        await interaction.user.add_roles(rctRole, iffRole, nickRole, reason = "Bot adding recruit roles")

        #HOLDFAST
        if "HOLDFAST" in (self.game.value).upper():
            await interaction.user.add_roles(holdfastRole, reason = "Bot adding holdfast role")
            await enlistmentLogChannel.send(f"<@{interaction.user.id}> was given the **Holdfast** game role")
            await iffBotTestChannel.send(f"""
Welcome message for {self.name.value}/<@{interaction.user.id}>

```:IFF4: **WELCOME TO THE IMPERIAL FRONTIER FORCE** :IFF4:

Everyone welcome <@{interaction.user.id}> to the Imperial Frontier Force!

Make sure you change your in-game name to `IFF | Rct. {self.name.value}` during events and to join the in-game regiment registry!

**__CHECK OUT THESE AWESOME CHANNELS!__**
#🍻︱mess-hall - Where we chat everything up!
#🏰︱announcements - For information about upcoming events!
#🥇︱medals-and-ribbons - For information about achievements within the IFF!
#🎮︱games - For the other games we play!

#💻︱server-info - For the mods we use in event servers! (Recommended to pre-subscribe for faster loading times)


Feel free to tag any Officer or NCO if you have any questions!```
""")
        # Arma
        elif "ARMA" in (self.game.value).upper():
            await interaction.user.add_roles(bannerlordRole, reason = "Bot adding bannerlord roles")
            await enlistmentLogChannel.send(f"<@{interaction.user.id}> was given the **Bannerlord** game role")
            await iffBotTestChannel.send(f"""
Welcome message for {self.name.value}/<@{interaction.user.id}>

```:IFF4: **WELCOME TO THE IMPERIAL FRONTIER FORCE** :IFF4:

Everyone welcome <@{interaction.user.id}> to the Imperial Frontier Force!

Make sure you change your in-game name to `3IC | IFF | {self.name.value}` during events by going to the Oceanic S&M server and typing !nick 3IC | IFF | {self.name.value}!

**__CHECK OUT THESE AWESOME CHANNELS!__**
#🍻︱mess-hall - Where we chat everything up!
#🏰︱announcements - For information about upcoming events!
#🎮︱games - For the other games we play!

Feel free to tag any Officer or NCO if you have any questions!```
""")
        else:
            await enlistmentLogChannel.send(f"<@{interaction.user.id}> was given **no** game roles")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('An error has occurred, if this issue persists please contact SoulWarden#8946', ephemeral=True)
        print(f"An error occurred with the enlistment form: {error}")

class iffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.event_vc_category_id = 948180967607136306

    @commands.command(name = "test")
    async def test(self, ctx):
        print(ctx.author.is_on_mobile())

    @app_commands.checks.has_any_role(
        990267891330977813,#Reg HQ
        661521548061966357, #Company Cmd
        660353960514813952, #CO
        661522627646586893, #NCO
        948862889815597079, #Bot dev
        627801587351289856 #Newcomer
        )
    @app_commands.guild_only()
    @app_commands.command(name="enlist", description='The IFF enlistment form')
    async def enlist(self, interaction: discord.Interaction):
        await interaction.response.send_modal(enlistForm(start = datetime.now(), bot = self.bot))

    # Rolls the person doing the announcement
    @commands.has_any_role(
        907603010438459402, 907603359048040488, 1134451793825378304
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(aliases=["Roll"])
    async def roll(self, ctx):
        pingDays = [2, 4, 5]
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Auto role
        roll = 0
        while True:
            randId = randint(0, len(varStore.members)-1)
            roll += 1
            if varStore.members[randId] not in varStore.pastSelectIds:
                break
        announceChannel = self.bot.get_channel(907599229629911104)

        varStore.pastSelectIds.pop(0)
        varStore.pastSelectIds.append(str(varStore.members[randId]))
        try:
            f = open(
                "storage/pastSelectId.txt", "w")
        except:
            f = open("storage/pastSelectId.txt", "w")

        for id in varStore.pastSelectIds:
            f.write(id + "\n")
        f.close()

        selectMemberId = varStore.members[randId]
        user = await self.bot.fetch_user(selectMemberId)
        await announceChannel.send(f"<@{selectMemberId}> has been chosen to do the announcement! If you want a template, run '/template'.")

        activity = discord.Activity(
            type=discord.ActivityType.watching, name=f"{user.name}'s announcement")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)

        print(f"Announcement rolled at {current_time}")

        # Stops the auto rotation of status for 10 minutes
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

        now = datetime.now()
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

    @commands.cooldown(1, 3, commands.BucketType.user)
    @app_commands.guild_only()
    @app_commands.command(name="template", description='Announcement template')
    async def template(self, interaction: discord.Interaction, message: str = None, emoji: str = None):
        iffGuild = self.bot.get_guild(592559858482544641)
        eightGuild = self.bot.get_guild(907599229629911101)
        sevenRole = iffGuild.get_role(783564469854142464)
        eightRole = iffGuild.get_role(845007589674188839)
        nineRole = iffGuild.get_role(863756344494260224)
        company_icon = ""

        # Gets the current day and the event time
        now = datetime.now()
        day = (now.strftime("%A")).upper()

        # If the day is friday, then the event is 1 hour later
        # if datetime.today().weekday() == 4:
        # # All other days of the week other than sunday
        #     event_type = "OCEANIC"
        #     event_datetime = datetime(now.year, now.month, now.day, hour = 21, minute = 0, second = 0)
        #     training_msg = "We have training **1 hour** before the event so make sure you come!"
        if datetime.today().weekday() not in [6]:
            event_type = "OCEANIC"
            event_datetime = datetime(now.year, now.month, now.day, hour = 20, minute = 0, second = 0)
            training_msg = "We have training **1 hour** before the event so make sure you come!"
        # Sunday is SEA
        else:
            event_type = "ASIA"
            event_datetime = datetime(now.year, now.month, now.day, hour = 22, minute = 0, second = 0)
            training_msg = ""

        event_epoch = int(event_datetime.timestamp())

        if message is None:
            message = "[Inspirational message]"

        if emoji is None:
            emoji = "[Emoji]"

        if sevenRole in interaction.user.roles:
            company_icon = ":7e:"
        elif eightRole in interaction.user.roles:
            company_icon = ":8e:"
        elif nineRole in interaction.user.roles:
            company_icon = ":9e:"
        elif interaction.guild == eightGuild:
            company_icon = ":8e:"

        await interaction.response.send_message(
            "Check you dm's!"
        )

        await interaction.user.send(
                f"""
# {company_icon} :IFF1:   ═════ {day} {event_type} LINEBATTLE EVENT ═════   :IFF1: {company_icon}
## When: <t:{event_epoch}:t> or <t:{event_epoch}:R>

{message}

{training_msg}

React {emoji} if you'll be attending

I hope to see all of you coming!
[Ping]
    """
            )

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(aliases=["Ranks", "rank", "Rank"])
    async def ranks(self, ctx):
        await ctx.reply("You can find the ranks at")

    # 8e company welcome
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.command(
        aliases=[
            "comWelcome",
            "comwel",
            "ComWel",
            "Comwel",
            "companywelcome",
            "Companywelcome",
        ],
    )
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    async def comWel(self, ctx, rct: discord.User):
        iffGuild = self.bot.get_guild(592559858482544641)
        sevenRole = iffGuild.get_role(783564469854142464)
        eightRole = iffGuild.get_role(845007589674188839)
        nineRole = iffGuild.get_role(863756344494260224)

        if sevenRole in ctx.author.roles:
            company = "7e"
            leadership = "Cpt. Tobakshi, SMaj. Muddy Shoes and Sgt. Kerrahn"
        elif eightRole in ctx.author.roles:
            company = "8e"
            leadership = "Col. Joshlols, Cpt. Bronze, Lt. Ace, SMaj. SoulWarden, SMaj. Rabbi and Sgt. Quack"
        elif nineRole in ctx.author.roles:
            company = "9e"
            leadership = "AdC. Ballistic, Cpt. Ghost and SMaj. Redundant"
        else:
            await ctx.reply("Invalid roles")
            return

        try:
            img = discord.File(
                "iffBot/files/8e.png",
                filename="8e.png",
            )
        except:
            img = discord.File(
                "/home/pi/Desktop/iffBot/files/8e.png", filename="8e.png"
            )

        # channel = self.bot.get_channel(varStore.companyChannel)
        channel = self.bot.get_channel(806427204896292864)

        embed = discord.Embed(
            title=f"Welcome to the {company} Infantry Company {rct.name}!",
            url="",
            description=f"The {company} is one of the IFF's 3 infantry companies",
            color=0x109319,
        )
        embed.set_thumbnail(url="attachment://8e.png")
        embed.add_field(
            name="Our Leadership",
            value=f"Our leadership is made up of {leadership}",
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value=f"Feel free to ask any of them any questions or concerns you have about the IFF, the {company} company or holdfast in general ",
            inline=False,
        )
        embed.add_field(name="\u200b", value="Enjoy your stay here!", inline=True)
        embed.set_author(name=rct.display_name, icon_url=rct.avatar_url)
        await channel.send(file=img, embed=embed)


    # Wargames rotation
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    async def wgsplit(self,ctx,target_channel: int):
        if ctx.author.voice.channel.category_id == self.event_vc_category_id:
            i = True
            channel = self.bot.get_channel(target_channel)
            for user in ctx.author.voice.channel.members:
                if i:
                    await user.move_to(channel)
                    i = False
                else:
                    i = True


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
                "iffBot/files/8e.png",
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
    @commands.command(name = "rollcall", aliases=["Rollcall"])
    async def rollcall(self, ctx:commands.Context):
        vcCatIds = [948180967607136306, 995586698006233219]
        iffGuild = self.bot.get_guild(592559858482544641)
        vcChannelsIds = []
        totalUsers = 0
        channelUsers = []
        sevenUsers = []
        eightUsers = []
        nineUsers = []
        otherUsers = []

        sevenRole = ctx.guild.get_role(783564469854142464)
        eightRole = ctx.guild.get_role(845007589674188839)
        nineRole = ctx.guild.get_role(863756344494260224)

        vcChannelsIds = [channel.id for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]

        for channelId in vcChannelsIds:
            channel = self.bot.get_channel(channelId)
            channelUsers.append(channel.members)
            totalUsers += len(channel.members)

        for user in channelUsers:
            for x in user:
                if sevenRole in x.roles:
                    sevenUsers.append(x.display_name)
                    continue
                elif eightRole in x.roles:
                    eightUsers.append(x.display_name)
                    continue
                elif nineRole in x.roles:
                    nineUsers.append(x.display_name)
                    continue
                else:
                    otherUsers.append(x.display_name)
                    continue

        sevenStr = ", ".join(sevenUsers)
        eightStr = ", ".join(eightUsers)
        nineStr = ", ".join(nineUsers)
        otherStr = ", ".join(otherUsers)

        ncoChannel = self.bot.get_channel(954194296809095188)

        embed=discord.Embed(title="IFF Attendance", description="Current IFF attendance", color=0x151798)
        embed.add_field(name=f"Total Players", value=f"{totalUsers}", inline=False)
        embed.add_field(name=f"7th Players (Total: {len(sevenUsers)})", value=f"\u200b{sevenStr}", inline=False)
        embed.add_field(name=f"8th Players (Total: {len(eightUsers)})", value=f"\u200b{eightStr}", inline=False)
        embed.add_field(name=f"9th Players (Total: {len(nineUsers)})", value=f"\u200b{nineStr}", inline=False)
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
        async with ctx.channel.typing():
            msg = await ctx.reply("Splitting line now...")
            voiceChannelUsers = ctx.author.voice.channel.members

            sevenVcs = [872101027682324540, 872056405052510238]
            eightVcs = [869519564973703228, 872101199028043866]
            nineVcs = [1211849719601438821, 864013586774491187, 1210897956824162364]

            sevenRole = ctx.guild.get_role(783564469854142464)
            eightRole = ctx.guild.get_role(845007589674188839)
            nineRole = ctx.guild.get_role(863756344494260224)

            #7e
            if sevenRole in ctx.author.roles:
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
            if eightRole in ctx.author.roles:
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
            if nineRole in ctx.author.roles:
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

        await msg.edit(content="Done!")

    #Merge command
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["Merge"])
    async def merge(self, ctx):
        async with ctx.channel.typing():
            msg = await ctx.reply("Merging lines now...")
            sevenRole = ctx.guild.get_role(783564469854142464)
            eightRole = ctx.guild.get_role(845007589674188839)
            nineRole = ctx.guild.get_role(863756344494260224)

            #7e
            if sevenRole in ctx.author.roles:
                firstVc = self.bot.get_channel(872101027682324540)
                secondVc = self.bot.get_channel(872056405052510238)
                for user in secondVc.members:
                    await user.move_to(firstVc)

            #8e
            if eightRole in ctx.author.roles:
                firstVc = self.bot.get_channel(869519564973703228)
                secondVc = self.bot.get_channel(840889769713205248)
                for user in secondVc.members:
                    await user.move_to(firstVc)

            #9e
            if nineRole in ctx.author.roles:
                firstVc = self.bot.get_channel(872101199028043866)
                secondVc = self.bot.get_channel(864013586774491187)
                for user in secondVc.members:
                    await user.move_to(firstVc)

        await msg.edit(content="Done!")


    #Move all users in current vc to parade ground
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["Parade"])
    async def parade(self, ctx):
        async with ctx.channel.typing():
            msg = await ctx.reply("Moving users now...")
            paradeGround = self.bot.get_channel(757782109275553863)
            connectedUsers = ctx.author.voice.channel.members

            for user in connectedUsers:
                await user.move_to(paradeGround)

        await msg.edit(content="Done!")

    #Move everyone to parade ground
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["Forceparade","unfuck","return"])
    async def forceparade(self, ctx):
        async with ctx.channel.typing():
            msg = await ctx.reply("Moving users now...")
            vcCatId = 948180967607136306
            paradeGround = self.bot.get_channel(757782109275553863)

            for channel in ctx.guild.voice_channels:
                if channel.category_id == vcCatId and channel.category_id != 757782109275553863 and channel.category_id != 853615447261446144:
                    for user in channel.members:
                        await user.move_to(paradeGround)

        await msg.edit(content="Done!")

    #Spread command
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Spread","fuckoff"])
    async def spread(self, ctx):
        async with ctx.channel.typing():
            msg = await ctx.reply("Spreading users now...")

            vcCatId = 948180967607136306
            sevenChannel = self.bot.get_channel(872101027682324540)
            eightChannel = self.bot.get_channel(869519564973703228)
            nineChannel = self.bot.get_channel(1211849719601438821)
            fourChannel = self.bot.get_channel(660358590925897769)

            sevenRole = ctx.guild.get_role(783564469854142464)
            eightRole = ctx.guild.get_role(845007589674188839)
            nineRole = ctx.guild.get_role(863756344494260224)
            fourRole = ctx.guild.get_role(760440084880162838)

            if ctx.author.voice.channel.category_id == vcCatId:
                for user in ctx.author.voice.channel.members:
                    if sevenRole in user.roles:
                        await user.move_to(sevenChannel)
                    elif eightRole in user.roles:
                        await user.move_to(eightChannel)
                    elif nineRole in user.roles:
                        await user.move_to(nineChannel)
                    elif fourRole in user.roles:
                        await user.move_to(fourChannel)

            await msg.edit(content="Spreading complete. Please move the mercs/recruits to the appropriate channel")

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
            if iffRole in user.roles and retiredRole not in user.roles and retiredLeadership not in user.roles and "Rct." not in user.display_name and "Cdt." not in user.display_name and "Sdt." not in user.display_name:
                duration = int((datetime.now() - user.joined_at.replace(tzinfo=None)).days)
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

        # embed=discord.Embed(title="Service Medals", description="All the users who need to be awarded service medals", color=0xff0000)
        # embed.add_field(name="Bronze Military Merit", value=", ".join(bronzeMerit) + "\u200b", inline=False)
        # embed.add_field(name="Silver Military Merit", value=", ".join(silverMerit) + "\u200b", inline=False)
        # embed.add_field(name="Gold Military Merit", value=", ".join(goldMerit) + "\u200b", inline=False)
        # embed.add_field(name="Platinum Military Merit", value=", ".join(platMerit) + "\u200b", inline=False)
        # await ctx.send(embed=embed)
        await ctx.send("**Service Medals**")
        await ctx.send("**Bronze Service:** " + ", ".join(bronzeMerit) + "\u200b")
        await ctx.send("**Silver Service:** " + ", ".join(goldMerit) + "\u200b")
        await ctx.send("**Gold Service:** " + ", ".join(goldMerit) + "\u200b")
        await ctx.send("**Platinium Service:** " + ", ".join(platMerit) + "\u200b")

    #Anniversaries
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.guild_only()
    @commands.command(aliases=["anni"])
    async def anniversaries(self, ctx):
        iffRole = get(ctx.guild.roles, id = 611927973838323724)
        retiredRole = get(ctx.guild.roles, id= 707125172699660288)
        retiredLeadership = get(ctx.guild.roles, id= 887542975821905970)
        players = []
        msg = ""

        for user in ctx.guild.members:
            if iffRole in user.roles and retiredRole not in user.roles and retiredLeadership not in user.roles and "Rct." not in user.display_name and "Cdt." not in user.display_name and "Sdt." not in user.display_name:
                duration = int((datetime.now() - user.joined_at.replace(tzinfo=None)).days)
                if duration >= 730:
                    players.append([user.display_name, round(duration/365, 2)])

        players = sorted(players, key=lambda x: x[1], reverse=True)

        for player in players:
            msg += f"{player[0]}: {player[1]}\n"

        await ctx.send("**Anniversaries**")
        await ctx.send(msg)

    # Returns the roles a member had if they return to the server
    @app_commands.checks.has_any_role(
        990267891330977813, #Reg HQ
        661521548061966357, #Company Cmd
        660353960514813952, #CO
        661522627646586893, #NCO
        948862889815597079, #Bot dev
        855301506252406795, # Person in "Random shit" server
        )
    @app_commands.guild_only()
    @app_commands.command(name="return_role", description='Returns the roles to a returned user')
    async def return_role(self, interaction: discord.Interaction, member: discord.Member):
        storageFolder = Path().absolute() / "storage"
        leftMembersFile = storageFolder / "leftMembers.txt"
        await interaction.response.defer()

        # Writes the user ID with the following line containing the role id's
        with open(leftMembersFile, "r") as file:
            file = file.readlines()
            for i,line in enumerate(file):
                line = line.strip()

                if line == str(member.id):
                    # 592559858482544641
                    iffGuild = self.bot.get_guild(854332552117485569)
                    roleids = file[i+1].strip().split(",")
                    failedRoles = []
                    index_to_remove = [i, i+1]

                    for roleid in roleids:
                        role = get(iffGuild.roles, id = int(roleid))
                        if role.name != "@everyone":
                            try:
                                await member.add_roles(role, reason = "Restoring roles")
                            except Exception as E:
                                if role not in member.roles:
                                    failedRoles.append(role.name)

                    await interaction.followup.send(f"Roles restored. Please manually add the roles {failedRoles} and remove any unnecessary roles.")

        with open(leftMembersFile, "w") as newFile:
            for i,line in enumerate(file):
                if i not in index_to_remove:
                    newFile.write(line)

    @app_commands.checks.has_any_role(
        990267891330977813, #Reg HQ
        661521548061966357, #Company Cmd
        660353960514813952, #CO
        661522627646586893, #NCO
        948862889815597079, #Bot dev
        855301506252406795, # Person in "Random shit" server
        )
    @app_commands.guild_only()
    @app_commands.command(name="read_return", description='Reads the list of users who have left')
    async def read_return(self, interaction: discord.Interaction):
        storageFolder = Path().absolute() / "storage"
        leftMembersFile = storageFolder / "leftMembers.txt"

        users = []
        not_in_server = 0

        with open(leftMembersFile, "r") as file:
            lines = file.readlines()

            for i in range(0,len(lines), 2):
                user = self.bot.get_user(int(lines[i].strip()))

                if user is not None:
                    users.append(user.display_name)
                else:
                    not_in_server += 1

        await interaction.response.send_message(f"{users}" + f"\nThere were {not_in_server} other people who are currently not in the IFF server")

    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Rctform", "rctForm", "RctForm"])
    async def rctform(self, ctx):
        await ctx.send("""
**Copy/Paste and answer the following questions to access the server**
Please check <#853180535303176213>, <#910247350923059211> and <#853180574957043712> before you answer
```**What is your new Holdfast ingame name?** IFF | Name

**What region/timezone are you from? (e.g. Australia, South East Asia, NA, etc.)**
*(If from South East Asia, state your country)*

**How did you find out about the IFF?**

**Have you joined the in-game IFF regiment registry?**

**Do you agree with our rules and discord ToS?**

@Recruiter```""")

    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Rctrole", "rctRole", "RctRole"])
    async def rctrole(self, ctx, *, rct: discord.Member = None):
        rctRole = ctx.guild.get_role(845563588324098058)
        iffRole = ctx.guild.get_role(611927973838323724)
        nickRole = ctx.guild.get_role(893824145299746816)
        newcomerRole = ctx.guild.get_role(627801587351289856)

        if (ctx.channel.id == 592560417394393098 and ctx.message.reference is not None and rct is None):
            repliedMsgId = ctx.message.reference.message_id
            repliedMsg = await ctx.fetch_message(repliedMsgId)
            user = ctx.guild.get_member(repliedMsg.author.id)
            try:
                await user.remove_roles(newcomerRole, reason = "Bot removing newcomer role")
                await user.add_roles(rctRole, iffRole, nickRole, reason = "Bot adding recruit roles")
            except:
                await ctx.reply("Failed to add recruit roles")
            else:
                await ctx.reply(f"Recruit roles added for {user.display_name}")

        elif rct is not None:
            try:
                await rct.remove_roles(newcomerRole, reason = "Bot removing newcomer role")
                await rct.add_roles(rctRole, iffRole, nickRole, reason = "Bot adding recruit roles")
            except:
                await ctx.reply("Failed to add recruit roles (Check the spacing in the command)")
            else:
                await ctx.reply(f"Recruit roles added for {rct.display_name}")
        else:
            await ctx.reply("Please reply to a form or input an id/username")

    #Muster role
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(name = "muster", aliases=["Muster"])
    async def muster(self, ctx):
        start = datetime.now()
        musterChannelId = 832454366598135808
        sevenRole = ctx.guild.get_role(783564469854142464)
        eightRole = ctx.guild.get_role(845007589674188839)
        nineRole = ctx.guild.get_role(863756344494260224)
        coRole = ctx.guild.get_role(660353960514813952)
        ncoRole = ctx.guild.get_role(661522627646586893)
        cplRole = ctx.guild.get_role(863757684674920519)

        async with ctx.channel.typing():
            if ctx.channel.id == musterChannelId:
                async for message in ctx.channel.history(limit = 14):
                    if message is None:
                        break
                    elif message.author.bot:
                        await message.delete()

            workingMsg = await ctx.reply("Generating now")

            #Creates functions for calculating muster roll
            def coCalc(companyRole):
                coList = []
                for user in ctx.guild.members:
                    if companyRole in user.roles:
                        if coRole in user.roles:
                            if '"Cpt. ' in user.display_name:
                                nick = (user.display_name).replace('"Cpt. ', "Captain ").split("|",1)
                                cleanNick = nick[0]
                                coList.insert(0, cleanNick)
                            elif '"Lt.' in user.display_name:
                                nick = (user.display_name).replace('"Lt. ', "Lieutenant ").split("|",1)
                                cleanNick = nick[0]
                                coList.append(cleanNick)
                if coList == []: coList = ["Currently vacant"]
                coList.sort()
                return coList

            def ncoCalc(companyRole):
                ncoList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if ncoRole in user.roles:
                                if "'SMaj." in user.display_name:
                                    nick = (user.display_name).replace("'SMaj. ", "Sergeant Major ").split("|",1)
                                    cleanNick = nick[0]
                                    ncoList.insert(0, cleanNick)
                                elif "'Sgt." in user.display_name:
                                    nick = (user.display_name).replace("'Sgt. ", "Sergeant ").split("|",1)
                                    cleanNick = nick[0]
                                    ncoList.append(cleanNick)
                if ncoList == []: ncoList = ["Currently vacant"]
                return ncoList

            def cplCalc(companyRole):
                cplList = []
                for user in ctx.guild.members:
                        if companyRole in user.roles:
                            if cplRole in user.roles:
                                if ".Cpl." in user.display_name:
                                    nick = (user.display_name).replace(".Cpl. ", "Corporal ").split("|",1)
                                    cleanNick = nick[0]
                                    cplList.append(cleanNick)
                                elif ".LCpl." in user.display_name:
                                    nick = (user.display_name).replace(".LCpl. ", "Lance Corporal ").split("|",1)
                                    cleanNick = nick[0]
                                    cplList.append(cleanNick)
                if cplList == []: cplList = ["Currently vacant"]
                cplList.sort()
                return cplList

            def enlistedCalc(companyRole):
                kgsmList = []
                grenList = []
                regList = []
                pfcList = []

                sgdList = []
                gdmList = []

                for user in ctx.guild.members:
                    if companyRole in user.roles and "[" not in user.display_name:
                        if "Kgsm. " in user.display_name:
                            nick = (user.display_name).replace("Kgsm. ", "Kingsman ").split("|",1)
                            cleanNick = nick[0]
                            kgsmList.append(cleanNick)
                        elif "Gren. " in user.display_name:
                            nick = (user.display_name).replace("Gren. ", "Grenadier ").split("|",1)
                            cleanNick = nick[0]
                            grenList.append(cleanNick)
                        elif "Reg. " in user.display_name:
                            nick = (user.display_name).replace("Reg. ", "Regular ").split("|",1)
                            cleanNick = nick[0]
                            regList.append(cleanNick)
                        elif "PFC. " in user.display_name:
                            nick = (user.display_name).replace("PFC. ", "Private First Class ").split("|",1)
                            cleanNick = nick[0]
                            pfcList.append(cleanNick)
                        elif "Sgd. " in user.display_name:
                            nick = (user.display_name).replace("Sgd. ", "Senior Guardsman ").split("|",1)
                            cleanNick = nick[0]
                            sgdList.append(cleanNick)
                        elif "Gdm. " in user.display_name:
                            nick = (user.display_name).replace("Gdm. ", "Guardsman ").split("|",1)
                            cleanNick = nick[0]
                            gdmList.append(cleanNick)

                kgsmList.sort()
                grenList.sort()
                regList.sort()
                pfcList.sort()

                sgdList.sort()
                gdmList.sort()

                enlistedList = [sgdList, gdmList, kgsmList, grenList, regList, pfcList]
                flatEnlistedList = [name for list in enlistedList for name in list]

                return flatEnlistedList

            def enlistedCountCalc(companyRole):
                enlistedCount = 0
                for user in ctx.guild.members:
                    if companyRole in user.roles and "[" not in user.display_name:
                        if "Rct." in user.display_name:
                            enlistedCount += 1
                        elif "Cdt." in user.display_name:
                            enlistedCount += 1
                        elif "Pte." in user.display_name:
                            enlistedCount += 1
                return enlistedCount

            #Stuff for creating muster roll
            companies = ["seven", "eight", "nine"]
            rankGroups = ["Co", "Nco", "Cpl", "Enlisted"]
            muster = {}

            #Creates muster roll information
            for company in companies:
                if company == "seven": role = sevenRole
                elif company == "eight": role = eightRole
                elif company == "nine": role = nineRole

                for rank in rankGroups:
                    if rank == "Co": func = coCalc
                    elif rank == "Nco": func = ncoCalc
                    elif rank == "Cpl": func = cplCalc
                    elif rank == "Enlisted": func = enlistedCalc

                    muster[f"{company}{rank}"] = func(role)
                    muster[f"{company}{rank}"] = "\n".join(muster[f"{company}{rank}"])

            # fourEnlistedCount = enlistedCountCalc(fourRole)
            sevenEnlistedCount = enlistedCountCalc(sevenRole)
            eightEnlistedCount = enlistedCountCalc(eightRole)
            nineEnlistedCount = enlistedCountCalc(nineRole)

            imageFolder = Path().absolute() / "files"

            # Command skin 1 pic
            cmdImgDir = imageFolder / "cmd_skin.png"
            cmdImg = discord.File(cmdImgDir)

            cmdImg2Dir = imageFolder / "cmd_skin2.png"
            cmdImg2 = discord.File(cmdImg2Dir)

            sevenImgDir = imageFolder / "7e_skin.png"
            sevenImg = discord.File(sevenImgDir)

            eightImgDir = imageFolder / "8e_skin.png"
            eightImg = discord.File(eightImgDir)

            nineImgDir = imageFolder / "9e_skin.png"
            nineImg = discord.File(nineImgDir)

            adminImgDir = imageFolder / "admin_skin.png"
            adminImg = discord.File(adminImgDir)

            cavImgDir = imageFolder / "cav_skin.png"
            cavImg = discord.File(cavImgDir)

            # Command Col----------------------------------------------------
            cmd1Embed=discord.Embed(title="Imperial Frontier Force - 1ic", description="", color=0xffff00)
            cmd1Embed.set_thumbnail(url="attachment://cmd_skin.png")
            cmd1Embed.add_field(name="Colonel Joshlols", value='"Shutup when he\'s talking"', inline=False)

            # Command 2ic----------------------------------------------------
            # cmd2Embed=discord.Embed(title="Imperial Frontier Force - 2ic", description="", color=0xffff00)
            # cmd2Embed.set_thumbnail(url="attachment://cmd_skin2.png")
            # cmd2Embed.add_field(name="Lieutenant Colonel Ballistic", value='"But I\'m not a rapper"', inline=False)

            # Maj 7e ----------------------------------------------------
            maj7eEmbed=discord.Embed(title="Imperial Frontier Force - Head of 7th Company", description="", color=0xffff00)
            maj7eEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/224567016671936512/a1652bca7807f02b9d3fbbfc648de545.webp?size=1024")
            maj7eEmbed.add_field(name="Major Tobakshi", value="Major for 7th Brunswick Field Corps", inline=False)

            # Maj 8e ----------------------------------------------------
            maj8eEmbed=discord.Embed(title="Imperial Frontier Force - Head of 8th Company", description="", color=0xffff00)
            maj8eEmbed.set_thumbnail(url="https://cdn.discordapp.com/avatars/499816773122654219/2b64003095a012e870fc5638360cdb1c.webp?size=1024")
            maj8eEmbed.add_field(name="Major SoulWarden", value="Major for 8th Connaught Rangers", inline=False)

            #Maj 9e ----------------------------------------------------
            maj9eEmbed=discord.Embed(title="Imperial Frontier Force - Head of 9th Company", description="", color=0xffff00)
            maj9eEmbed.set_thumbnail(url="https://cdn.discordapp.com/guilds/592559858482544641/users/398731536813522954/avatars/8b8e1623669d4112ccbb75bde85783a9.webp?size=1024")
            maj9eEmbed.add_field(name="Major Kiwi", value="Major for 9th Gordon Highlanders", inline=False)

            # 7e ---------------------------------------------------------------------
            sevenEmbed = discord.Embed(
                title="7th Brunswick Field Corps - 'Black Legion'",
                description="Muster roll for 7th company",
                color=0xb12222,
            )
            sevenEmbed.set_thumbnail(url="attachment://7e_skin.png")
            sevenEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{muster['sevenCo']}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Non-Commissioned Officers",
                value=f"\u200b{muster['sevenNco']}",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Corporals", value=f"\u200b{muster['sevenCpl']}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{muster['sevenEnlisted']}", inline=False
            )
            sevenEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            sevenEmbed.add_field(
                name=f"Recruit → Private",
                value=f"\u200b{sevenEnlistedCount}",
                inline=False,
            )

            # 8e ---------------------------------------------------------------------
            eightEmbed = discord.Embed(
                title="8th Connaught Rangers - 'Devil's Own'",
                description="Muster roll for 8th company",
                color=0x1f8b4c,
            )
            eightEmbed.set_thumbnail(url="attachment://8e_skin.png")
            eightEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{muster['eightCo']}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Non-Commissioned Officers",
                value=f"\u200b{muster['eightNco']}",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Corporals", value=f"\u200b{muster['eightCpl']}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{muster['eightEnlisted']}", inline=False
            )
            eightEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            eightEmbed.add_field(
                name=f"Recruit → Private",
                value=f"\u200b{eightEnlistedCount}",
                inline=False,
            )

            # 9e ---------------------------------------------------------------------
            nineEmbed = discord.Embed(
                title="9th Gordon Highlanders - 'Skirted Devils'",
                description="Muster roll for 9th company",
                color=0x206694,
            )
            nineEmbed.set_thumbnail(url="attachment://9e_skin.png")
            nineEmbed.add_field(
                name=f"Commissioned Officers", value=f"\u200b{muster['nineCo']}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Non-Commissioned Officers", value=f"\u200b{muster['nineNco']}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Corporals", value=f"\u200b{muster['nineCpl']}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Enlisted", value=f"\u200b{muster['nineEnlisted']}", inline=False
            )
            nineEmbed.add_field(
                name=f"\u200b",
                value=f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
                inline=False,
            )
            nineEmbed.add_field(
                name=f"Recruit → Private",
                value=f"\u200b{nineEnlistedCount}",
                inline=False,
            )

            #Could automate admins in future
            #Admins ------------------------------------------------------
            adminEmbed=discord.Embed(title="Administration", description="", color=0xe74c25)
            adminEmbed.set_thumbnail(url="attachment://admin_skin.png")
            adminEmbed.add_field(name="Commissioned Officer", value="Quartermaster Peenoire", inline=False)
            adminEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            adminEmbed.add_field(name="Non-Commissioned Officer", value="Adjutant Ping\nAdjutant Minz", inline=False)

            #Specials ------------------------------------------------------
            specEmbed=discord.Embed(title="Non-Infantry Specialisation Leadership", description="Leadership for the specials.", color=0xf8e61c)
            specEmbed.set_thumbnail(url="attachment://cav_skin.png")
            specEmbed.add_field(name="Royal Somerset Rangers", value="Colonel Joshlols\nMajor Kiwi\nSergeant Major Bjorn", inline=False)
            specEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            specEmbed.add_field(name="King's Royal Hussars", value="Captain Bronze\nCorporal Sheppo", inline=False)
            specEmbed.add_field(name="\u200b", value="=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", inline=False)
            specEmbed.add_field(name="Royal Field Artillery Brigade", value="Lieutenant Deedee\nGrenadier Romans", inline=False)

            #Info embed
            end = datetime.now()

            infoEmbed=discord.Embed(title="Muster Roll Information", description="This muster roll is automatically generated, therefore there are a few matters that need to be explained", color=0xd0142a)
            infoEmbed.add_field(name="Naming", value="If you do not appear on the muster roll, firstly make sure you rank is spelt correctly with the correct prefix and suffix. For most enlisted, this will be a '.' at the end of your rank. Eg Cdt. [Name]. For leadership, make sure you have the correct prefix and correct capitalisation.", inline=False)
            infoEmbed.add_field(name="Roles", value="If you do not have the correct company role, you will not appear on the muster roll where you belong", inline=True)
            infoEmbed.add_field(name="Ranks", value="If you're within the ranks of Rct to Pte, you will not be displayed on the muster roll to save space", inline=True)
            infoEmbed.add_field(name="LOA and Retired", value="If you are on LOA or are retired, you will not be displayed on the muster roll (unless you're a member of leadership)", inline=True)
            infoEmbed.add_field(name="Other issues", value="Please dm SoulWarden or the bot directly if there are any problems", inline=True)
            infoEmbed.set_footer(text = f"Generation time: {end-start}")
            await workingMsg.delete()

            await ctx.send(file=cmdImg,embed=cmd1Embed)
            # await ctx.send(file=cmd2Img, embed=cmd2Embed)
            await ctx.send(embed=maj7eEmbed)
            await ctx.send(embed=maj8eEmbed)
            await ctx.send(embed=maj9eEmbed)
            await ctx.send(file=sevenImg, embed=sevenEmbed)
            await ctx.send(file=eightImg, embed=eightEmbed)
            await ctx.send(file=nineImg, embed=nineEmbed)
            await ctx.send(file=adminImg, embed=adminEmbed)
            await ctx.send(file=cavImg, embed=specEmbed)
            await ctx.send(embed = infoEmbed)

async def setup(bot):
    await bot.add_cog(iffCog(bot))
