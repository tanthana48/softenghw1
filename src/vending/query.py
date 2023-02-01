from app import mysql
from flask import jsonify


def select_query(query_statement: str) -> jsonify(str):
    """Execute query and result in json."""
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            result = cur.fetchall()
            return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e))


def action_query(query_statement: str) -> jsonify(str):
    """Execute query and result in json."""
    try:
        with mysql.connection.cursor() as cur:
            cur.execute(query_statement)
            mysql.connection.commit()
            return jsonify(message="Success")
    except Exception as e:
        return jsonify(error=str(e))
