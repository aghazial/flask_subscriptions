from flask_app import app
from flask import render_template, session,request,redirect,flash
from flask_app.models  import user, magazine
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/register/user', methods=['POST'])
def register_new_user():
    if not user.User.validate_registration_form_input(request.form):
        return redirect('/')
    
    
    register_password = request.form['registerPassword']
    
    if register_password != request.form['confirmPassword']:
        flash('Entered passwords are not matching.', 'registration_form')
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['registerPassword'])
    
    data ={
        "first_name": request.form['firstName'],
        "last_name": request.form['lastName'],
        "email": request.form['registerEmail'],
        "password": pw_hash
        }
    
    user_id = user.User.create_user(data)
    session['user_id'] = user_id
    
    return redirect('/dashboard')
  
@app.route('/login', methods=['POST'])
def login_user():
    
    if not user.User.validate_login_form(request.form):
        return redirect('/')
    
    login_email = request.form['loginEmail']
    login_password = request.form['loginPassword']
    
    data = {
        "email": login_email
    }
    
    
    user_in_db = user.User.get_user_by_email(data)
    
    if not user_in_db:
        flash("No user with this email!", 'login_form')
        return redirect('/')
        
    if not bcrypt.check_password_hash(user_in_db['password'], login_password):
        flash('Password did not match with user email.', 'login_form')
        return redirect('/')

    session['user_id'] = user_in_db['id']
    
    return redirect('/dashboard')

@app.route('/user/update', methods=['POST'])
def update_user_account():
    if 'user_id' not in session:
        return redirect('/')
    
    
    if request.method == 'POST':
        if not user.User.validate_update_account_form(request.form):
            return redirect('/user/account')
    
    user_id = session['user_id']
    data = {
        "first_name": request.form['firstName'],
        "last_name": request.form['lastName'],
        "email": request.form['updateEmail'],
        "id": user_id
    }
    user.User.update_user_table_data(data)
    
    return redirect('/user/account')
        
        
@app.route('/user/account')
def show_user_account():
    
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id": session['user_id']
    }
    
    user_with_magazines = user.User.get_magazines_with_user(data)
    if not user_with_magazines:
        flash('No magazines created yet.', 'users_magazine') 

    user_info = user.User.get_user_by_id(data)
    
    return render_template('edit_user_account.html', user_magazines = user_with_magazines, user =user_info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')