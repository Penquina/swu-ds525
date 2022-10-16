import psycopg2


drop_table_queries = [
    "DROP TABLE IF EXISTS events",
]
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS events (
        id text,
        type text,
        actor text,
        repo text,
        created_at text
    )
    """,
]
# Get data from S3 into redshift
copy_table_queries = [
    """
    COPY events FROM 's3://kik-project3/github_events_01.json'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::074831285365:role/LabRole'
    JSON 's3://kik-project3/events_json_path.json'
    REGION 'us-east-1'
    """,
]


insert_table_queries = [
    """
    INSERT INTO
      events (
        id
      )
    SELECT
      DISTINCT id,
    FROM
      staging_events
    WHERE
      id NOT IN (SELECT DISTINCT id FROM events)
    """,
]

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

#Set connection to redshift
def main():
    host = "redshift-cluster-1.cbdkb6riwsow.us-east-1.redshift.amazonaws.com"
    dbname = "dev"
    user = "awsuser"
    password = "Wai>chi1"
    port = "5439"
    conn_str = f"host={host} dbname={dbname} user={user} password={password} port={port}"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    # drop_tables(cur, conn)
    # create_tables(cur, conn)
    # load_tables(cur, conn)
    # insert_tables(cur, conn)

    query = "select * from events"
    cur.execute(query)

    records = cur.fetchall()
    for row in records:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()