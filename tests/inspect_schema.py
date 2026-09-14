import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


result = con.execute("""
    DESCRIBE cinema_data.movies
""").fetchall()


print("\nMovies table schema:\n")

for column in result:
    print(column)


con.close()