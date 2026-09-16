import duckdb


con = duckdb.connect("cinema_pipeline.duckdb")


with open("sql/credit_role_classification.sql", "r", encoding="utf-8") as file:
    sql = file.read()


con.execute(sql)


print("\nCredit role classification:\n")


results = con.execute("""
    SELECT
        role_category,
        COUNT(*) AS total
    FROM cinema_data.credit_roles
    GROUP BY role_category
    ORDER BY total DESC
""").fetchall()


for row in results:
    print(row)


print("\nSample classified credits:\n")


samples = con.execute("""
    SELECT
        p.name,
        c.role_type,
        c.job,
        cr.role_category
    FROM cinema_data.credit_roles cr
    JOIN cinema_data.people p
        ON cr.person_id = p.person_id
    JOIN cinema_data.credits c
        ON cr.credit_id = c.credit_id
    LIMIT 20
""").fetchall()


for row in samples:
    print(row)


con.close()