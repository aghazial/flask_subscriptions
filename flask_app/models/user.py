from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
#https://docs.python.org/3/library/datetime.html
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*\d).{8,}') #https://docs.python.org/3/library/re.html
class User:
    database = 'subscriptions'
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = ['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.all_magazines = []
        
    # @classmethod
    # def read_all_users(cls):
    #     query = "SELECT * FROM users" 
    #     results = connectToMySQL(cls.database).query_db(query)
    #     users = [];
        
    #     for user in results:
    #         users.append(user)
        
    #     return users
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(), NOW());"
        return connectToMySQL(cls.database).query_db(query, data)
        
    @classmethod
    def update_user_table_data(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s,email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query, data)
    @classmethod
    def delete_user(cls,user_id):
        query = "DELETE FROM users WHERE id = %(id)s"
        data = {"id": user_id}
        return connectToMySQL(cls.database).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        if not results:
            return False
        
        return results[0]
    @classmethod
    def check_if_email_exists(cls,data):
        query = "SELECT count(email) as emails FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results[0]
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.database).query_db(query, data)
        return results[0]
    
    # @classmethod
    # def get_user_with_magazines(cls, data):
    #     query = "SELECT users.id as user_id, users.first_name, users.last_name, users.email, magazines.id as magazine_id, magazines.title, magazines.description FROM users LEFT JOIN magazines ON users.id = magazines.user_id WHERE users.id = %(id)s;"
    #     results = connectToMySQL(cls.database).query_db(query, data)
        
    #     return results
    
    @classmethod
    def get_magazines_with_user(cls, data):
        query = """
                SELECT m.title, m.user_id, m.id as magazine_id,COUNT(s.id) as subscriber_count
                FROM magazines m
                LEFT JOIN subscriptions s on m.id = s.magazine_id
                WHERE m.user_id = %(id)s
                GROUP BY m.id, m.title;
                """
                
        results = connectToMySQL(cls.database).query_db(query, data)
        return results
 

    @staticmethod
    def validate_registration_form_input(registration_form):
        is_valid = True;
        data = {
            "email": registration_form['registerEmail']
        }    
        
        email_count = User.check_if_email_exists(data)
        
        if not registration_form['firstName'] or not registration_form['lastName'] or  not registration_form['registerEmail'] or not registration_form['registerPassword']:
            flash('All Fields are Required.', 'registration_form')
            is_valid=False
        if len(registration_form['firstName']) <3:
            flash('First Name must be 3 or more characters.', 'registration_form')
            is_valid = False
        if len(registration_form['lastName']) < 3:
            flash('Last Name must be 3 or more characters.', 'registration_form')
            is_valid = False
        if not EMAIL_REGEX.match(registration_form['registerEmail']):
            flash('Invalid Email Address.', 'registration_form')
            is_valid=False
        if not PASSWORD_REGEX.match(registration_form['registerPassword']):
            flash('Password did not meet the criteria.', 'registration_form')
            flash('Password must be 8 or more characters long, requires at least 1 number and 1 upper case letter.', 'registration_form')
            is_valid=False
        if int(email_count['emails']) > 0:
            flash('Email is already used.', 'registration_form')
            is_valid = False  
        return is_valid
    
    @staticmethod
    def validate_login_form(login_form):
        is_valid=True
        
        if not login_form['loginEmail'] or not login_form['loginPassword']:
            flash('All Fields are required.', 'login_form')
            is_valid = False
            
        if not EMAIL_REGEX.match(login_form['loginEmail']):
            flash('Invalid Email.', 'login_form')
            is_valid = False
        
        return is_valid
    
    @staticmethod 
    def validate_update_account_form(update_form):
        is_valid=True
        
        if not update_form['firstName'] or not update_form['lastName'] or not update_form['updateEmail']:
            flash('All Fields are required.', 'update_form')
            is_valid = False
            
        if len(update_form['firstName']) <3:
            flash('First Name must be 3 or more characters.', 'update_form')
            is_valid = False
        if len(update_form['lastName']) < 3:
            flash('Last Name must be 3 or more characters.', 'update_form')
            is_valid = False
            
        if not EMAIL_REGEX.match(update_form['updateEmail']):
            flash('Invalid Email.', 'update_form')
            is_valid = False
            
            
        return is_valid