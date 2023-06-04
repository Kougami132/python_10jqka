import pymysql

class DataBase:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='1329623049', port=3306, charset='utf8', autocommit=True)
        self.cursor = self.db.cursor()
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS stock')
        self.cursor.execute('USE stock')
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS stock_data (
                        Id INT,
                        Code VARCHAR(255),
                        Name VARCHAR(255),
                        Value FLOAT,
                        Time INT
                        );
                        ''')
    def save(self, id, code, name, value, time):
        sql = 'INSERT INTO stock_data (Id, Code, Name, Value, Time) VALUES '
        for i in range(len(id)):
            sql += f"({id[i]}, '{code[i]}', '{name[i]}', {value[i]}, {time}),"
        sql = sql[:len(sql) - 1] + ';'
        self.cursor.execute(sql)

    def get(self, id):
        sql = f'SELECT * FROM stock_data WHERE Id = {id};'
        self.cursor.execute(sql)
        return self.cursor.fetchall()