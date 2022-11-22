import discord
from discord.ext import commands
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
from pathlib import Path

scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

iffAttendanceCreds = Path().absolute() / "storage" / "iffAttendanceCreds.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(iffAttendanceCreds, scope)
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
        if company == "7th":
            sheet = spreadsheet.worksheet("7e Attendance")
        elif company == "8th":
            sheet = spreadsheet.worksheet("8e Attendance")
        elif company == "9th":
            sheet = spreadsheet.worksheet("9e Attendance")
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
        if minAttend < 70:
            await ctx.reply("This will show too many users, please choose a higher cap")
            return
        
        start = datetime.now()
        msg = await ctx.reply("Working...")  
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        
        def calc(sheet):
            nameColumn = sheet.col_values(4)
            attendanceColumn = sheet.col_values(6)
            zip_iterator = zip(nameColumn, attendanceColumn)
            users = dict(zip_iterator)
            users.pop("Name")
            return users
        
        users = {}
        users.update(calc(sevenSheet))
        users.update(calc(eightSheet))
        users.update(calc(nineSheet))     
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
        
        end = datetime.now()
        embed=discord.Embed(title="Attendance Leaderboard", description=f"Lists all players with over {minAttend} attendances", color=0xc392ff)
        embed.add_field(name="Players: ", value=f"{userStr}", inline=True)
        embed.set_footer(text = f"Calculation time: {end-start}")
        
        await msg.delete()
        await ctx.send(embed=embed)
    
    @attend.command(name = "companyTotal", aliases=["comTot","comtotal","comtot","companytotal"])
    async def companyTotal(self, ctx, minAttend = 100):
        start = datetime.now()
        msg = await ctx.reply("Working...")  
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        
        def calc(sheet):
            totalAttendance = []
            totalAttendanceRaw = sheet.col_values(6)
            try: 
                index = totalAttendanceRaw.index("Date Joined")
            except:
                pass
            else:
                totalAttendanceRaw = totalAttendanceRaw[:index]

            for item in totalAttendanceRaw:
                try:
                    int(item)
                except:
                    continue
                else:
                    totalAttendance.append(int(item))
            print(totalAttendance)
            return sum(totalAttendance)
        
        sevenAttendTotal = calc(sevenSheet)
        eightAttendTotal = calc(eightSheet)
        nineAttendTotal = calc(nineSheet)
        
        end = datetime.now()
        embed=discord.Embed(title="Company Total Attendance", description=f"The individual attendances of each member of each company totaled", color=0xff0000)
        embed.add_field(name="7th", value=f"{sevenAttendTotal}", inline=True)
        embed.add_field(name="8th", value=f"{eightAttendTotal}", inline=True)
        embed.add_field(name="9th", value=f"{nineAttendTotal}", inline=True)
        embed.set_footer(text = f"Calculation time: {end-start}")
        
        await msg.delete()
        await ctx.send(embed=embed)
    
    # Auto fills out attendance
    @attend.command(name = "fill", aliases=["Fill"])
    async def fill(self, ctx):
        msg = await ctx.reply("Filling out attendance now...", mention_author = False)
        start = datetime.now()
        vcCatIds = [948180967607136306, 995586698006233219]
        iffGuild = self.bot.get_guild(592559858482544641)
        sevenRole = ctx.guild.get_role(783564469854142464)
        eightRole = ctx.guild.get_role(845007589674188839)
        nineRole = ctx.guild.get_role(863756344494260224)
        #fourRole = ctx.guild.get_role(760440084880162838)
        
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        #fourSheet = spreadsheet.worksheet("4e Attendance")
        
        rawSevenUsers = [[user.id for user in channel.members if sevenRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        rawEightUsers = [[user.id for user in channel.members if eightRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        rawNineUsers = [[user.id for user in channel.members if nineRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        #rawFourUsers = [[user.id for user in channel.members if fourRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        sevenUsers = [item for sublist in rawSevenUsers for item in sublist]
        eightUsers = [item for sublist in rawEightUsers for item in sublist]
        nineUsers = [item for sublist in rawNineUsers for item in sublist]
        #fourUsers = [item for sublist in rawFourUsers for item in sublist]
        
        currentDate = start.strftime("%d/%m/%Y")
        
        def calc(date, sheet, users):
            countTickedUsers = 0
            failedUser = []
            noDate = False
            
            # Checks if there are no members of a company, if so exit
            if not users:
                print("No users")
                return
            
            #Attempting to find the correct column with the right date
            dateColumn = sheet.find(date, in_row = 1)
            if dateColumn is None:
                print("Date NOT found")
                noDate = True
                return countTickedUsers, failedUser, noDate
            else:
                print("Date found")
            
            idColumnIndex = sheet.find("Discord Id's")
            idColumnValues = sheet.col_values(idColumnIndex.col)
            ticked = []
            
            # Make this not a number
            for i in range(1,150):
                ticked.append(False)
                
            count = 1
            for id in users:
                try:
                    if str(id) in idColumnValues:
                        ticked[idColumnValues.index(str(id))] = True
                        countTickedUsers += 1
                    else:
                        username = self.bot.get_user(id)
                        failedUser.append(username.name)
                        print(f"Failed id: {id}")
                    count += 1
                except:
                    print("Failed")
                    return countTickedUsers, failedUser, noDate
            
            count = 1
            cells = []
            for value in ticked:
                try:
                    if value == True:
                        cells.append(Cell(row=count, col=dateColumn.col, value=True))
                    count += 1
                except:
                    print("Failed")
                    return countTickedUsers, failedUser, noDate
            
            # Ticks all users
            try:
                sheet.update_cells(cells)
            except:
                    print("Failed")
                    return countTickedUsers, failedUser, noDate
            
            return countTickedUsers, failedUser, noDate

        error = False
        embed=discord.Embed(title="Auto Attendance", description=f"Done! Please inform the relevant people if there are failed users", color=0xff0000)
        #7th
        seven = calc(currentDate, sevenSheet, sevenUsers)
        print("7th done")  
        try:
            if isinstance(seven[0], int):
                msg = await msg.edit(content=msg.content + f" 7th done ({seven[0]})...")
                embed.add_field(name="7th", value=f"No. Ticked= {seven[0]}, Failed Users: {seven[1]}", inline=True)
            elif seven[2]:
                msg = await msg.edit(content=msg.content + f" No date for 7th...")
                embed.add_field(name="7th", value=f"No date was entered", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f"7th has failed...")
                embed.add_field(name="7th", value=f"No date was entered", inline=True)
        except:
            error = True
            if seven is None:
                msg = await msg.edit(content=msg.content + f" No 7th users...")
                embed.add_field(name="7th", value=f"No players in 7th", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f" 7th has failed...")
                embed.add_field(name="7th", value=f"**7th has failed**", inline=True)
            
        #8
        eight = calc(currentDate, eightSheet, eightUsers)
        print("8th done")
        try:
            if isinstance(eight[0], int) and not eight[2]:
                msg = await msg.edit(content=msg.content + f"8th done ({eight[0]})...")
                embed.add_field(name="8th", value=f"No. Ticked= {eight[0]}, Failed Users: {eight[1]}", inline=True)
            elif eight[2]:
                msg = await msg.edit(content=msg.content + f"No date for 8th...")
                embed.add_field(name="8th", value=f"No date was entered", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f"8th has failed...")
                embed.add_field(name="8th", value=f"No date was entered", inline=True)
        except:
            error = True
            if eight is None:
                msg = await msg.edit(content=msg.content + f"No 8th users...")
                embed.add_field(name="8th", value=f"No players in 8th", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f"8th has failed...")
                embed.add_field(name="8th", value=f"**8th has failed**", inline=True)
        
        #9
        nine = calc(currentDate, nineSheet, nineUsers)
        print("9th done")
        try:
            if isinstance(nine[0], int):
                msg = await msg.edit(content=msg.content + f" 9th done ({nine[0]})...")
                embed.add_field(name="9th", value=f"No. Ticked= {nine[0]}, Failed Users: {nine[1]}", inline=True)
            elif nine[2]:
                msg = await msg.edit(content=msg.content + f" No date for 9th...")
                embed.add_field(name="9th", value=f"No date was entered", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f"9th has failed...")
                embed.add_field(name="9th", value=f"No date was entered", inline=True)
        except:
            error = True
            if nine is None:
                msg = await msg.edit(content=msg.content + f" No 9th users...")
                embed.add_field(name="9th", value=f"No players in 9th", inline=True)
            else:
                msg = await msg.edit(content=msg.content + f" 9th has failed...")
                embed.add_field(name="9th", value=f"**9th has failed**", inline=True)
                
        end = datetime.now()
        #Check if there are failed users, if so alert user
        if error:
            embed.set_footer(text=f"Took {end-start}. WARNING THERE ARE FAILED USERS/COMPANIES, PLEASE CHECK YOUR ATTENDANCE SHEET")
        else:
            embed.set_footer(text=f"Took {end-start}")
        
        await msg.edit(content=None, embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(attendanceCog(bot))
