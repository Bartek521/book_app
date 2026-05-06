import sqlite3

class UserAction :
    def __init__(self,database):
        self.database = database
    def CheckUsers(self,email):
        with self.database.GetConnectionDb() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT ID_USER FROM USERS WHERE EMAIL = ?",(email,))
            if cursor.fetchall():
                return True
            else:
                return False
    def AddUser(self, name,lastname,email,password,rola):
        try:
            with self.database.GetConnectionDb() as connect:
                if self.CheckUsers(email):
                    return False,"Email jest już przypisany do innego użytkownika"
                else:
                    cursor = connect.cursor()
                    cursor.execute("INSERT INTO USERS(NAME,LASTNAME,EMAIL,PASSWORD,ROLA) VALUES(?,?,?,?,?)",(name,lastname,email,password,rola))
                    return True,"Konto zostało utworzone"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych :{e}"
    def Login(self,email, password):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT ID_USER FROM USERS WHERE (UPPER(EMAIL)=UPPER(?) AND PASSWORD = ?)",(email,password,))
                user = cursor.fetchall()
                if user:
                    return user,"Użytkownik zalogowany",
                else:
                    return False,"Użytkownik nie posiada konta, najpierw zarejestruj się."
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych : {e}"
    def EditPassword(self,email,oldpassword,newpassword):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT NAME FROM USERS WHERE EMAIL = ? AND PASSWORD = ?", (email,oldpassword,))
                check = cursor.fetchall()
                if check:
                    cursor.execute("UPDATE USERS SET PASSWORD = ? WHERE EMAIL = ?",(newpassword,email))
                    return True, f"Zaktualizowano hasło"
                else:
                    return False,f"Użytkownik o takim emailu nie istnieje"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych : {e}"

    def CheckBook(self,barcode):
        with self.database.GetConnectionDb() as connect:
            cursor = connect.cursor()
            cursor.execute("SELECT ID_BOOK FORM BOOKS WHERE BARCODE=?",(barcode,))
            book = cursor.fetchall()
            if book:
                return True
            else:
                return False
    def AddBook(self,barcode,title,author,publishing_house,year,kind,id_user):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                book = self.CheckBook(barcode)
                if book:
                    return False,"Książka o takim kodzie kreskowym już istnieje"
                else:
                    cursor.execute("INSERT INTO BOOKS(BARCODE,TITLE,AUTHOR,PUBLISHING_HOUSE,YEAR,KIND,ID_USER) VALUES (?,?,?,?,?,?,?)",
                                   (barcode, title, author, publishing_house, year, kind,id_user))
                    return True,"Dodano książkę do bazy"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych: {e}"
    def AddToList(self,barcode,id_user, status, rate ,note):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT ID_BOOK FROM BOOKS WHERE BARCODE = ?",(barcode,))
                book = cursor.fetchall()
                if book:
                    cursor.execute("INSERT INTO MAGAZINE(ID_USER,ID_BOOK,STATUS,RATE,NOTES) VALUES(?,?,?,?,?)",(id_user,book[0],status,rate,note))
                    return True,f"Dodano książkę do listy : {status}"
                else:
                    return False,f"Najpierw dodaj książkę do bazy książek"
        except sqlite3.Error as e:
            return False,f"Błąd bazy danych: {e}"
    def DownloadList(self,id_user, status):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute('''SELECT * FROM BOOKS b JOIN MAGAZINE m ON b.ID_BOOK = m.ID_BOOK
                                  WHERE m.ID_USER = ? AND m.STATUS = ?''',(id_user,status,))
                books = cursor.fetchall()
                return books
        except sqlite3.Error as e:
            return False,f"Błąd przy pobieraniu listy : {e}"
    def UpdateStatus(self,id_user,barcode,new_status):
        try:
            with self.database.GetConnectionDb() as connect:
                cursor = connect.cursor()
                cursor.execute("SELECT ID_BOOK FROM BOOKS WHERE BARCODE = ?",(barcode,))
                book_id = cursor.fetchone()[0]

                cursor.execute('''UPDATE MAGAZINE SET STATUS = ?
                                  WHERE ID_USER = ? AND ID_BOOK = ?''',
                                  (new_status,id_user,book_id))
                return True,"Zaktualizowano status"
        except Exception as e:
            return False,f"Błąd przy bazie danych : {e}"