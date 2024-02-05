def new_user_template(userid, password):
    """
    Email template for new user.
    Args:
    userid (str): User ID.
    Returns:
    str: Email template.
    """
    return f"""
    <html>
    <body>
    <h2>Welcome to our company!</h2>
    <p>Your user ID is: {userid}</p>
    <p>Your temporary password is: {password}</p>
    <p>Thank you for joining our platform.</p>
    </body>
    </html>
    """