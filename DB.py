import mysql.connector

class Database:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="4728",
            database="expenses"
        )
        self.cursor = self.con.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS expense (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), amount FLOAT, date DATE, description TEXT)"
        )
        self.con.commit()

    def insert(self, category, amount, date, description):
        sql = "INSERT INTO expense (category, amount, date, description) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (category, amount, date, description))
        self.con.commit()

    def fetch(self):
        self.cursor.execute("SELECT * FROM expense")
        rows = self.cursor.fetchall()
        return rows

    def update(self, id, category, amount, date, description):
        sql = "UPDATE expense SET category=%s, amount=%s, date=%s, description=%s WHERE id=%s"
        self.cursor.execute(sql, (category, amount, date, description, id))
        self.con.commit()

    def remove(self, id):
        sql = "DELETE FROM expense WHERE id=%s"
        self.cursor.execute(sql, (id,))
        self.con.commit()

    def get_total_amount(self):
        self.cursor.execute("SELECT SUM(amount) FROM expense")
        total = self.cursor.fetchone()[0]
        return total if total else 0

    def get_category_amount(self, category):
        sql = "SELECT SUM(amount) FROM expense WHERE category=%s"
        self.cursor.execute(sql, (category,))
        total = self.cursor.fetchone()[0]
        return total if total else 0

if __name__ == "__main__":
    db = Database()
