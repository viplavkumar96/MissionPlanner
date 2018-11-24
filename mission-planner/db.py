import mysql.connector

import psycopg2

from flask_bcrypt import generate_password_hash, check_password_hash
def connectDB(host='localhost',database='codejam',user='root',password='1234'):
    return mysql.connector.connect(host=host,database=database,user=user,password=password)

def disconnectDB(conn):
    conn.close()

def executeDB(conn,sql,values):
    cursor = conn.cursor()
    cursor.execute(sql,values)
    conn.commit()
    return cursor.lastrowid

def queryDB(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    try:
        rows = cursor.fetchall() # fetchone() , fetchmany() , fetchall()
    except:
        rows=[]
    cursor.close()
    return rows


# User Functions

def user_register(username,password,email):
    c = connectDB()
    password = generate_password_hash(password)
    executeDB(c,"insert into members values(0,%s,%s,%s)",(username,password,email))
    disconnectDB(c)
    return True

def user_update(username,email,bio,dob,ieee_no,branch,sem):
    c = connectDB()
    executeDB(c,"update members set \
                username=%s, \
                email=%s, \
                where email=%s",(username,email))
    disconnectDB(c)
    return True

def user_unregister(user_id):
    c = connectDB()
    executeDB(c,"delete from members where user_id="+str(user_id),())
    disconnectDB(c)
    return True

def user_login(email,password):
    c = connectDB()
    result = queryDB(c,"select * from members where email='"+email+"'")

    disconnectDB(c)
    if check_password_hash(result[0][2], password):
        return result[0]
    else:
        return False

def mission_creation(streetloc,typeofmission,indoor_outdoor,minmaj,user_id,latitude,longitude):
    c = connectDB()
    executeDB(c,"insert into mission (streetloc,typeofmission,indoor_outdoor,minmaj,user_id,longitude,latitude) values(%s,%s,%s,%s,%s,%s,%s)",(streetloc,typeofmission,indoor_outdoor,minmaj,user_id,longitude,latitude))
    disconnectDB(c)
    return True

def drones_query(typeofmission,minmaj):
    c = connectDB()
    result = None
    if typeofmission=="Fire" and minmaj =="Minor":
        result = queryDB(c,"select * from drones where sensor_smoke = 'Yes' and sensor_temp = 'Yes' and battery_life>=30")
    elif typeofmission=="Fire" and minmaj=="Major":
        result = queryDB(c,"select * from drones where sensor_smoke = 'Yes' and sensor_temp = 'Yes' and battery_life>=60")
    elif typeofmission=="Flood" and minmaj=="Minor":
        result = queryDB(c,"select * from drones where sensor_video = 'Yes' and battery_life>=30")
    elif typeofmission=="Flood" and minmaj=="Major":
        result = queryDB(c,"select * from drones where sensor_video = 'Yes' and battery_life>=60")
    disconnectDB(c)
    if result is not None:
        count = 0
        for i in result:
            count +=1
        return count
    else:
        return False





def init_DB():
    c = connectDB()
    sql ='''
    CREATE TABLE if not exists members  (
       user_id   serial primary key,
       username  text NOT NULL,
       password  text NOT NULL,
       email  text NOT NULL
      )
    '''
    executeDB(c,sql,())

    sql ='''
    CREATE TABLE if not exists mission  (
       mission_id   serial primary key,
       streetloc  text NOT NULL,
       typeofmission text NOT NULL,
       indoor_outdoor text NOT NULL,
       minmaj text NOT NULL
       user_id foreign key,
       latitude decimal(20),
       longitude decimal(20)
      )
    '''
    executeDB(c,sql,())

    sql ='''
    CREATE TABLE if not exists drones  (
       drone_id   serial primary key,
       sensor_temp  text NOT NULL,
       sensor_smoke  text NOT NULL,
       sensor_video  text NOT NULL,
       payload text NOT NULL,
       battery_life int NOT NULL
      )
    '''
    executeDB(c,sql,())

    disconnectDB(c)

#init_DB()



# Tables
# members
#     id	 int Auto Increment
#     username	text
#     password	text
#     email	text


#USAGE
# c = connectDB()
# executeDB(c,"insert into memebers values(a,b,c)")
# disconnectDB(c)


# c = connectDB()
# result = queryDB(c,"select * from memebers")
# disconnectDB(c)
