from django.db import connection

def find_similar_destination(liked_destination):
    # Retrieve the details of the liked destination
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM DESTINATIONS WHERE DEST LIKE %s", [liked_destination])
        row = cursor.fetchone()
        liked = row[2:8]

    # Find the destination with the minimum distance from the liked destination
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM DESTINATIONS WHERE DEST NOT LIKE %s", [liked_destination])
        mini = None
        for row in cursor.fetchall():
            x = row[2:8]
            A = sum([abs(x[i]-liked[i]) for i in range(6)])
            if mini == None or A < mini:
                mini = A
                place = row[1]

    return (mini, place)