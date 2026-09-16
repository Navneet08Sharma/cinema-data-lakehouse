import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


print("\nPeople table:")

people_count = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.people
""").fetchone()[0]

print("Total people:", people_count)


print("\nCredits table:")

credits_count = con.execute("""
    SELECT COUNT(*)
    FROM cinema_data.credits
""").fetchone()[0]

print("Total credits:", credits_count)


print("\nSample people:\n")

people = con.execute("""
    SELECT
        person_id,
        name,
        known_for_department
    FROM cinema_data.people
    ORDER BY person_id
    LIMIT 10
""").fetchall()

for person in people:
    print(person)


print("\nSample credits:\n")

credits = con.execute("""
    SELECT
        credit_id,
        media_id,
        media_type,
        person_id,
        role_type,
        character_name,
        job
    FROM cinema_data.credits
    LIMIT 10
""").fetchall()

for credit in credits:
    print(credit)


con.close()