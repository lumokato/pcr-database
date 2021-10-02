from PCRApi import PCRApi
from PCRSql import *
import json, csv
import multiprocessing

def read_clan_list():
    sql_list = get_clan_id()
    if sql_list:
        sql_id_max = sql_list[-1]
    else:
        sql_id_max = 0
    csv_list = []
    with open('clan_full.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if int(line[1]) > sql_id_max:
                csv_list.append(int(line[1]))
        csvfile.close()
    return csv_list

def insert_sql(app, clan_id):
    clan_data = app.query_clan(clan_id)
    if 'clan' in clan_data:
        insert_new_clan_detail(clan_data)
    print('已更新公会'+str(clan_id))


def insert_clan_new():
    with open('account.json') as f:
        account_data = json.load(f)
    account = account_data["new3"]
    App = PCRApi(account['viewer_id'], account['uid'], account['access_key'])
    id_list = read_clan_list()
    for clan_id in [5936]:
    # for clan_id in range(44129,50000):
        clan_data = App.query_clan(clan_id)
        if 'clan' in clan_data:
            insert_new_clan_detail_validate(clan_data)
        print('已更新公会'+str(clan_id))

def merge_clan():
    #data_clan = {**get_sql_clan('pcr_qd.db'), **get_sql_clan('pcr_qda.db'), **get_sql_clan('pcr_qdb.db'), **get_sql_clan('pcr_qdc.db')}
    #insert_merge_clan(data_clan)
    data_clan_members = {**get_sql_clan_members('pcr_qd.db'), **get_sql_clan_members('pcr_qda.db'), **get_sql_clan_members('pcr_qdb.db'), **get_sql_clan_members('pcr_qdc.db')}
    insert_merge_clan_members(data_clan_members)

def insert_clan_month():
    top_id_list = get_clan_top()
    with open('account.json') as f:
        account_data = json.load(f)
    account = account_data["new2"]
    App = PCRApi(account['viewer_id'], account['uid'], account['access_key'])
    for clan_id in top_id_list:
        if clan_id > 0:
            clan_data = App.query_clan(clan_id)
            if 'clan' in clan_data:
                insert_new_clan_detail_validate(clan_data)
            print('已更新公会'+str(clan_id))

def insert_clan_all():
    with open('account.json') as f:
        account_data = json.load(f)
    account = account_data["new2"]
    App = PCRApi(account['viewer_id'], account['uid'], account['access_key'])
    id_list = read_clan_list()
    for clan_id in range(44594,50000):
        clan_data = App.query_clan(clan_id)
        if 'clan' in clan_data:
            insert_new_clan_all_validate(clan_data)
        print('已更新公会'+str(clan_id))

if __name__ == "__main__":
    # create_sql_clan_detail('pcr_qd2109.db')
    # create_sql_clan_members('pcr_qd2109.db')
    # insert_clan_all()
    insert_clan_new()
    #insert_clan_month()
    