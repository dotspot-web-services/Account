from src.setting.dbcon import DbSet


def test_connection() -> None:
    pg = DbSet()
    con = pg.get_db()
    con.execute("select * from users")
    print(con.fetchall())
