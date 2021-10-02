import datetime
import sqlite3
import time, re

def validate(name):
    rstr = r"[\/\\\:\*\?\'\"\<\>\|\-\+\%]"
    new_name = re.sub(rstr,"''", name)
    return new_name
# 创建 TABLE clan_detail
def create_sql_clan_detail(database):
    conn = sqlite3.connect(database)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS `clan_detail`")
    # 使用预处理语句创建表
    sql = """CREATE TABLE `clan_detail` ( 
            "clan_id"	INTEGER NOT NULL UNIQUE,
            "clan_name"	TEXT NOT NULL,
            "leader_name"	TEXT NOT NULL,
            "leader_viewer_id"	INTEGER NOT NULL,
            "join_condition"	INTEGER NOT NULL,
            "activity"	INTEGER NOT NULL,
            "member_num"	INTEGER NOT NULL,
            "current_period_ranking"	INTEGER NOT NULL,
            "grade_rank"	INTEGER NOT NULL,
            "discard_status"	INTEGER,
            "name_history"	TEXT,
            "refresh_time"	TEXT NOT NULL,
            PRIMARY KEY("clan_id")
            )"""
    cursor.execute(sql)
    print("CREATE TABLE clan_detail OK")
    cursor.close()
    conn.close()

# 创建 TABLE clan_members
def create_sql_clan_members(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS `clan_members`")
    # 使用预处理语句创建表
    sql = """CREATE TABLE `clan_members` ( 
            "viewer_id"	INTEGER NOT NULL UNIQUE,
            "name"	TEXT NOT NULL,
            "level"	INTEGER NOT NULL,
            "role"	INTEGER NOT NULL,
            "total_power"	INTEGER NOT NULL,
            "join_clan_id"	INTEGER,
            "join_clan_name"	TEXT,
            "last_login_time"	TEXT NOT NULL,
            "join_clan_history"	TEXT,
            "name_history"	TEXT,
            "last_refresh_time"	TEXT NOT NULL,
            PRIMARY KEY("viewer_id")
            )"""
    cursor.execute(sql)
    print("CREATE TABLE clan_members OK")
    cursor.close()
    conn.close()

# 将 clan 信息第一次添加到TABLE中
def insert_new_clan_detail(clan_data):
    clan_dict = clan_data['clan']['detail']
    conn = sqlite3.connect('pcr_qd2108.db')
    cursor = conn.cursor()
    insert_keys = ["clan_id", "clan_name", "leader_name", "leader_viewer_id", "join_condition", "activity", "member_num", "current_period_ranking", "grade_rank"]
    ROWstr = ''
    COLstr = ''
    for key in insert_keys:
        COLstr=(COLstr+'%s'+',')%key
        ROWstr=(ROWstr+"'%s'"+',')%(clan_dict[key])
    sqlrow = """INSERT INTO `clan_detail` (%s) VALUES (%s)"""%(COLstr[:-1]+",name_history,refresh_time",ROWstr[:-1]+",'"+clan_dict["clan_name"]+"',"+time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime()))
    cursor.execute(sqlrow)
    #添加 members 信息
    members_list = clan_data['clan']['members']
    insert_keys = ['viewer_id', 'name', 'level', 'role', 'total_power']
    for member in members_list:
        ROWstr = ''
        COLstr = ''
        for key in insert_keys:
            COLstr=(COLstr+'%s'+',')%key
            ROWstr=(ROWstr+"'%s'"+',')%(member[key])
        COLstr = COLstr + 'join_clan_id,join_clan_name,last_login_time,join_clan_history,name_history,last_refresh_time' 
        ROWstr = ROWstr + str(clan_dict['clan_id']) + ",'" + clan_dict["clan_name"] +"'," + time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime(member['last_login_time'])) + ',' + str(clan_dict['clan_id']) + ",'" + member['name'] + "'"
        sqlrow = """INSERT INTO `clan_members` (%s) VALUES (%s)"""%(COLstr,ROWstr+','+time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime()))
        cursor.execute(sqlrow)    
    conn.commit()
    cursor.close()
    conn.close()

