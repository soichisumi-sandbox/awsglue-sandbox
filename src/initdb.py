import MySQLdb

con = MySQLdb.connect(
        user='user',
        passwd='password',
        host='0.0.0.0',
        db='database',
        charset='utf8',
    )

def init_db():
    cur= con.cursor()
    sql = "create table users (id int primary key auto_increment, name varchar(100) not null, email varchar(100) not null, created timestamp default CURRENT_TIMESTAMP);"
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

if __name__ == "__main__":
    init_db()