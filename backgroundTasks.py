from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from random import randint, choice
import asyncio
import varStore
import attendance
import platform

# from randomCmd import testMsg


class backgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Rotates the status
    @tasks.loop(seconds=60.0)
    async def statusRotation(self):
        statuses = [
            "_help",
            "your shotcalls",
            "your lack of skill",
            "your right clicking",
            "Joshlols",
            "your teamkills",
            "your terrible aim",
            "you getting straight stabbed",
            "you getting cannon wipped",
            "Deedee's stream",
            "the IFF",
            "7th",
            "8th",
            "9th",
        ]
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"{choice(statuses)}"
            )
        )

    # Automatically rolls the announcement picker
    @tasks.loop(seconds=59.0)
    async def autoRoll(self):
        eventDays = [2, 4, 5, 6]
        pingDays = [2, 4, 5]
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Auto roll
        if (
            current_time == "14:30"
            and datetime.today().weekday() in pingDays
            and platform.system() == "Linux"
        ):
            roll = 0
            while True:
                randId = randint(0, len(varStore.members) - 1)
                roll += 1
                if varStore.members[randId] not in varStore.pastSelectIds:
                    break
            announceChannel = self.bot.get_channel(907599229629911104)

            varStore.pastSelectIds.pop(0)
            varStore.pastSelectIds.append(str(varStore.members[randId]))
            
            f = open("storage/pastSelectId.txt", "w")

            for id in varStore.pastSelectIds:
                f.write(id + "\n")
            f.close()

            selectMemberId = varStore.members[randId]
            try:
                user = await self.bot.fetch_user(selectMemberId)
                user = user.name
            except:
                user = "Error"
            
            await announceChannel.send(
                f"<@{selectMemberId}> has been chosen to do the announcement! If you want a template, run '/template'."
            )

            activity = discord.Activity(
                type=discord.ActivityType.watching, name=f"{user}'s announcement"
            )
            await self.bot.change_presence(
                status=discord.Status.online, activity=activity
            )

            print(f"Announcement rolled at {current_time}")

            # Stops the auto rotation of status for 10 minues
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.cancel()
            await asyncio.sleep(600)
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.start()

        # Auto leadership attendance ping
        elif (
            current_time == "16:00"
            and datetime.today().weekday() in pingDays
            and platform.system() == "Linux"
        ):
            leadershipChannel = self.bot.get_channel(907599229629911104)

            embed = discord.Embed(
                title="Leadership Attendance",
                description="React with :thumbsup: or :thumbsdown: if you're coming tonight",
                color=0x109319,
            )
            embed.add_field(name="Coming: ", value=f"No one :(", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)
            embed.add_field(name="Not coming: ", value=f"No one :)", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)
            embed.add_field(name="Maybe coming: ", value=f"No one :(", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)

            msg = await leadershipChannel.send(embed=embed)

            await msg.add_reaction("\N{THUMBS UP SIGN}")
            await msg.add_reaction("\N{THUMBS DOWN SIGN}")
            await msg.add_reaction("\N{SHRUG}")

            varStore.leaderPingMsgId = msg.id

        # Auto roll call
        elif (
            current_time == "20:20"
            and datetime.today().weekday() in eventDays
            and platform.system() == "Linux"
        ):
            vcCatId = 948180967607136306
            iffGuild = self.bot.get_guild(592559858482544641)
            vcChannelsIds = []
            totalUsers = 0
            channelUsers = []
            sevenUsers = []
            eightUsers = []
            nineUsers = []
            otherUsers = []

            sevenRole = iffGuild.get_role(783564469854142464)
            eightRole = iffGuild.get_role(845007589674188839)
            nineRole = iffGuild.get_role(863756344494260224)

            vcChannelsIds = [
                channel.id
                for channel in iffGuild.voice_channels
                if channel.category_id == vcCatId
            ]

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

            embed = discord.Embed(
                title="IFF Attendance",
                description="Current IFF attendance",
                color=0x151798,
            )
            embed.add_field(name=f"Total Players", value=f"{totalUsers}", inline=False)
            embed.add_field(
                name=f"7th Players (Total: {len(sevenUsers)})",
                value=f"\u200b{sevenStr}",
                inline=False,
            )
            embed.add_field(
                name=f"8th Players (Total: {len(eightUsers)})",
                value=f"\u200b{eightStr}",
                inline=False,
            )
            embed.add_field(
                name=f"9th Players (Total: {len(nineUsers)})",
                value=f"\u200b{nineStr}",
                inline=False,
            )
            embed.add_field(
                name=f"Other Players (Total: {len(otherUsers)})",
                value=f"\u200b{otherStr}",
                inline=False,
            )
            await ncoChannel.send(embed=embed)

        # Auto muster roll
        # elif current_time == "22:00" and datetime.today().weekday() == 5 and varStore.platform:
        #     channel = self.bot.get_context(832454366598135808)
        #     muster = self.bot.get_command("muster")
        #     await channel.invoke(muster)

    @tasks.loop(seconds=5)
    async def rgb(self):
        while True:
            await self.bot.change_presence(status=discord.Status.idle)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.dnd)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online)
            await asyncio.sleep(5)

    # @tasks.loop(seconds=30)
    # async def test(self):
    #     await testMsg(self)

    @commands.Cog.listener()
    async def on_ready(self):
        # Creates backgroup loops
        self.statusRotation.start()
        self.autoRoll.start()
        # self.test.start()
        print("Background tasks started")


async def setup(bot):
    await bot.add_cog(backgroundTasks(bot))
