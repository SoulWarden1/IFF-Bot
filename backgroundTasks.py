from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from random import randint
import asyncio
import varStore


class backgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Rotates the status
    @tasks.loop(seconds=30.0)
    async def statusRotation(self):
        statuses = ["_help", "your shotcalls", "your lack of skill", "your right clicking", "Joshlols", "your teamkills",
                    "your terrible aim", "you get straight stabbed", "Quack's line leading", "you get cannon wiped", "Deedee's stream", "Avyn", "8e"]
        choice = randint(0, len(statuses)-1)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{statuses[choice]}"))

    # Automatically rolls the announcement picker
    @tasks.loop(seconds=59.0)
    async def autoRoll(self):
        eventDays = [1, 2, 4, 5]
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        # Auto role
        if current_time == "14:30" and datetime.today().weekday() in eventDays and varStore.platform:
            roll = 0
            while True:
                randId = randint(0, len(varStore.members)-1)
                roll += 1
                if varStore.members[randId] != varStore.pastSelectId:
                    break
            logChannel = self.bot.get_channel(varStore.logChannel)
            announceChannel = self.bot.get_channel(varStore.companyChannel)
            await logChannel.send(f"Rolled {roll} times")

            try:
                f = open(
                    "C:/Users/Ryan/OneDrive - Haileybury/2022/Software Dev/VS Code Work/IFF Bot/storage/pastSelectId.txt", "w")
            except:
                f = open("/home/pi/Desktop/iffBot/storage/pastSelectId.txt", "w")

            f.write(str(varStore.members[randId]))
            f.close()
            varStore.pastSelectId = varStore.members[randId]

            selectMemberId = varStore.members[randId]
            user = await self.bot.fetch_user(selectMemberId)
            await announceChannel.send(f"<@{selectMemberId}> has been chosen to do the announcement! If you want a template, run '_template' (Although this isn't recommended)")

            activity = discord.Activity(
                type=discord.ActivityType.watching, name=f"{user.name}'s annoucement")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)

            print(f"Announcement rolled at {current_time}")

            # Stops the auto rotation of status for 10 minues
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.cancel()
            await asyncio.sleep(600)
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.start()

        # Auto leadership attendance ping
        elif current_time == "14:00" and datetime.today().weekday() in eventDays and varStore.platform:
            leadershipChannel = self.bot.get_channel(907599229629911104)

            embed = discord.Embed(title="Leadership Attendance", description="React with :thumbsup: or :thumbsdown: if you're coming tonight", color=0x109319)
            embed.add_field(name="Coming: ", value=f"No one :(", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)
            embed.add_field(name="Not coming: ",
                            value=f"No one :(", inline=False)
            embed.add_field(name="Count: ", value=f"0", inline=False)

            msg = await leadershipChannel.send(embed=embed)

            await msg.add_reaction("\N{THUMBS UP SIGN}")
            await msg.add_reaction("\N{THUMBS DOWN SIGN}")

            varStore.leaderPingMsgId = msg.id
            

    @tasks.loop(seconds=5)
    async def rgb(self):
        while True:
            await self.bot.change_presence(status=discord.Status.idle)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.dnd)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online)
            await asyncio.sleep(5)

    @commands.Cog.listener()
    async def on_ready(self):
        # Creates backgroup loops
        self.statusRotation.start()
        self.autoRoll.start()
        print("Background tasks started")


def setup(bot):
    bot.add_cog(backgroundTasks(bot))
