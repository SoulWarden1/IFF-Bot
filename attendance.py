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
        if minAttend <= 99:
            await ctx.reply("This will show too many users, please choose a higher cap")
            return
        
        start = datetime.now()
        msg = await ctx.reply("Working...")  
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        
        def calc(sheet):
            nameCol = sheet.find("Name")
            totalCol = sheet.find("Total")
            
            nameColumnVal = sheet.col_values(nameCol.col)
            attendanceColumnVal = sheet.col_values(totalCol.col)
            zip_iterator = zip(nameColumnVal, attendanceColumnVal)
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
        eventDays = [1, 2, 4, 5, 6]
        vcCatIds = [948180967607136306, 995586698006233219]
        iffGuild = self.bot.get_guild(592559858482544641)
        sevenRole = ctx.guild.get_role(783564469854142464)
        eightRole = ctx.guild.get_role(845007589674188839)
        nineRole = ctx.guild.get_role(863756344494260224)
        
        sevenSheet = spreadsheet.worksheet("7e Attendance")
        eightSheet = spreadsheet.worksheet("8e Attendance")
        nineSheet = spreadsheet.worksheet("9e Attendance")
        
        rawSevenUsers = [[user.id for user in channel.members if sevenRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        rawEightUsers = [[user.id for user in channel.members if eightRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        rawNineUsers = [[user.id for user in channel.members if nineRole in user.roles] for channel in iffGuild.voice_channels if channel.category_id in vcCatIds]
        sevenUsers = [item for sublist in rawSevenUsers for item in sublist]
        eightUsers = [item for sublist in rawEightUsers for item in sublist]
        nineUsers = [item for sublist in rawNineUsers for item in sublist]
        
        currentDate = start.strftime("%d/%m/%Y")
        
        
        # Checks if the current day of the week is an event day
        if datetime.today().weekday() not in eventDays:
            await msg.edit(content="Error: today is not an event day")
            return
            
        
        def calc(date, sheet, users):
            countTickedUsers = 0
            failedUser = []
            errorMsg = ""
            
            # Checks if there are no members of a company, if so exit
            if not users:
                print("No users")
                return
            
            #Attempting to find the correct column with the current date
            dateColumn = sheet.find(date, in_row = 1)
            if dateColumn is None:
                # Gets all the values from the row with the dates on it
                dateRow = sheet.row_values(1)
                # Checks from the end of the row and counts backwards to find the last empty cell
                for dateRowIndex in range(len(dateRow)-1, 0, -1):
                    if dateRow[dateRowIndex] != "" and dateRow[dateRowIndex] != "-":
                            # The 8th sheet has black col seperating weeks, so checking if that is the case
                        try:
                            if dateRow[dateRowIndex + 1] == "-":
                                # Updates sheet to have the current date at the correct cell. Repeated below
                                currentDateCol = dateRowIndex + 3
                                sheet.update_cell(1, currentDateCol, start.strftime("%d/%m/%Y"))
                                dateColumn = sheet.cell(1,currentDateCol)
                            # Other sheets don't have week seperators
                            else:
                                currentDateCol = dateRowIndex + 2
                                sheet.update_cell(1, currentDateCol, start.strftime("%d/%m/%Y"))
                                dateColumn = sheet.cell(1,currentDateCol)
                        except:
                            currentDateCol = dateRowIndex + 2
                            sheet.update_cell(1, currentDateCol, start.strftime("%d/%m/%Y"))
                            dateColumn = sheet.cell(1,currentDateCol)
                        break
            else:
                print("Date found")
            
            # Attempts to finds the column with the discord id's
            idColumnIndex = sheet.find("Discord Id's")
            # Checks if the column was found
            if idColumnIndex is None:
                errorMsg = "Discord Id column could not be found"
                return countTickedUsers, failedUser, errorMsg
            else:
                # Gets the all the discord id's in the column
                idColumnValues = sheet.col_values(idColumnIndex.col)
            
            ticked = []
            # Make this not a number
            # Sets the ticked list to have 200 falses
            # len(ticked) >= number of rows, otherwise an error will occur
            for _ in range(1,200):
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
                except Exception as e:
                    print(f"Failed (0) with: {e}")
                    print(id)
                    errorMsg = "An unknown error has occurred (0)"
                    return countTickedUsers, failedUser, errorMsg
            
            count = 1
            cells = []
            for value in ticked:
                try:
                    if value == True:
                        cells.append(Cell(row=count, col=dateColumn.col, value=True))
                    count += 1
                except Exception as e:
                    print(f"Failed (1) with: {e}")
                    errorMsg = "An unknown error has occurred (1)"
                    return countTickedUsers, failedUser, errorMsg
            
            # Ticks all users
            try:
                sheet.update_cells(cells)
            except Exception as e:
                    print(f"Failed (2) with: {e}")
                    errorMsg = "An unknown error has occurred (2)"
                    return countTickedUsers, failedUser, errorMsg
            
            return countTickedUsers, failedUser, errorMsg

        error = False
        embed=discord.Embed(title="Auto Attendance", description=f"Done! Please inform the relevant people if there are failed users", color=0xff0000)
        
        #7th
        try:
            seven = calc(currentDate, sevenSheet, sevenUsers)
        except:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 7th...")
            
        print("7th done")  
        if seven is None:
            msg = await msg.edit(content=msg.content + f"No 7th users...")
            embed.add_field(name="7th", value=f"No players in 7th", inline=True)
        elif isinstance(seven[0], int) and not seven[2]:
                msg = await msg.edit(content=msg.content + f"7th done ({seven[0]})...")
                embed.add_field(name="7th", value=f"No. Ticked= {seven[0]}, Failed Users: {seven[1]}", inline=True)
        elif seven[2]:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 7th...")
            embed.add_field(name="7th", value=seven[2], inline=True)
            error = True
            
        #8
        try:
            eight = calc(currentDate, eightSheet, eightUsers)
        except:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 8th...")
            
        print("8th done")
        if eight is None:
            msg = await msg.edit(content=msg.content + f"No 8th users...")
            embed.add_field(name="8th", value=f"No players in 8th", inline=True)
        elif isinstance(eight[0], int) and not eight[2]:
                msg = await msg.edit(content=msg.content + f"8th done ({eight[0]})...")
                embed.add_field(name="8th", value=f"No. Ticked= {eight[0]}, Failed Users: {eight[1]}", inline=True)
        elif eight[2]:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 8th...")
            embed.add_field(name="8th", value=eight[2], inline=True)
            error = True
        
        #9
        try:
            nine = calc(currentDate, nineSheet, nineUsers)
        except:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 9th...")
            
        print("9th done")
        if nine is None:
            msg = await msg.edit(content=msg.content + f"No 9th users...")
            embed.add_field(name="9th", value=f"No players in 9th", inline=True)
        elif isinstance(nine[0], int) and not nine[2]:
                msg = await msg.edit(content=msg.content + f"9th done ({nine[0]})...")
                embed.add_field(name="9th", value=f"No. Ticked= {nine[0]}, Failed Users: {nine[1]}", inline=True)
        elif nine[2]:
            msg = await msg.edit(content=msg.content + f"An error has occurred for 9th...")
            embed.add_field(name="9th", value=nine[2], inline=True)
            error = True
                
        end = datetime.now()
        #Check if there are failed users, if so alert user
        if error:
            embed.set_footer(text=f"Took {end-start}. WARNING THERE ARE FAILED USERS/COMPANIES.")
        else:
            embed.set_footer(text=f"Took {end-start}")
        
        # Updates the message with the results of the attendance
        await msg.edit(content=None, embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(attendanceCog(bot))
