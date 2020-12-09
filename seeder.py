from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///journal.db", echo=True, future=True)

# create new table 'registrants' with username 1 and password 1
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS registrants"))
    conn.execute(text("CREATE TABLE 'registrants' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' VARCHAR(255),'hash' TEXT)"))
    conn.commit()
    password = generate_password_hash('1')
    conn.execute(text("INSERT INTO registrants (username, hash) VALUES ('1', :hash)"),
                    [{"hash": password}])
    conn.commit()

    conn.execute(text("DROP TABLE IF EXISTS entries"))
    conn.execute(text("CREATE TABLE 'entries' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
        + " 'username' TEXT NOT NULL,"
        + " 'entry' TEXT,"
        + " 'mood' TEXT,"
        + " 'date' DATE)"))
    conn.commit()