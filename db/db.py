import os
import mysql.connector


def read_query_from_file(query_file, query_name):
    with open(query_file, 'r') as file:
        content = file.read()

    queries = content.split(";")
    for query in queries:
        if query.strip().startswith(f"[{query_name}]"):
            return query.strip()[len(query_name) + 2:].strip()

    raise ValueError(f"Query '{query_name}' not found in {query_file}")


def get_post_info_from_db(post_id):
    # DB 연결 설정
    connection = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_DATABASE"]
    )

    query = read_query_from_file("queries.sql", "get_post_info")

    cursor = connection.cursor()
    cursor.execute(query, (post_id,))

    row = cursor.fetchone()

    if row:
        post_info = {
            "name": row[0],
            "url": row[1],
            "soup": row[2],
        }
        return post_info
    else:
        return None

    # 연결 종료
    cursor.close()
    connection.close()
