import goblinSpy, re, discord, os, requests, bloodBowl
from discord.utils import get
import texts
class Commands:
    def __init__(self, ctx):
        self.ctx = ctx
        self.language = texts.EN
        self.goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)

    async def help(self):
        command = self.ctx.message.content.split()
        # Select witch help has to show
        if len(command) > 1:
            if command[1] == '1':
                await self.help_setup()
                return
            elif command[1] == '2':
                await self.help_commands()
                return
        # If not list has been selected, it will show the default help, listing the others
        await self.help_generic()

    async def help_generic(self):
        # List the help chapters
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title=self.language.HELP_GENERIC_TITLE,
            description=self.language.HELP_GENERIC_DESCRIPTION
        )
        embed.set_thumbnail(url=self.language.BOT_THUMBAIL)
        for field in self.language.HELP_GENERIC_FIELDS:
            embed.add_field(name= field[0], value=field[1], inline=False)

        await self.ctx.send(embed = embed)

    async def help_setup(self):
        # Shows how to setup the bot on a new server
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title=self.language.HELP_SETUP_TITLE,
            description=self.language.HELP_SETUP_DESCRIPTION
        )
        embed.set_thumbnail(url=self.language.BOT_THUMBAIL)
        for field in self.language.HELP_SETUP_FIELDS:
            embed.add_field(name= field[0], value=field[1], inline=False)

        await self.ctx.send(embed = embed)
    async def help_commands(self):
        # Shows the available commands
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title=self.language.HELP_COMMAND_TITLE,
            description=self.language.HELP_COMMAND_DESCRIPTION
        )
        embed.set_thumbnail(url=self.language.BOT_THUMBAIL)
        for field in self.language.HELP_COMMAND_FIELDS:
            embed.add_field(name= field[0], value=field[1], inline=False)

        await self.ctx.send(embed = embed)
        
    async def configure(self):
        #Configure the server with the passed parammeters
        regex_exp = "\"(.*)\" \"(.*)\""
        command = re.split(regex_exp, self.ctx.message.content)
        
        if self.goblin.goblin_token:
            # If the server is already configured, return an error
            await self.ctx.send(content=self.language.ERROR_ALREADY_CONFIGURED)
        else:
            if len(command) >= 3:
                # Add the server to DB and reutn OK
                self.goblin.create_goblin(command[1], command[2])
                await self.ctx.send(content=self.language.SUCCESS_SERVER_CONFIGURED)
            else:
                # If there are not valid params, return an error

                await self.ctx.send(content=self.language.ERROR_SYNTAX_CONFIGURATION)

    async def reset(self):
        # Delete the server configuration
        #Only can be do it by an administrator
        if (self.ctx.message.author.server_permissions.administrator):
            if (self.goblin.league_name):
                self.goblin.delete_goblin()
                await self.ctx.send(content=self.language.SUCCESS_SERVER_RESET)
            else:
                await self.ctx.send(content=self.language.ERROR_NOT_CONFIGURED)
        else:
            await self.ctx.send(content=self.language.ERROR_NOT_ALLOWED)

    async def teams(self):
        #Shows the competition team list
        if not self.goblin.goblin_token:
            await self.ctx.send(content=self.language.ERROR_NOT_CONFIGURED)
        else:
            #Get data from GoblinSpy
            league = self.goblin.get_goblin_base_data()
            tournament = league.tournaments[self.goblin.tournament]
            if tournament:
                teams = ""
                coach = ""
                ranking = ""
                for team_position in tournament.ranking.ranking:
                    race_logo = get(self.ctx.message.guild.emojis, name = tournament.ranking.ranking[team_position].race)
                    if not race_logo: race_logo = ":grey_question:"
                    teams += "%s %s\n\n" %(race_logo, tournament.ranking.ranking[team_position].team_name)
                    coach += "%s\n\n" % (tournament.ranking.ranking[team_position].coach.display_name)
                    ranking += "%s\n\n" % (bloodBowl.Get_Ranking(team_position))
                

                embed = discord.Embed(
                   colour = discord.Colour.red(),
                   description = self.language.LAST_UPDATE % tournament.last_update,    
                   title = "Teams on %s" % self.goblin.tournament,
                )
                embed.add_field(name = ":trophy:", value=ranking, inline=True)
                embed.add_field(name = self.language.TEAM_NAME, value=teams, inline=True)
                embed.add_field(name = self.language.COACH, value=coach, inline=True)

                await self.ctx.send(embed=embed)
            else:
                await self.ctx.send(content=self.language.ERROR_DATA_NOT_FOUND)
    async def round(self):
        #Shows the specifyied or current round
        if not self.goblin.goblin_token:
            await self.ctx.send(content=self.language.ERROR_NOT_CONFIGURED)
        else:
            #Get data from GoblinSpy
            league = self.goblin.get_goblin_base_data()
            tournament = league.tournaments[self.goblin.tournament]
            if tournament:
                if tournament.type_of_competition != "ladder":

                    command = self.ctx.message.content.split()

                    if len(command) == 1: get_round = tournament.schedule.current_round
                    else: get_round = command[1]
                    # Add local team and visitor team (and result if the match has ended) on respective strings. Every string will be on a different column on embed message
                    local_teams = ""
                    visitor_teams = ""
                    results = ""
                    for match in tournament.schedule.schedule[get_round]:
                        print(match)
                        local_teams += "%s\n\n" % (match.local_team.team_name)
                        visitor_teams += " %s\n\n" % (match.visitor_team.team_name)
                        results += "%s - %s\n\n" % (match.local_score, match.visitor_score)
                    embed = discord.Embed(
                        title= self.language.ROUND % (get_round),
                        description = self.language.LAST_UPDATE % tournament.last_update,    
                        colour = discord.Colour.red()
                    )
                    embed.add_field(name = self.language.LOCAL_TEAM, value=local_teams, inline=True)
                    embed.add_field(name = self.language.VS, value=results, inline=True)
                    embed.add_field(name = self.language.VISITOR_TEAM, value=visitor_teams, inline=True)
                    await self.ctx.send(embed=embed)
                else:
                    await self.ctx.send(content=self.language.ERROR_NOT_SCHEDULE)

            else:
                await self.ctx.send(content=self.language.ERROR_DATA_NOT_FOUND)

    async def this_is_my_team(self):
        if not self.goblin.goblin_token:
            await self.ctx.send(content=self.language.ERROR_NOT_CONFIGURED)
        else:
            command = self.ctx.message.content.split()
            if (len(command) > 1):
                result = self.goblin.set_coach(command[1] , str(self.ctx.message.author), self.ctx.message.author.id)
                await self.ctx.send(content=result)
            else:
                await self.ctx.send(content=self.language.ERROR_SYNTAX_IAM)

    async def my_next_match(self):
        if not self.goblin.goblin_token:
            await self.ctx.send(content=self.language.ERROR_NOT_CONFIGURED)
        else:
            pass
           # 