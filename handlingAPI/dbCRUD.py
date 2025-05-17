import pymysql

db = pymysql.connect(
    host="localhost",
    user="ashika",
    password="ashi",
    database="customers"
)

cursor = db.cursor()

# create pr add customer data
def create_user():
    query = "INSERT INTO customer(name, contact_number, address, city, price) VALUES (%s,%s, %s, %s, %s)"
    values = ("Vijay", 8899778789, "Krishna vihar colony", "Ratlam", 45.90)
    cursor.execute(query, values)
    db.commit()
    print("Customer Inserted!")

# read user data
def get_user():
    cursor.execute("SELECT * FROM customer")
    res = cursor.fetchall()

    print("Customer Data:-")
    for i in res:
        print(i)

# update user data
def update_user():
    query = "UPDATE customer SET address = %s WHERE name = %s"
    values = ("Bhopal", "Ram")
    cursor.execute(query, values)
    db.commit()
    print("Customer Updated!")

# delete user data
def del_user():
    query = "DELETE FROM customer WHERE name = %s"
    values = ("Vijay")
    cursor.execute(query, values)
    db.commit()
    print("Customer Deleted!")

create_user()
#get_user()
#update_user()
#del_user()
get_user()

cursor.close()
db.close()