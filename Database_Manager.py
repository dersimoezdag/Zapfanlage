import sqlite3

DB_File = "Zapfanlage.db"

################################# Database
class DatabaseManager():
    def __init__(self):
        self.conn = sqlite3.connect(DB_File)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()
		
    def add_del_update_db_record(self, sql_query, args=()):
        print("Dantenbak Eintrag erfolgt...")
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def get_full_db_record(self, table):
        sql_select_Query = "SELECT * FROM " + table
        self.cur.execute(sql_select_Query)
        records = self.cur.fetchall()
        print("Total number of rows in " + table +" is - ", self.cur.rowcount)
        print("Dantenbak Einträge erfolgt geholt!")
        return records

    def get_dinks_record(self):
        sql_select_Query = "SELECT name, v_prozent, volumen, fach_1, fach_2, fach_3, fach_4 FROM Drinks"
        self.cur.execute(sql_select_Query)
        records = self.cur.fetchall()
        print("Dantenbak Einträge erfolgt geholt!")
        return records

    def get_setting(self, key):
        sql_select_Query = "SELECT value FROM Settings WHERE key = '" + key + "'"
        self.cur.execute(sql_select_Query)
        records = self.cur.fetchall()
        print("Dantenbak Einträge erfolgt geholt!")
        return records

    def get_cocktail_rezept(self, name):
        sql_select_Query = "SELECT recipe_path FROM Cocktails WHERE name = '" + name + "'"
        self.cur.execute(sql_select_Query)
        records = str(self.cur.fetchone())
        print("Dantenbak Einträge erfolgt geholt!")
        return records

    def get_alkoholfrei_rezept(self, name):
        sql_select_Query = "SELECT recipe_path FROM Alkoholfrei WHERE name = '" + name + "'"
        self.cur.execute(sql_select_Query)
        records = str(self.cur.fetchone())
        print("Dantenbak Einträge erfolgt geholt!")
        return records

    def set_setting(self, key, value):
        sql_select_Query = "UPDATE Settings SET value = '" + value + "' WHERE key = '" + key + "'"
        self.cur.execute(sql_select_Query)
        self.conn.commit()
        print("Neue Einstellung geschrieben.")
    
    def add_drinks_fachnumber(self, name, v_prozent, volumen, fach):
        sql_select_Query = "UPDATE Drinks SET fach_" + fach + " = NULL"
        self.cur.execute(sql_select_Query)
        sql_select_Query = "UPDATE Drinks SET fach_" + fach + " = 1 WHERE name = '" + name + "' AND v_prozent = " + v_prozent + " AND volumen = " + volumen
        self.cur.execute(sql_select_Query)
        self.conn.commit()
        print("Neue Fachnummer geschrieben.")
    
    def del_drinks_fachnumber(self, fach):
        sql_select_Query = "UPDATE Drinks SET fach_" + fach + " = NULL"
        self.cur.execute(sql_select_Query)
        self.conn.commit()
        print("Neue Fachnummer geschrieben.")

    def add_Cocktail(self, name, bild_pfad, rezept, rating):
        # Push into DB Table
        dbObj = DatabaseManager()
        dbObj.add_del_update_db_record("insert into Cocktails (name, image_path, recipe_json, rating) values (?,?,?,?)", [name, bild_pfad, rezept, rating])
        del dbObj
        print("Inserted Cocktail Data into Database.")
       
    def __del__(self):
        self.cur.close()
        self.conn.close()