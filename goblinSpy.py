import sqlite3, math, js2py, os, requests, models, bloodBowl
class GoblinSpy:
    def __init__(self, discord_id, league = None, tournament = None, goblin_token = None):
        self.league_name = league
        self.discord_id = discord_id
        self.tournament = tournament
        self.goblin_token = goblin_token
        self.database = sqlite3.connect(os.getenv('SQLITE_CONNECTION'))
        self.recover_goblin()
    def __str__(self):
        return ('Discord Server: %s - League: %s - Tournament: %s - Goblin: %s' % (self.discord_id, self.league_name, self.tournament, self.goblin_token))
    def recover_goblin(self):
        # Recover discord configuration info from database 
        cursor = self.database.cursor()
        cursor.execute('SELECT * FROM tournaments WHERE idDiscord=\'%s\'' % self.discord_id)
        goblin = cursor.fetchone()
        print(goblin)
        cursor.close()
        if goblin:
            self.league_name = goblin[2]
            self.tournament = goblin[3]
            self.goblin_token = goblin[4]
        else:
            return False

    def create_goblin(self, league, tournament):
        # create a new entry with passed values
        # Caluclate the safePath used on GoblinSpy page
        goblin_token = self.get_goblin_token(league, tournament)
        try:

            cursor = self.database.cursor()
            cursor.execute('INSERT INTO tournaments (idDiscord, league, tournament, goblinValue) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');' % (self.discord_id, league, tournament, goblin_token))
            self.database.commit()
            cursor.close()
            self.league_name = league
            self.tournament = tournament
            self.goblin_token = goblin_token
        except:
            print("Error al configurar el servidor")
    def delete_goblin(self):
        # Delete a config entry
        try:
            cursor = self.database.cursor()
            cursor.execute('DELETE FROM tournaments WHERE idDiscord=\'%s\'; ' +
                'DELETE FROM coaches WHERE idDiscord=\'%s\'' % self.discord_id, self.discord_id)
            self.database.commit()
            cursor.close()
        except:
            print("Error al eliminar")
    def get_goblin_token(self, league, tournament):
        # Calculate the safe path from Goblin Spy using the same JavaScript script
        jsScripts = '''
            function(k){var j=this;var e=j.toUTF8Array(k);var g="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";var p="";var n=[0,0,0,0,0,0,0,0];for(var f=0;f<e.length;f+=5){var o=Math.min(e.length-f,5);n=e.slice(f,f+o);n.reverse();while(n.length<8){n.push(0)}n.reverse();for(var m=((o+1)*8)-5;m>3;m-=5){var d=Math.floor(m/8);var h=m-d*8;var b=n.slice(n.length-d-1,n.length-d-1+2);var c=b.length>1?(b[0]<<8)+b[1]:b[0]<<8;var a=(c>>h);var l=a&31;p+=g[l]}}return p}
            function toUTF8Array(d){var a=[];for(var c=0;c<d.length;c++){var b=d.charCodeAt(c);if(b<128){a.push(b)}else{if(b<2048){a.push(192|(b>>6),128|(b&63))}else{if(b<55296||b>=57344){a.push(224|(b>>12),128|((b>>6)&63),128|(b&63))}else{c++;b=65536+(((b&1023)<<10)|(d.charCodeAt(c)&1023));a.push(240|(b>>18),128|((b>>12)&63),128|((b>>6)&63),128|(b&63))}}}}return a}
        '''
        goblin_token = js2py.eval_js(jsScripts)(league + "." + tournament)
        return str(goblin_token)

    def get_goblin_base_data(self):
        # Make a get request to recover de .json data from GoblinSpy
        goblin_request = requests.get(os.getenv('SPYURLBASE') + 'overview.' + self.goblin_token + '.json')
        if goblin_request.ok:
            return self.read_tournament(goblin_request.json())
        else:
            return None

    def read_tournament(self, json):
        # Se recuperan los datos del JSON 
        league = models.League(self.league_name)
        tournament = models.Tournament(discord_id=self.discord_id, tournament_name=self.tournament)
        # Ultima actualizacion de goblin spy
        tournament.last_update = json["Info"]["rows"][0][3]
        # Se guardan las instancias de equipos 
        all_teams = {}
        ranking = models.Ranking()
        # Lista de los equipos inscritos ordenados por puntuación
        ranking_data = json["LeagueStandings"]["rows"]
        for team_data in ranking_data:
            # team[10] es la casilla del coachbame. Get_Coach revisa si el nombre está inscrito en la DB de usuarios
            recover_coach = self.get_coach(team_data[10])
            coach = models.Coach(team_data[10], team_data[10])
            if recover_coach != team_data[10]:
                coach.display_name = recover_coach[0]
                coach.user_discord_id = recover_coach[1]
            # Se guarda la raza como el emoticono de la raza (bb<race_name>)
            team = models.Team(coach = coach, team_name=team_data[17], race=bloodBowl.Get_Race(int(team_data[16])), wins=team_data[22], draws=team_data[23], loses=team_data[24], rank=team_data[18], td=team_data[25])
            ranking.add_team(team)
            all_teams[team.team_name] = team
        # Primero se recuperan los datos del histórico. Después, si la competición no es de tipo escalera y tiene partidos programados, se recuperan estos, incluidos los ya jugados
        # NOTA: Se crea una nueva instancia de un mismo partido porque en el json no hay ningun identificador comun entre Matches y Schedule
        # Recuoperación del histórico
        tournament.ranking = ranking
        history = models.History()
        matches_data = json["Matches"]["rows"]
        for match_data in matches_data:
            match = models.Match(local_team=all_teams[match_data[14]], visitor_team=all_teams[match_data[17]], local_score=match_data[15], visitor_score=match_data[16], status="played", played_time=match_data[4])
            history.add_match(match)
        tournament.match_history = history
        schedule_data = json["Schedule"]["rows"]
        if schedule_data == None or len(schedule_data) == 0:
            tournament_type = "ladder"
        else:
            tournament_type = schedule_data[0][7]
            schedule = models.Schedule()
            for match_data in schedule_data:
                match = models.Match(local_team=all_teams[match_data[19]], visitor_team=all_teams[match_data[25]], local_score=match_data[29], visitor_score=match_data[30], status=match_data[10])
                if match.status == "scheduled":
                    if schedule.current_round == 0:
                        schedule.current_round = match_data[8]
                    # Recupera si los usuarios de dicord han establecido una hora para jugar
                    match.programmed_time = self.get_programmed_time(match)
                schedule.add_match(match_data[8], match)
            tournament.schedule = schedule
        league.add_tournament(tournament)
        return league
    def get_programmed_time(self, match):
        return ""
    def get_coach(self, bb_coach):
        # Recovers a discord user name from coach if he's already registered (uning !iam command)
        query = "SELECT discordName, idDiscord FROM coaches WHERE coachName = '%s' AND idDiscord = '%s';" % (bb_coach, self.discord_id)
        cursor = self.database.cursor()
        result = cursor.execute(query).fetchone()
        cursor.close()
        if result: return result
        else: return bb_coach

    def set_coach(self, bb_coach, discord_name, discord_user_id):
        coach = self.get_coach(bb_coach)
        if coach != bb_coach and coach[0] != discord_name: 
            return "This coach is already registered. If it's your coach name, talk with an administrator."
        elif self.get_user_registerd(discord_name): 
            query = "UPDATE coaches SET coachName = '%s' WHERE discordName = '%s' AND idDiscord='%s';" % (bb_coach,discord_name, self.discord_id)
            result =  "Your coach name has been updated"
        else: 
            query = "INSERT INTO coaches (idDiscord, coachName, discordName, discordUserId) VALUES ('%s', '%s', '%s', '%s')" % (self.discord_id, bb_coach, discord_name, discord_user_id)
            result = "You has been registered successfully!"
        cursor = self.database.cursor()
        cursor.execute(query)
        self.database.commit()
        cursor.close()
        return result

    def get_user_registerd(self, discord_name):
        query = "SELECT coachName FROM coaches WHERE discordName = '%s' AND idDiscord = '%s';" % (discord_name, self.discord_id)
        cursor = self.database.cursor()
        result = cursor.execute(query).fetchone()
        cursor.close()
        print(result)
        if result: return result
        else: return None
