from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    DB = "users_schema"

    def __init__(self, first_name, last_name, email, password, id=None, created_at=None, updated_at=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    def register(self):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        data = {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'password': self.password}
        self.id = connectToMySQL('users_schema').query_db(query, data)
        return self

    @staticmethod
    def is_valid_email(email):
        """
        Validates if an email is in the proper format.
        Returns True if the email is valid, False otherwise.
        """
        # Regular expression to match email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True
        else:
            return False

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        if not user['first_name'].isalpha():
            flash("First Name must contain letters only")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters")
            is_valid = False
        if not user['last_name'].isalpha():
            flash("Last Name must contain letters only")
            is_valid = False
        if not User.is_valid_email(user['email']):
            flash("Invalid email format")
            is_valid = False
        elif User.get_by_email(user['email']):
            flash("Email already registered")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if 'confirm_password' not in user or user['password'] != user['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL(User.DB).query_db(query, data)
        if len(result) > 0:
            return User(**result[0])
        else:
            return None
