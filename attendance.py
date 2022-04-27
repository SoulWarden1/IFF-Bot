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
            dateColumn = sheet.find(date, in_row = 1)
            for id in users:
                try:
                    cell = sheet.find(str(id), in_column = 3)
                    sheet.update_cell(cell.row, dateColumn.col, True)
                except:
                    print(f"Failed id: {id}")
        
        #7e
        calc(currentDate, sevenSheet, sevenUsers)
        print("7e done")
        #8
        calc(currentDate, eightSheet, eightUsers)
        print("8e done")
        #9
        calc(currentDate, nineSheet, nineUsers)
        print("9e done")
        #4e
        calc(currentDate, fourSheet, fourUsers)
        print("4e done")

        end = datetime.now()
        await msg.edit(content=f"Done! This took: {end-start}")

def setup(bot:commands.Bot):
    bot.add_cog(attendanceCog(bot))
