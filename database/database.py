import sys

import pymysql.cursors

from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD


def connect():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except:
        sys.exit()


def get_records(d_from, d_to, direction, limit, offset):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE calldate >=%s AND calldate<=%s AND dcontext=%s AND disposition='ANSWERED' LIMIT %s OFFSET %s;"
        cursor.execute(sql, (d_from, d_to, direction, limit, offset))
        result = cursor.fetchall()
        return result


def get_total_records(d_from, d_to, direction):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE calldate >=%s AND calldate<=%s AND dcontext=%s AND disposition='ANSWERED';"
        cursor.execute(sql, (d_from, d_to, direction))
        result = cursor.fetchall()
        return result


def get_get_file_from_unique_id(uniqueid):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE uniqueid like %s;"
        cursor.execute(sql, uniqueid)
        result = cursor.fetchone()
        return result


def get_records_phone_in(phone, direction, limit, offset):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE src=%s AND dcontext=%s AND disposition='ANSWERED' LIMIT %s OFFSET %s;"
        cursor.execute(sql, (phone, direction, limit, offset))
        result = cursor.fetchall()
        return result


def get_records_phone_out(phone, direction, limit, offset):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE dst=%s AND dcontext=%s AND disposition='ANSWERED' LIMIT %s OFFSET %s;"
        cursor.execute(sql, (phone, direction, limit, offset))
        result = cursor.fetchall()
        return result


def get_total_records_phone_in(phone, direction):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE src=%s AND dcontext=%s AND disposition='ANSWERED';"
        cursor.execute(sql, (phone, direction))
        result = cursor.fetchall()
        return result


def get_total_records_phone_out(phone, direction):
    connection = connect()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM cdr WHERE dst=%s AND dcontext=%s AND disposition='ANSWERED';"
        cursor.execute(sql, (phone, direction))
        result = cursor.fetchall()
        return result

def get_missed_calls(phone):
    connection=connect()
    with connection.cursor() as cursor:
        sql = " SELECT calldate, src, dst  FROM cdr  WHERE disposition = 'NO ANSWER'  AND dcontext = 'from-internal'  AND LENGTH(dst) > 0;"
        cursor.execute(sql, (phone))
        result =  cursor.fetchall()
        return result
