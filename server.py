# Bu projenin ikinci kısmı olan veritabanına yazma kısmı için
# veritabanı connectionlarını hazırladım ve insert testi yaptım.
# Birinci kısım(client.py) da post hedefime ulaşamadığım için 
# bu kısım dinamik olamadı.

import psycopg2

try:
    connection = psycopg2.connect(user="postgres",
                                  password="P*b*p575",
                                  host="localhost",
                                  port="5432",
                                  database="userapi")
    cursor = connection.cursor()

    # CODE: Buraya client.py'dan post edilen data gelecek.
    postgres_insert_query = """ INSERT INTO users (first_name,last_name,address,birthday,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = ('Hünkar', 'Genç Yıldız ', '56' , '14-09-1992', 15, 15)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into users table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into users table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")