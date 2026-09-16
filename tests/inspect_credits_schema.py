import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


print("\nPEOPLE TABLE SCHEMA:\n")

people_schema = con.execute("""
    DESCRIBE cinema_data.people
""").fetchall()

for column in people_schema:
    print(column)


print("\nCREDITS TABLE SCHEMA:\n")

credits_schema = con.execute("""
    DESCRIBE cinema_data.credits
""").fetchall()

for column in credits_schema:
    print(column)


print("\nDUPLICATE CREDIT IDs:\n")

duplicates = con.execute("""
    SELECT
        credit_id,
        COUNT(*) AS occurrences
    FROM cinema_data.credits
    GROUP BY credit_id
    HAVING COUNT(*) > 1
    ORDER BY occurrences DESC
    LIMIT 10
""").fetchall()

if duplicates:
    for row in duplicates:
        print(row)
else:
    print("No duplicate credit IDs found.")


print("\nPEOPLE COUNT:")

people_count = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.people
""").fetchone()[0]

print(people_count)


print("\nCREDITS COUNT:")

credits_count = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.credits
""").fetchone()[0]

print(credits_count)


con.close()