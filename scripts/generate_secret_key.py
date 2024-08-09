'''
Generates a secure `SECRET_KEY`. Initially used to create values for env variables in each environment.

Usage:
    python generate_secret_key.py
'''

import secrets

def generate_secret_key():
    return secrets.token_hex(32)

if __name__ == "__main__":
    print("SECRET_KEY:", generate_secret_key())
