import sqlite3

from lib import crypto

def read_servers(db):
    query = 'select ' \
            '	server.name,' \
            '	server.host,' \
            '	server.port,' \
            '	server.username,' \
            '	server.password as "password", ' \
            '	user.password as "key"' \
            'from ' \
            '	server ' \
            'inner join ' \
            '	user on ' \
            '		user.id = server.user_id'

    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def decrypt_password(server):
    return crypto.decrypt(server['password'], server['key']).decode('utf-8')

def read_and_decrypt_servers(db):
    processed = []
    servers = read_servers(db)

    for server in servers:
        password = None

        try:
            password = decrypt_password(server)
        except:
            continue

        this = {}
        this['name'] = server['name']
        this['host'] = server['host']
        this['port'] = server['port']
        this['username'] = server['username']
        this['password'] = password

        processed.append(this)

    return processed
