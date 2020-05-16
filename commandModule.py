import goblinSpy, re, discord, os, requests, bloodBowl
class Commands:
    def __init__(self, ctx):
        self.ctx = ctx


    async def configure(self):
        regex_exp = "\"(.*)\" \"(.*)\""
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        command = re.split(regex_exp, self.ctx.message.content)
        
        if (goblin.league_name):
            await self.ctx.send(content="Ya existe una liga configurada en este servidor")
        else:
            if len(command) >= 3:
                goblin.Create_Goblin(command[1], command[2])
                print(goblin)
                await self.ctx.send(content="Servidor configurado correctamente!")
            else:
                await self.ctx.send(content="Utiliza el comando bb2!config \"Nombre de la liga\" \"Nombre del torneo\", incluyendo las comillas, para configurar la liga")

    async def reset(self):
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
            
        if (goblin.league_name):
            goblin.Delete_Goblin()
            await self.ctx.send(content="Se ha borrado la configuración de liga")
        else:
            await self.ctx.send(content="No hay ninguna liga configurada")

    async def teams(self):
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        if not goblin.goblin_token:
            await self.ctx.send(content="No hay ninguna liga configurada")
        else:
            goblin_request = requests.get(os.getenv('SPYURLBASE') + 'overview.' + goblin.goblin_token + '.json')
            if goblin_request.ok:
                league_data = goblin_request.json()
                data_teams = league_data['LeagueStandings']
                teams = ('Teams on %s:\n' % goblin.league_name)
                ranking = 1
                for team in data_teams["rows"]:
                    teams += ("#%i %s%s (%s)\n" % (ranking, bloodBowl.Get_Race(int(team[16])), team[17], team[10]))
                    ranking += 1
                await self.ctx.send(content=teams)
            else:
                await self.ctx.send(content="Error al recuperar los datos de la liga. Asegurate que ha sido dada de alta en: http://www.mordrek.com/goblinSpy/web/goblinSpy.html")
    async def round(self):
        goblin = goblinSpy.GoblinSpy(self.ctx.message.guild.id)
        if not goblin.goblin_token:
            await self.ctx.send(content="No hay ninguna liga configurada")
        else:
            goblin_data = goblin.GetGoblinData()
            if goblin_data:
                next_matches = []
                command = self.ctx.message.content.split()
                if len(command) == 1:
                    actual_round = 0
                    for match in goblin_data["Schedule"]["rows"]:
                        if match[10] == 'scheduled' and (match[8] == actual_round or actual_round == 0):
                            actual_round = match[8]
                            break
                else:
                    actual_round = command[1]
                for match in goblin_data["Schedule"]["rows"]:
                    if match[8] == actual_round:
                        next_matches.append(match)
                    if match[8] > actual_round:
                        break
                response = 'Current Round (round %i):\n' % int(actual_round)
                for match in next_matches:
                    if match[10] == 'played':
                        response += '%s (%s) %i VS %i %s (%s)\n'% (match[19], match[17], int(match[29]), int(match[30]) ,  match[25], match[23])
                    else:
                        response += '%s (%s) VS %s (%s)\n' % (match[19], match[17], match[25], match[23])
                await self.ctx.send(content=response)
            else:
                await self.ctx.send(content="Error al recuperar los datos de la liga. Asegurate que ha sido dada de alta en: http://www.mordrek.com/goblinSpy/web/goblinSpy.html")