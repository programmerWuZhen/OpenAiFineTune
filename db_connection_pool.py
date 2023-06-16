import pymysql
# 数据库连接池
connection_pool = []
# 初始化数据库连接池
def init_connection_pool(num,mydb):
    for i in range(num):
        conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root1201',
                charset='utf8',
                db=mydb)
        connection_pool.append(conn)
    return connection_pool

# 从连接池中获取数据库连接
def get_connection():
    return connection_pool.pop()

# 归还数据库连接到连接池
def return_connection(conn):
    connection_pool.append(conn)
 
def close_connection_pool():
    for i in range(len(connection_pool)):
        conn = connection_pool.pop() 
        conn.close()