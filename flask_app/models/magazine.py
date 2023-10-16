from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Magazine:
    database = 'subscriptions'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = []
        
        
    @classmethod
    def create_magazine(cls, data):
        query = "INSERT INTO magazines(title,description,created_at,updated_at,user_id) VALUES(%(title)s,%(description)s,NOW(),NOW(),%(user_id)s)"
        
        results = connectToMySQL(cls.database).query_db(query, data)
        
        if not results: 
            return False
        

        return results
    
    @classmethod
    def get_magazines_with_users(cls):
        query = "SELECT * FROM magazines JOIN users on magazines.user_id = users.id;"
        
        results = connectToMySQL(cls.database).query_db(query)
        all_magazines = []
        
    
        if results:
            for row in results:
                magazine_instance = cls(row)
                
                data = {
                    "id": row['user_id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                    }
                
                creator_instance = User(data)
                
                magazine_instance.creator = creator_instance
                
                all_magazines.append(magazine_instance) 
            
        return all_magazines
    
    
    @classmethod
    def get_magazine_and_user_with_id(cls, data):
        query = """
                    SELECT m.id,m.title, m.description, u.first_name, u.last_name
                    FROM magazines m
                    JOIN users u ON m.user_id = u.id
                    WHERE m.id = %(id)s;
                """   
        
        results = connectToMySQL(cls.database).query_db(query,data)
        
        if not results:
            return False
        
        
        return results[0]
    
    @classmethod
    def subscribe_to_magazine(cls, data):
        
        get_subscription_query = "SELECT id FROM subscriptions WHERE magazine_id = %(magazine_id)s AND user_id = %(user_id)s"
        
        subscriptions = connectToMySQL(cls.database).query_db(get_subscription_query,data)
        
        

        if not subscriptions:
            create_subscription = "INSERT INTO subscriptions(user_id, magazine_id, created_at) VALUES(%(user_id)s,%(magazine_id)s, NOW())"
            results = connectToMySQL(cls.database).query_db(create_subscription,data)
            return results 
        else:
            return False
    
    @classmethod
    def get_all_subscribed_users_for_a_magazine(cls,data):
        query = """
                SELECT users.first_name, users.last_name
                FROM users
                JOIN subscriptions ON users.id = subscriptions.user_id
                WHERE subscriptions.magazine_id = %(id)s;
                """
            
        results = connectToMySQL(cls.database).query_db(query,data)
        return results
    @classmethod
    def delete_magazine(cls,data):
        
        query = "DELETE FROM magazines WHERE id = %(id)s"
        return connectToMySQL(cls.database).query_db(query, data)

    @staticmethod
    def validate_magazines_form_inputs(magazine_form):
        is_valid = True

        if not magazine_form['magazineTitle'] or not magazine_form['magazineDescription']:
            flash('All fields are required.', 'magazine_form')
            is_valid = False
        
        if len(magazine_form['magazineTitle']) < 2:
            flash('Magazine title must be at least 2 characters long', 'magazine_form')
            is_valid = False
            
        if len(magazine_form['magazineDescription']) < 2:
            flash('Magazine description must be at least 2 characters long', 'magazine_form')
            is_valid = False
            
        return is_valid
    
    