import  sqlite3

connnection = sqlite3.connect('data.db')
cursor = connnection.cursor()
create_table = "CREATE TABLE users(id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'vivek', 'vivek')
insert_query = "INSERT INTO users values (?,?,?)"
cursor.execute(insert_query,user)

users = [
    (2, 'vivek1', 'vivek1'),
    (3, 'vivek2', 'vivek2')
]
cursor.executemany(insert_query, users)

select_query = "SELECT *FROM users"
for row in  cursor.execute(select_query):
    print(row)




connnection.commit()
connnection.close()

