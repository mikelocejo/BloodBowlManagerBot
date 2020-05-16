import goblinSpy, re, discord, os, requests, bloodBowl
class Commands:
    def __init__(self, ctx):
        self.ctx = ctx

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
            elif command[1] == '3':
                await self.help_developing()
                return
        # If not list has been selected, it will show the default help, listing the others
        await self.help_generic()

    async def help_generic(self):
        # List the help chapters
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title="Blood Bowl Manager",
            description="To see a page, just add the page number after the bb2!help command.\nLike this: ```bb2!help 2```"
        )
        embed.set_thumbnail(url="https://i.imgur.com/8eptQlM.png")
        embed.add_field(name= "Chapter 1: Set up your tournament", value="Check the firsts steps on Blood Bowl Bot", inline=False)
        embed.add_field(name= "Chapter 2: Blood Bowl Commands", value="Check the available commands on Blood Bowl Bot after configure your tournament", inline=False)
        #embed.add_field(name= "Chapter 3: About us", value="Do you need more help? Any question or suggestion? Check this section to know how to contact with us.", inline=False)

        await self.ctx.send(embed = embed)

    async def help_setup(self):
        # Shows how to setup the bot on a new server
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title="Setup - Blood Bowl Manager",
            description="Follow the next steps to configure your tournament on the discord server"
        )
        embed.set_thumbnail(url="https://i.imgur.com/8eptQlM.png")
        embed.add_field(name= "#1 Allow GoblinSpy recover data from your tournament.", value="Join http://www.mordrek.com/goblinSpy/web/activate.html?, introduce your tournament data and click on \"Activate\" button.", inline=False)
        embed.add_field(name= "#2 Configure the tournament on the bot", value="Use ```bb2!config \"League name\" \"Tournament name\"```, including quotation marks, to configure the tournament.", inline=False)
        embed.add_field(name= "#3 Install the custom emojis", value="Install the following emoji package on your server with the races icons", inline=False)

        await self.ctx.send(embed = embed)
    async def help_commands(self):
        # Shows the available commands
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title="Commands - Blood Bowl Manager",
            description=" Use the following commands to get info about the configured tournament. Newly played matches may take a while to update."
        )
        embed.set_thumbnail(url="https://i.imgur.com/8eptQlM.png")
        embed.add_field(name= "```bb2!teams```", value="List all teams from the tournament", inline=False)
        embed.add_field(name= "```bb2!round <round number>```", value="Show the matches of the selected round. If no round is specified, it will show the current round.", inline=False)
        embed.add_field(name= "```bb2!myTeam <team name>```", value="Link your Discord acc to your BloodBowl nickname, changin the coach name by your discord id on the messages.", inline=False)

        await self.ctx.send(embed = embed)
    async def help_developing(self):
        # Shows how to contact with the developing team
        # TODO
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title="About Us - Blood Bowl Manager",
            description=""
        )
        embed.set_thumbnail(url="https://i.imgur.com/8eptQlM.png")


        await self.ctx.send(embed = embed)
        
    async def configure(self):
        #Configure the server with the passed parammeters
        regex_exp = "\"(.*)\" \"(.*)\""
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        command = re.split(regex_exp, self.ctx.message.content)
        
        if (goblin.league_name):
            # If the server is already configured, return an error
            await self.ctx.send(content="Ya existe una liga configurada en este servidor")
        else:
            if len(command) >= 3:
                # Add the server to DB and reutn OK
                goblin.Create_Goblin(command[1], command[2])
                await self.ctx.send(content="Servidor configurado correctamente!")
            else:
                # If there are not valid params, return an error

                await self.ctx.send(content="Utiliza el comando bb2!config \"Nombre de la liga\" \"Nombre del torneo\", incluyendo las comillas, para configurar la liga")

    async def reset(self):
        # Delete the server configuration
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        #Only can be do it by an administrator
        if (ctx.message.author.server_permissions.administrator):
            if (goblin.league_name):
                goblin.Delete_Goblin()
                await self.ctx.send(content="Se ha borrado la configuración de liga")
            else:
                await self.ctx.send(content="No hay ninguna liga configurada")
        else:
            await self.ctx.send(content="Solo los usuarios con permisos de administrador pueden eliminar la configuración de la liga")

    async def teams(self):
        #Shows the competition team list
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        if not goblin.goblin_token:
            await self.ctx.send(content="No hay ninguna liga configurada")
        else:
            #Get data from GoblinSpy
            goblin_data = goblin.Get_Goblin_Data()
            if goblin_data:
                data_teams = goblin_data['LeagueStandings']
                #TODO Modify format
                teams = ""
                coach = ""
                ranking = ""
                for index in range (0, len(data_teams["rows"])):
                    teams += "%s%s\n" %(bloodBowl.Get_Race(int(data_teams["rows"][index][16])), data_teams["rows"][index][17])
                    coach += "%s\n" % data_teams["rows"][index][10]
                    ranking += "%s\n" % (bloodBowl.Get_Ranking(index + 1))
                embed = discord.Embed(
                   colour = discord.Colour.red(),
                   title = "Teams on %s" % goblin.tournament,
                )
                embed.add_field(name = ":trophy:", value=ranking, inline=True)
                embed.add_field(name = "Team name", value=teams, inline=True)
                embed.add_field(name = "Coach", value=coach, inline=True)

                await self.ctx.send(embed=embed)
            else:
                await self.ctx.send(content="Error al recuperar los datos de la liga. Asegurate que ha sido dada de alta en: http://www.mordrek.com/goblinSpy/web/goblinSpy.html")
    async def round(self):
        #Shows the specifyied or current round
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        if not goblin.goblin_token:
            await self.ctx.send(content="No hay ninguna liga configurada")
        else:
            #Get data from GoblinSpy
            goblin_data = goblin.Get_Goblin_Data()
            if goblin_data and goblin_data["Schedule"]:
                next_matches = []
                command = self.ctx.message.content.split()
                embed = discord.Embed(
                   colour = discord.Colour.red()
                )
                if len(command) == 1:
                    actual_round = 0
                    # If no round has been specifyied, it will calculate the current round
                    for match in goblin_data["Schedule"]["rows"]:
                        if match[10] == 'scheduled' and (match[8] == actual_round or actual_round == 0):
                            actual_round = match[8]
                            break
                    embed.title="Current round: Round %s" % actual_round

                else:
                    # Else specify the round
                    actual_round = command[1]
                    embed.title="Round %s" % actual_round

                for match in goblin_data["Schedule"]["rows"]:
                    if match[8] == actual_round:
                        next_matches.append(match)
                    if match[8] > actual_round:
                        break
                # Add local team and visitor team (and result if the match has ended) on respective strings. Every string will be a diferent column on embed message
                local_teams = ""
                visitor_teams = ""
                results = ""
                for match in next_matches:
                    local_teams += "(%s) %s\n\n" % (match[17], match[19] )
                    visitor_teams += " %s (%s) \n\n" % (  match[25], match[23])
                    if match[10] == 'played':
                        results += "%i - %i\n\n" % (int(match[29]), int(match[30]))
                    else:
                        results += "? - ?\n\n"

                embed.add_field(name = "Local Team", value=local_teams, inline=True)
                embed.add_field(name = "VS", value=results, inline=True)
                embed.add_field(name = "Visitor Team", value=visitor_teams, inline=True)


                await self.ctx.send(embed=embed)
                
            else:
                await self.ctx.send(content="No hay datos de la liga o no se trata de una liga con rondas")