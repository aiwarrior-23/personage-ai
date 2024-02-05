import random
import string

def password_generator(length=8):
    """
    Generate a random password.

    Args:
    length (int): Length of the password.

    Returns:
    str: Random password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password
