import sqlite3
from sqlite3 import Error
import random


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_task(conn, i, collection_id, created_by_id):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    arr_type = ["website", "book", "article", "music", "video"]
    type_of_link = arr_type[random.randint(0,4)]

    sql = f''' INSERT INTO link_storage_link (title, description, url_field, url_to_image, type_of_link, date_of_created, date_of_changed, collection_id, created_by_id)
                VALUES ('linkN{i}', 'description', "url_field", "url_to_image", "{type_of_link}", "2024-04-19T18:15:22.", "2024-04-19T18:15:22.265Z", {collection_id}, {created_by_id});'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"db_copy.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create tasks
        for y in range(1, 13):
            for i in range(random.randint(50, 100)):
                create_task(conn, i, collection_id=y, created_by_id=(y + 1))


if __name__ == '__main__':
    main()


sql_for_users = '''INSERT INTO accounts_customuser (password, email, is_superuser, first_name, last_name, is_staff, is_active, date_joined)
              VALUES ('testpassword', 'test13@example.com', False, "first_name", "last_name", False, False, "2024-04-19T18:15:22.265Z");
            '''

sql_for_category = '''INSERT INTO link_storage_collection (title, description, date_of_created, date_of_changed, created_by_id)
                        VALUES ('testcollection5', 'description', "2024-04-19T18:15:22.", "2024-04-19T18:15:22.265Z", 5);'''