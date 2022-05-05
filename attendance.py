import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re

scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('IFF Bot/storage/iffAttendanceCreds.json', scope)
except:
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Desktop/iffBot/storage/iffAttendanceCreds.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open("IFF Attendance")

class attendanceCog(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.has_any_role(
        661521548061966357, 660353960514813952, 661522627646586893, 948862889815597079
    )
    @commands.group(pass_context=True, aliases=["Attend"], invoke_without_subcommand=True)
    async def attend(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply("No command specified")
            return

    @attend.command(name = "individual", aliases=["indv"])
    async def individual(self, ctx, company: str, *, name: str):
        if company == "7e":
            sheet = spreadsheet.worksheet("7e Attendance")
        elif company == "8e":
            sheet = spreadsheet.worksheet("8e Attendance")
        elif company == "9e":
            sheet = spreadsheet.worksheet("9e Attendance")
        elif company == "4e":
            sheet = spreadsheet.worksheet("4e Attendance")
        else:
            await ctx.reply("Invalid company")

        try:
            search = re.compile(f'{name}')
            cell = sheet.find(search)
            attendance = sheet.cell(cell.row, (cell.col + 2)).value
            await ctx.reply(f"{cell.value} has {attendance} attendances")
        except:
            await ctx.reply("User not found")
      
    @attend.command(name = "leaderboard", aliases=["lead","leader"])
    async def leaderboard(self, ctx, minAttend = 100):
        if minAttend < 50:
            await ctx.reply("This will show too many users, please choose a higher cap")
            return
        
        msg = await ctx.reply("Working...")  
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        fourSheet = spreadsheet.worksheet("4e Attendance")
        
        def calc(sheet):
            nameColumn = sheet.col_values(4)
            attendanceColumn = sheet.col_values(6)
            
            zip_iterator = zip(nameColumn, attendanceColumn)
            users = dict(zip_iterator)
            users.pop("Name")
            return users
            
        sevenUsers = calc(sevenSheet)
        eightUsers = calc(eightSheet)
        nineUsers = calc(nineSheet)
        fourUsers = calc(fourSheet)
        
        users = {}
        users.update(sevenUsers)
        users.update(eightUsers)
        users.update(nineUsers)
        users.update(fourUsers)
        
        cleanedUsers = {}
        
        for user in users.items():
            if user[0] != "" and user[1] != "":
                try:
                    attendances = int(user[1])
                except:
                    pass     
                else:
                    if attendances > minAttend:
                            cleanedUsers[user[0]] = attendances
                            
        sortedList = {k: v for k, v in sorted(cleanedUsers.items(), reverse = True, key=lambda item: item[1])}
        userStr = ""
        count = 1
        for item in sortedList.items():
            userStr = userStr + f"{count}. {item[0]}: {item[1]}\n"
            count += 1
            
        embed=discord.Embed(title="Attendance Leaderboard", description=f"Lists all players with over {minAttend} attendances", color=0xc392ff)
        embed.add_field(name="Players: ", value=f"{userStr}", inline=True)
        
        await msg.delete()
        await ctx.send(embed=embed)
                
                
    @attend.command(name = "fill", aliases=["Fill"])
    async def fill(self, ctx):
        msg = await ctx.reply("Filling out attendance now...")
        start = datetime.now()
        vcCatId = 948180967607136306
        iffGuild = self.bot.get_guild(592559858482544641)
        sevenRole = ctx.guild.get_role(783564469854142464)
        eightRole = ctx.guild.get_role(845007589674188839)
        nineRole = ctx.guild.get_role(863756344494260224)
        fourRole = ctx.guild.get_role(760440084880162838)
        
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        fourSheet = spreadsheet.worksheet("4e Attendance")
        
        rawSevenUsers = [[user.id for user in channel.members if sevenRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id == vcCatId]
        rawEightUsers = [[user.id for user in channel.members if eightRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id == vcCatId]
        rawNineUsers = [[user.id for user in channel.members if nineRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id == vcCatId]
        rawFourUsers = [[user.id for user in channel.members if fourRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id == vcCatId]
        sevenUsers = [item for sublist in rawSevenUsers for item in sublist]
        eightUsers = [item for sublist in rawEightUsers for item in sublist]
        nineUsers = [item for sublist in rawNineUsers for item in sublist]
        fourUsers = [item for sublist in rawFourUsers for item in sublist]
        
        now = datetime.now()
        currentDate = now.strftime("%d/%m/%Y")
        
        def calc(date, sheet, users):
            countTickedUsers = 0
            countFailedUsers = 0
            dateColumn = sheet.find(date, in_row = 1)
            print("Date found")
            for id in users:
                try:
                    try:
                        cell = sheet.find(str(id), in_column = 3)
                    except:
                        cell = sheet.find(str(id), in_column = 2)
                    finally:
                        sheet.update_cell(cell.row, dateColumn.col, True)
                except:
                    countFailedUsers += 1
                    print(f"Failed id: {id}")
                else:
                    countTickedUsers += 1
            return countTickedUsers, countFailedUsers
        
        #7e
        seven = calc(currentDate, sevenSheet, sevenUsers)
        print("7e done")
        #8
        eight = calc(currentDate, eightSheet, eightUsers)
        print("8e done")
        #9
        nine = calc(currentDate, nineSheet, nineUsers)
        print("9e done")
        #4e
        four = calc(currentDate, fourSheet, fourUsers)
        print("4e done")

        end = datetime.now()
        
        embed=discord.Embed(title="Auto Attendance", description=f"Done! This took: {end-start}", color=0xff0000)
        embed.add_field(name="7e", value=f"Ticked Count = {seven[0]}, Failed Count = {seven[1]}", inline=True)
        embed.add_field(name="8e", value=f"Ticked Count = {eight[0]}, Failed Count = {eight[1]}", inline=True)
        embed.add_field(name="9e", value=f"Ticked Count = {nine[0]}, Failed Count = {nine[1]}", inline=True)
        embed.add_field(name="4e", value=f"Ticked Count = {four[0]}, Failed Count = {four[1]}", inline=True)
        
        await msg.delete()
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(attendanceCog(bot))
