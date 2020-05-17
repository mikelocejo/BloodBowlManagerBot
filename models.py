class Match:
    def __init__(self, local_team = None, visitor_team= None, local_score = 0, visitor_score = 0, status = "", played_time = "", programmed_time = ""):
        self.id = 0
        self.local_team = local_team
        self.visitor_team = visitor_team
        self.local_score = local_score
        self.visitor_score = visitor_score
        self.status = status
        self.played_time = played_time
        self.programmed_time = programmed_time
class Team:
    def __init__(self, coach = None, team_name = "", race = "", wins = 0, loses = 0, draws = 0, rank = 0, td = 0):
        self.id = 0

        self.team_name = team_name
        self.race = race
        self.wins = wins
        self.loses = loses
        self.draws = draws
        self.rank = rank
        self.td = td
        self.coach = coach
        self.player = []
    def add_player(self, player):
        self.player.append(player)
class League:
    def __init__(self, league_name = ""):
        self.id = 0

        self.league_name = league_name
        self.tournaments = {}
    def add_tournament(self, tournament):
        self.tournaments[tournament.tournament_name] = tournament
class Tournament:
    def __init__(self, discord_id = None, tournament_name = "", organizer = None, type_of_competition = "", ranking = None, match_history = None, schedule = None, last_update = ""):
        self.id = 0
        self.discord_id = discord_id
        self.tournament_name = tournament_name
        self.organizer = organizer
        self.type_of_competition = type_of_competition
        self.ranking = ranking
        self.match_history = match_history
        self.schedule = schedule
        self.last_update = last_update
class Coach:
    def __init__(self, coach_name = "", display_name = "", user_discord_id = ""):
        self.id = 0
        self.coach_name = coach_name
        self.display_name = display_name
        self.user_discord_id = user_discord_id
class Ranking:
    def __init__(self):
        self.ranking =  {}
    def add_team(self, team, position = -1):
        if position == -1:  position = len(self.ranking.keys()) + 1
        self.ranking[position] = team
class Schedule:
    def __init__(self, current_round = 0):
        self.current_round = current_round
        self.schedule = {}
    def add_match(self, competition_round, match):
        if competition_round not in self.schedule.keys() or not self.schedule[competition_round]:
            self.schedule[competition_round] = []
        self.schedule[competition_round].append(match)
class History:
    def __init__(self, matches = []):
        self.matches = matches
    def add_match(self, match):
        self.matches.append(match)

class Player:
    def __init__(self, race = "", player_type = "", name="", lvl = 0, experience = 0, mobility=0,stamina=0,agility=0,armor=0, skills = [], injury=[], 
            touchdowns=0, received_ko = 0, inflicted_ko = 0):
        self.id = 0
        self.race = race
        self.type = player_type 
        self.name = name
