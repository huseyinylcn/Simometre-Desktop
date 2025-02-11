
import sqlite3


class dbWrite():
    def __init__(self):
        super().__init__()


    def dbConnect (self):
        return sqlite3.connect('sismo.db')


    def serialinfoSave(self,port='',bound=''):
        conn = self.dbConnect()
        cursorr = conn.cursor()
        cursorr.execute('''
    UPDATE users
    SET serialport = ?, boundspeed = ?
    WHERE 1 = 1
''', (port, bound))
       
        conn.commit()
        conn.close()
    
    def dbInfoGet(self):
        conn = self.dbConnect()
        cursorr = conn.cursor()
        cursorr.execute('''
select * from users
''')
        data = cursorr.fetchall()[0]
        conn.commit()
        conn.close()
        
        return data
    
    def dbuserPasw(self,username,password):

        # !burada şifreleri kayıt etmeden önce sunucuya gönderip doğru alup olmadığını kontrol et doğru ise sunucudaki kayıtlı is numarasını al buradaki tabloya yz


        conn = self.dbConnect()
        cursorr = conn.cursor()
        cursorr.execute('''
    UPDATE users
    SET username = ?, password = ?
    WHERE 1 = 1
''', (username, password))
       
        conn.commit()
        conn.close()

    def dbUrlSave(self,url=''):
        print(url)
        conn = self.dbConnect()
        cursorr = conn.cursor()

        cursorr.execute(f'''
    UPDATE users
    SET url = '{url}'
    WHERE 1 = 1
''')
       
        conn.commit()
        conn.close()

