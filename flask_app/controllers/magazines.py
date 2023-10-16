from flask_app import app
from flask import render_template, session,request,redirect,flash
from flask_app.models  import magazine,user
from flask_bcrypt import Bcrypt



@app.route('/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id": session['user_id']
    }
    
    logged_in_user = user.User.get_user_by_id(data)
    
    magazines_and_users_db = magazine.Magazine.get_magazines_with_users()
    return render_template('dashboard.html', magazines=magazines_and_users_db, user = logged_in_user)


@app.route('/new', methods =['GET', 'POST'])
def create_magazine():
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'GET':
        return render_template('create_magazine.html')
    
    if request.method == 'POST':
        if not magazine.Magazine.validate_magazines_form_inputs(request.form):
            return redirect('/new')
        
        data = {
            "title": request.form['magazineTitle'],
            "description": request.form['magazineDescription'],
            'user_id': session['user_id']
        }
        
        magazine_id = magazine.Magazine.create_magazine(data)
        
        return redirect('/dashboard')
    
@app.route('/show/<int:id>')
def show_magazine(id):
    if 'user_id' not in session:
        return redirect('/')
    
    
    data = {
        "id": id
    }
    magazine_db = magazine.Magazine.get_magazine_and_user_with_id(data) 
    subsribers = magazine.Magazine.get_all_subscribed_users_for_a_magazine(data)
    
    return render_template('show_magazine.html', magazine =magazine_db, subsribers=subsribers)


@app.route('/subscribe/<int:user_id>/<int:magazine_id>')
def subscribe_to_magazine(user_id, magazine_id):
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'magazine_id': magazine_id,
        'user_id': user_id
    }
    subscribed = magazine.Magazine.subscribe_to_magazine(data)
    
    if subscribed:
        flash('Successfully Subscribbed to the magazine!', 'subscribed')
    else:
        flash('You have already subscribed to this magazine.', 'subscribed')
        
    return redirect('/dashboard')

    
@app.route('/delete/<int:id>')
def delete_magazine(id):
    
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    magazine.Magazine.delete_magazine(data)
    
    return redirect('/user/account')

