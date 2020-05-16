import sqlite3, math, js2py, os, requests
class GoblinSpy:
    def __init__(self, discord_id,database = None, league = None, tournament = None, goblin_token = None):
        self.league_name = league
        self.discord_id = discord_id
        self.tournament = tournament
        self.goblin_token = goblin_token
        self.database = sqlite3.connect(os.getenv('SQLITE_CONNECTION'))
        self.Recover_Goblin()
    def __str__(self):
        return ('Discord Server: %s - League: %s - Tournament: %s - Goblin: %s' % (self.discord_id, self.league_name, self.tournament, self.goblin_token))
    def Recover_Goblin(self):
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

    def Create_Goblin(self, league, tournament):
        goblin_token = self.GetGoblinUrl(league, tournament)
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
    def Delete_Goblin(self):
        try:
            cursor = self.database.cursor()
            print(self.discord_id)
            cursor.execute('DELETE FROM tournaments WHERE idDiscord=\'%s\';' % self.discord_id)
            self.database.commit()
            cursor.close()
        except:
            print("Error al eliminar")
    def GetGoblinUrl(self, league, tournament):
        jsScripts = '''
            function(k){var j=this;var e=j.toUTF8Array(k);var g="ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";var p="";var n=[0,0,0,0,0,0,0,0];for(var f=0;f<e.length;f+=5){var o=Math.min(e.length-f,5);n=e.slice(f,f+o);n.reverse();while(n.length<8){n.push(0)}n.reverse();for(var m=((o+1)*8)-5;m>3;m-=5){var d=Math.floor(m/8);var h=m-d*8;var b=n.slice(n.length-d-1,n.length-d-1+2);var c=b.length>1?(b[0]<<8)+b[1]:b[0]<<8;var a=(c>>h);var l=a&31;p+=g[l]}}return p}
            function toUTF8Array(d){var a=[];for(var c=0;c<d.length;c++){var b=d.charCodeAt(c);if(b<128){a.push(b)}else{if(b<2048){a.push(192|(b>>6),128|(b&63))}else{if(b<55296||b>=57344){a.push(224|(b>>12),128|((b>>6)&63),128|(b&63))}else{c++;b=65536+(((b&1023)<<10)|(d.charCodeAt(c)&1023));a.push(240|(b>>18),128|((b>>12)&63),128|((b>>6)&63),128|(b&63))}}}}return a}
        '''
        goblin_token = js2py.eval_js(jsScripts)(league + "." + tournament)
        print(goblin_token)
        return str(goblin_token)
    def GetGoblinData(self):
        goblin_request = requests.get(os.getenv('SPYURLBASE') + 'overview.' + self.goblin_token + '.json')
        if goblin_request.ok:
            return goblin_request.json()
            
        else:
            return None