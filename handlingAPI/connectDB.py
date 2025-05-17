import pymysql

# connect to database
db = pymysql.connect(
    host="localhost",
    user="ashika",
    password="ashi",
    database="customers"
)

# it creates a cursor object
cursor = db.cursor()

cursor.execute("SELECT * FROM customer") # run sql query to execute the data

result = cursor.fetchall() # get all results

print("Customer Data:")
for i in result:
    print(i) # print each row

cursor.execute("SELECT DATABASE();")
dbs = cursor.fetchall()

print("\n")
print("Databases Name:")
print(dbs)

cursor.close()
db.close()

