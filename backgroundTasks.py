from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from random import randint, choice
import asyncio
import varStore
import iffCmd

class backgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Rotates the status
    @tasks.loop(seconds=30.0)
    async def statusRotation(self):
        statuses = ["_help", 
                    "your shotcalls", 
                    "your lack of skill", 
                    "your right clicking", 
                    "Joshlols", 
                    "your teamkills",
                    "your terrible aim", 
                    "you getting straight stabbed", 
                    "Quack's line leading", 
                    "you getting cannon wipped", 
                    "Deedee's stream", 
                    "the IFF", 
                    "7e", 
                    "8e", 
                    "9e", 
                    "4e"]
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{choice(statuses)}"))

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
                if varStore.members[randId] not in varStore.pastSelectId:
                    break
            logChannel = self.bot.get_channel(varStore.logChannel)
            announceChannel = self.bot.get_channel(907599229629911104)
            await logChannel.send(f"Rolled {roll} times")

            varStore.pastSelectIds.pop(0)
            varStore.pastSelectIds.append(str(varStore.members[randId]))
            try:
                f = open(
                    "IFF Bot/storage/pastSelectId.txt", "w")
            except:
                f = open("/home/pi/Desktop/iffBot/storage/pastSelectId.txt", "w")

            f.write(varStore.pastSelectIds)
            f.close()

            selectMemberId = varStore.members[randId]
            user = await self.bot.fetch_user(selectMemberId)
            await announceChannel.send(f"<@{selectMemberId}> has been chosen to do the announcement! If you want a template, run '_template' (Although this isn't recommended)")

            activity = discord.Activity(
                type=discord.ActivityType.watching, name=f"{user.name}'s announcement")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)

            print(f"Announcement rolled at {current_time}")

            # Stops the auto rotation of status for 10 minues
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.cancel()
            await asyncio.sleep(600)
            cog = self.bot.get_cog("backgroundTasks")
            cog.statusRotation.start()

        # Auto leadership attendance ping
        elif current_time == "16:00" and datetime.today().weekday() in eventDays and varStore.platform:
            leadershipChannel = self.bot.get_channel(907599229629911104)

            embed = discord.Embed(title="Leadership Attendance", description="React with :thumbsup: or :thumbsdown: if you're coming tonight", color=0x109319)
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
            
        #Auto roll call
        elif current_time == "20:20" and datetime.today().weekday() in eventDays and varStore.platform:
            channel = self.bot.get_channel(954194296809095188)
            rollcall = self.bot.get_command("rollcall")
            await channel.invoke(rollcall)
            
        #Auto muster roll
        elif current_time == "22:00" and datetime.today().weekday() == 5 and varStore.platform:
            channel = self.bot.get_channel(832454366598135808)
            muster = self.bot.get_command("muster")
            await channel.invoke(muster)
            
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
