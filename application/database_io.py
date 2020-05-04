from application.db_utils import pool
import os


def getValueTreatments(item, tariff):
    sql = """SELECT value FROM treatments WHERE item = {} AND tariff = '{}'""".format(item, tariff)
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    filtered_result = cursor.fetchone()
    cursor.close()
    conn.close()
    return filtered_result

def getTreatments(tariff, featured=None):
    if (featured is None):
        sql = """SELECT LPAD(item, 3, 0) AS item, description, category FROM treatments WHERE tariff = '{}' ORDER BY id""".format(tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        filtered_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return filtered_result

    elif(featured is not None):
        featured = tuple(featured)
        sql = """SELECT LPAD(item, 3, 0) AS item, description FROM treatments WHERE item IN {} AND tariff = '{}' ORDER BY id""".format(featured, tariff)
        connection = pool.connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        featured_result = cursor.fetchall()
        cursor.close()
        connection.close()
        return featured_result


def getTreatmentByGroup(items, tariff):
    treatment_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in items.split(","):
        sql = """SELECT description FROM treatments WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        treatment_list.append(q)
    return treatment_list



def getTreatmentByItem(treatments, tariff):
    treatment_list=[]
    connection = pool.connection()
    cursor = connection.cursor()
    for i in treatments:
        sql = """SELECT description, units, value FROM treatments WHERE item = {} AND tariff = '{}'""".format(i, tariff)
        cursor.execute(sql)
        q = cursor.fetchone()
        treatment_list.append(q)
    cursor.close()
    connection.close()
    return treatment_list
