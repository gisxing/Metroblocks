# Andrew Quintanilla
# Manages the high score list
import sqlite3
dbname = 'database.db'

# Checks if there exists a table matching name
    def CheckTable(name):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE name='{0}'".format(name))
        namelist = c.fetchall()
        conn.close()
        if nameslist:
            return True
        else:
            return False

# Holds top 10 high scores
def Highscores():
    def __init__(self):
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()
        if not CheckTable('highscores'):
            self.c.execute('CREATE TABLE highscores (id ' + \
                'INTEGER PRIMARY KEY, name TEXT, score INTEGER)')
        conn.commit()

    # Returns high scores 
    def View(self):
        self.c.execute('SELECT id FROM highscores')
        ids = self.c.fetchall()
        highscores = []
        for i in ids:
            self.c.execute('SELECT name,score FROM highscores WHERE '\
                +'id={0}'.format(i))
            highscores.append(self.fetchone())
        return highscores

    # Checks if score is a high score
    def CheckScore(self, score):
        self.c.execute('SELECT score FROM highscores')
        strhighscores = self.c.fetchall()
        highscores = []
        for st in strhighscores:
            highscores.append(int(st))
        for h in highscores:
            if score > h:
                return True
        return False

    # Removes lowest score from table, inserts new score
    def InsertScore(self, name, score):
##        self.c.execute('SELECT id from ( '+\
##            '
##        toremove = self.c.fetchone()
        pass

    def close():
        self.conn.close()