def insert_new_clan_detail_validate(clan_data):
    clan_dict = clan_data['clan']['detail']
    conn = sqlite3.connect('pcr_qd2109.db')
    cursor = conn.cursor()
    insert_keys = ["clan_id", "clan_name", "leader_name", "leader_viewer_id", "join_condition", "activity", "member_num", "current_period_ranking", "grade_rank"]
    ROWstr = ''
    COLstr = ''
    for key in insert_keys:
        COLstr=(COLstr+'%s'+',')%key
        if key == "clan_name" or key == "leader_name":
            ROWstr=(ROWstr+"'%s'"+',')%(validate(clan_dict[key]))
        else:
            ROWstr=(ROWstr+"'%s'"+',')%(clan_dict[key])
    sqlrow = """INSERT INTO `clan_detail` (%s) VALUES (%s)"""%(COLstr[:-1]+",name_history,refresh_time",ROWstr[:-1]+",'"+validate(clan_dict["clan_name"])+"',"+time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime()))
    cursor.execute(sqlrow)
    #添加 members 信息
    members_list = clan_data['clan']['members']
    insert_keys = ['viewer_id', 'name', 'level', 'role', 'total_power']
    for member in members_list:
        ROWstr = ''
        COLstr = ''
        for key in insert_keys:
            COLstr=(COLstr+'%s'+',')%key
            if key == "name":
                ROWstr=(ROWstr+"'%s'"+',')%(validate(member[key]))
            else:
                ROWstr=(ROWstr+"'%s'"+',')%(member[key])
        COLstr = COLstr + 'join_clan_id,join_clan_name,last_login_time,join_clan_history,name_history,last_refresh_time' 
        ROWstr = ROWstr + str(clan_dict['clan_id']) + ",'" + validate(clan_dict["clan_name"]) +"'," + time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime(member['last_login_time'])) + ',' + str(clan_dict['clan_id']) + ",'" + validate(member['name']) + "'"
        sqlrow = """INSERT INTO `clan_members` (%s) VALUES (%s)"""%(COLstr,ROWstr+','+time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime()))
        cursor.execute(sqlrow)
    conn.commit()
    cursor.close()
    conn.close()

# 添加新clan信息至all.db
def insert_new_clan_all_validate(clan_data):
    clan_dict = clan_data['clan']['detail']
    conn = sqlite3.connect('pcr_qdall.db')
    cursor = conn.cursor()
    insert_keys = ["clan_id", "clan_name", "leader_name", "leader_viewer_id", "join_condition", "activity", "member_num", "current_period_ranking", "grade_rank"]
    ROWstr = ''
    COLstr = ''
    for key in insert_keys:
        COLstr=(COLstr+'%s'+',')%key
        if key == "clan_name" or key == "leader_name":
            ROWstr=(ROWstr+"'%s'"+',')%(validate(clan_dict[key]))
        else:
            ROWstr=(ROWstr+"'%s'"+',')%(clan_dict[key])
    sqlrow = """INSERT INTO `clan_detail` (%s) VALUES (%s)"""%(COLstr[:-1]+",name_history,refresh_time",ROWstr[:-1]+",'"+validate(clan_dict["clan_name"])+"',"+time.strftime("'%Y-%m-%d %H:%M:%S'", time.localtime()))
    cursor.execute(sqlrow)
    conn.commit()
    cursor.close()
    conn.close()

# 从数据库中获取 clan_id 信息, 并返回字典
def get_clan_id():
    clan_id_list = []
    conn = sqlite3.connect('pcr_qd.db')
    cursor = conn.cursor()
    sql = """SELECT clan_id FROM `clan_detail`"""
    try:
        cursor.execute(sql)
        for id_tuple in cursor:
            for clan_id in id_tuple:
                clan_id_list.append(clan_id)
        clan_id_list.sort()        
        return clan_id_list
    except Exception as e:
        print('Error', e)
        conn.rollback()
    conn.close()

def get_sql_clan(database):
    clan_detail_dict = {}
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    COLstr = "clan_id,clan_name,leader_name,leader_viewer_id,join_condition,activity,member_num,current_period_ranking,grade_rank,name_history,refresh_time"
    sql = """SELECT %s FROM `clan_detail`"""%COLstr
    try:
        cursor.execute(sql)
        for user in cursor:
            clan_detail_dict[user[0]] = user
        return clan_detail_dict
    except Exception as e:
        print('Error', e)
        conn.rollback()
    conn.close()

def get_sql_clan_members(database):
    clan_members_dict = {}
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    #COLstr = "viewer_id,name,level,role,total_power,join_clan_id,join_clan_name,last_login_time,join_clan_history,name_history,last_refresh_time"
    sql = """SELECT * FROM `clan_members`"""
    try:
        cursor.execute(sql)
        for user in cursor:
            clan_members_dict[user[0]] = user
        return clan_members_dict
    except Exception as e:
        print('Error', e)
        conn.rollback()
    conn.close()

