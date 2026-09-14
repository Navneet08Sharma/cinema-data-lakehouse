import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


result = con.execute("""
    DESCRIBE cinema_data.tv_shows
""").fetchall()


print("\nTV shows table schema:\n")

for column in result:
    print(column)


con.close()