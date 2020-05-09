import psycopg2

connection = psycopg2.connect(database="test", user="postgres", password=1234, host="127.0.0.1", port="5432")

cursor = connection.cursor()

cursor.execute('''
Create Table table2
(
id integer primary key, 
completed boolean not null default false
);
''')

cursor.execute('''
insert into table2 (id,completed) values(1,true);
''')

connection.commit()

connection.close()
cursor.close()