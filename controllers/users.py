from logger import get_logger

def get_all_users(cursor, jsonify):
    """
    Get all users from the database.

    Returns:
    list: List of users.
    """
    logger = get_logger("my_logger")
    try:
        cursor.execute("SELECT * FROM company_table")
        columns = [col[0] for col in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify({'message': "users fetched successfully","status":"success","data":users}), 200
    except Exception as e:
        logger.error(str(e))
        return jsonify({'message': "could not fetch users","status":"failure"}), 500
    finally:
        cursor.close()