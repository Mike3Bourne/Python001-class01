import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'ak123',
    'db' : 'test'
}

# sqls = ['select 1', 'select VERSION()']
sql = ["insert into movies (film_name, film_type, film_date) values ('醉酒','喜剧', '2020-09-21');"]
# result = []

class ConnDB(object):
    def __init__(self, dbInfo, sql):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        # self.sqls = sqls
        self.sql = sql

        # self.run()

    def run(self):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )
        # 游标建立的时候就开启了一个隐形的事务
        cur = conn.cursor()
        try:
            
            cur.execute(self.sql)
            cur.execute("select * from movies;")
            
            print(cur.fetchall())

            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()
    # def select(self):
    #     pass

    # def insert(self):
    #     pass



if __name__ == "__main__":
    
    print(sql)
    db = ConnDB(dbInfo,sql)
    db.run()

    