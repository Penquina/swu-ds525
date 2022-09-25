import glob
import json
import os
from typing import List

import psycopg2

table_insert = """
    INSERT INTO users (
        xxx
    ) VALUES (%s)
    ON CONFLICT (xxx) DO NOTHING
"""

def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        print('for datafile in all_files:')
        
        with open(datafile, "r") as f:
            #If not json must change code for get input
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                print(each["id"], each["type"], each["actor"]["login"])
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login
                    ) VALUES ({each["actor"]["id"]}, 
                    '{each["actor"]["login"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                #Importance in "ON CONFLICT (id) DO NOTHING "
                #If insert actor same id code is do nothing 

                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into tables here 
                # 2. from create table in create_tables.py increase feature to have the same in that columns  
                # 3. increase '{each["actor"]["url"]}','{each["created_at"]}' in the command
                insert_statement = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id,
                        actor_url,
                        created_at
                    ) VALUES ('{each["id"]}',
                     '{each["type"]}',
                     '{each["actor"]["id"]}',
                     '{each["actor"]["url"]}',
                     '{each["created_at"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                conn.commit()


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main()