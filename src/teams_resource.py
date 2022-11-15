import pymysql

import os


class TeamsResources:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        # usr = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        usr = "admin"
        pw = "dbuserdbuser"
        h = "e61561.cxstuweu8lu4.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_teams():

        sql = "select * from f22_databases.Team"
        conn = TeamsResources._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @staticmethod
    def get_teams_info(id):

        sql = "select * from f22_databases.Team where Team_ID =  %s"
        conn = TeamsResources._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result

    @staticmethod
    def get_teams_games(id):

        sql = "select distinct game_id, Team_Abbrev as away, Team_Score as away_score, Opponent_Score as home_score, Opponent_Abbrev as home from f22_databases.Game where (Team_Abbrev = %s or Opponent_Abbrev = %s) and Opponent_Abbrev = substr(game_id, 10) order by game_date desc limit 82;"
        conn = TeamsResources._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=[id, id])
        result = cur.fetchall()

        for r in result:
            game_id = r["game_id"]
            year = game_id[:4]
            mon = game_id[4:6]
            day = game_id[6:8]
            date = year + "-" + mon + "-" + day
            r["game_date"] = date

        return result

