import mysql.connector

def get_post_info_from_db(post_id,pattern):
    # DB 연결 설정
    connection = mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )

    cursor = connection.cursor()
    cursor.execute(f"SELECT name, url, soup FROM TEMP_TABLE WHERE id = {post_id}")

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
