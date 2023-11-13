import sqlite3
import json
from datetime import datetime

# 创建数据库连接
conn = sqlite3.connect('data.db')
c = conn.cursor()

table_and_files = {'Users': 'users.json',
                   'UserTypes': 'usersType.json',
                   'AddFrom': 'addfrom.json',
                   'OrgTree':'orgTree.json'}

# 帐号 姓名 密码 加密方式 帐号有效期 部门 用户类型 邮箱 校外邮箱 手机号码 身份证号 帐号来源 帐号锁定状态 别名
# "自动编号" "帐号" "姓名" "密码" "加密方式" "帐号有效期" "部门" "用户类型" "邮箱" "校外邮箱" "手机号码" "身份证号" "帐号来源" "帐号锁定状态" "别名"
table_structures = {
    'Users': '''
        id INTEGER PRIMARY KEY, 
        userid TEXT, 
        cn TEXT, 
        passwd TEXT, 
        security TEXT, 
        lifetime TEXT, 
        departmetname TEXT, 
        usertype TEXT, 
        usertypename TEXT, 
        email TEXT, 
        outemail TEXT, 
        telnum TEXT,
        cardid TEXT, 
        lockstatus TEXT, 
        academy TEXT, 
        academyname TEXT, 
        xgmmsj TEXT, 
        addfrom TEXT, 
        container TEXT, 
        petname TEXT, 
        modifyEmailFlag INTEGER, 
        pwdstrength INTEGER, 
        qqopenid TEXT, 
        pwdpolicy INTEGER, 
        telVcode TEXT, 
        wxopenid TEXT, 
        inetuserstatus TEXT, 
        departmet TEXT, 
        userPswd TEXT, 
        teltime INTEGER''',
    'UserTypes': '''
        ID INTEGER PRIMARY KEY, 
        NAME TEXT''',
    'AddFrom': '''
        ADDFROM TEXT
        ''',
    'OrgTree':'''
    pid INTEGER, 
        isParent TEXT, 
        open TEXT,
        nocheck TEXT, 
        level INTEGER, 
        name TEXT, 
        id INTEGER PRIMARY KEY
    '''
}


def process_date(d):
    if d:
        return datetime.strptime(d, '%Y-%m-%d').strftime('%Y-%m-%d')
    return None


def process_datetime(dt):
    if dt:
        return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    return None


conversion_functions = {'lifetime': process_datetime,
                        'xgmmsj': process_date}


def process_data(data):
    for row in data:
        for k in row:
            f = conversion_functions.get(k)
            if f:
                row[k] = f(row[k])
    return data


def insert_data(data, table):
    for row in data:
        # 行数据中的所有键（即字段名）
        columns = ', '.join(row.keys())
        # 各个字段名对应的值
        placeholders = ', '.join(':' + str(col) for col in row.keys())

        try:
            c.execute(f'''
                INSERT INTO {table} ({columns}) VALUES ({placeholders})
            ''', row)
        except sqlite3.IntegrityError:
            # 如果发生了sqlite3.IntegrityError异常，尝试更新指定的行
            if table == "Users":
                assignments = ', '.join(str(col) + '=:' + str(col) for col in row.keys())
                c.execute(f'''
                    UPDATE {table} SET {assignments} WHERE id=:id
                ''', row)



def load_and_process_file(filename, table):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = process_data(data)
    insert_data(data, table)


for table, filename in table_and_files.items():
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table}(
        {table_structures[table]}
    )''')
    load_and_process_file(filename, table)

# Commit to the database
conn.commit()

# Close the connection
conn.close()
