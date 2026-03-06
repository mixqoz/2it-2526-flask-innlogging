from dataclasses import dataclass
from auth import hash_password, is_correct_password
import sqlite3

DATABASE = "test.db"





@dataclass
class User:
    username: str
    password: str

    fornavn: str = ""
    etternavn: str = ""

    def __post_init__(self):
        self.password = hash_password(self.password, self.username)
        self.save()

        def save(self):
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO users(
                           username,
                           password,
                           forvanv,
                           etternavn
                        ) VALUES (:username,
                           :password,
                           :fornavn,
                           :etternavn)""", self.__dict__)
            conn.commit()
            conn.close()



    def check_password(self, password: str) -> bool:
        return is_correct_password(password, self.username, self.password)
    
    @property
    def full_navn(self) -> str:
        return f"{self.fornavn} {self.etternavn}"

def get_all():
    data = {}
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():

        # 0 = username, 1 = pass, 2 = fornavn, 3 = etternavn
        data[row[0]] = User(*row)
    conn.close()
    return data


def init_db():
    conn = sqlite3.connect(DATABASE) # Lager en tilkobling til databasen
    cursor = conn.cursor() # Lager en cursor for å utføre SQL-kommandoer


    # Creates a tabele, and if it already exists, it does not create a new one. It crashes if you do not have IF NOT EXISTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        fornavn TEXT,
        etternavn TEXT,
        UNIQUE(username)
    )
    """)
    conn.commit()
    conn.close()


init_db()