def insert_merge_clan(clan_dict):
    conn = sqlite3.connect('pcr_qdall.db')
    cursor = conn.cursor()
    for clan in clan_dict.values():
        COLstr = "clan_id,clan_name,leader_name,leader_viewer_id,join_condition,activity,member_num,current_period_ranking,grade_rank,name_history,refresh_time"
        sqlrow = """INSERT INTO `clan_detail`(%s) VALUES %s """%(COLstr,str(clan))
        cursor.execute(sqlrow)
    conn.commit()
    cursor.close()
    conn.close()

def insert_merge_clan_members(clan_dict):
    conn = sqlite3.connect('pcr_qdall.db')
    cursor = conn.cursor()
    for clan in clan_dict.values():
        #COLstr = "clan_id,clan_name,leader_name,leader_viewer_id,join_condition,activity,member_num,current_period_ranking,grade_rank,name_history,refresh_time"
        sqlrow = """INSERT INTO `clan_members` VALUES %s """%(str(clan))
        cursor.execute(sqlrow)
    conn.commit()
    cursor.close()
    conn.close()


# 从数据库中获取上期会战前1500名公会id
def get_clan_top():
    clan_id_list = []
    conn = sqlite3.connect('pcr_qd2108.db')
    cursor = conn.cursor()
    sql = """SELECT clan_id,current_period_ranking FROM `clan_detail`"""
    try:
        cursor.execute(sql)
        for clan in cursor:
            if clan[1] < 1501 and clan[1] > 0:
                clan_id_list.append(clan[0])
        return clan_id_list
    except Exception as e:
        print('Error', e)
        conn.rollback()
    conn.close()
    # # 删除 artist 中数据
    # def del_sql_artist(id_del):
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     sql = "DELETE FROM `artist` WHERE id_artist = %s" % id_del
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except Exception as e:
    #         print('Error', e)
    #         db.rollback()
    #     db.close()


    # # 创建 TABLE album
    # def create_sql_album():
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     cursor.execute("DROP TABLE IF EXISTS `album`")
    #     sql = """CREATE TABLE `album` ( 
    #             id_album  INT(10) NOT NULL, 
    #             name_album  VARCHAR(80) NOT NULL,
    #             id_artist  INT(10) NOT NULL, 
    #             name_artist  VARCHAR(40) NOT NULL,
    #             comment_url_album  VARCHAR(20),
    #             PRIMARY KEY (id_album)
    #             )"""
    #     cursor.execute(sql)
    #     print("CREATE TABLE album OK")
    #     db.close()


    # # 将 album 信息添加到TABLE中
    # def insert_sql_album(id_album, name_album, id_group, name_group, comment_url_album):
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     sql = "INSERT INTO `album` (id_album, name_album, id_artist, " \
    #         "name_artist, comment_url_album) VALUES (%s, %s, %s, %s, %s)"
    #     try:
    #         cursor.execute(sql, (id_album, name_album, id_group, name_group, comment_url_album))
    #         db.commit()
    #     except Exception as e:
    #         print('Error', e)
    #         db.rollback()
    #     db.close()


    # # 从数据库中获取 album 的 id 与 name 信息, 并返回字典
    # def get_sql_album():
    #     album_data = {}
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     sql = 'SELECT * FROM `album` WHERE 1=1'
    #     try:
    #         cursor.execute(sql)
    #         for user in cursor:
    #             album_data[user['id_album']] = user['name_album']
    #         db.commit()
    #         return album_data
    #     except Exception as e:
    #         print('Error', e)
    #         db.rollback()
    #     db.close()


    # # 删除 album 中数据
    # def del_sql_album(id_del):
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     sql = "DELETE FROM `album` WHERE id_album = %s" % id_del
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except Exception as e:
    #         print('Error', e)
    #         db.rollback()
    #     db.close()


    # # 增加 album 表的新列
    # def add_sql_album():
    #     db = pymysql.connect(**config)
    #     cursor = db.cursor()
    #     sql = "ALTER TABLE `album` ADD COLUMN size_album INT(5) NOT NULL"
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except Exception as e:
    #         print('Error', e)
    #         db.rollback()
    #     db.close()
