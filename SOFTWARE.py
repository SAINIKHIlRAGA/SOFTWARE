from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = 'some secret key'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='SOFTWARE'
app.config['MYSQL_DB']='first'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('HOME.html')


@app.route('/ABOUT_US')
def aboutus():
    return render_template('ABOUT_US.html')


@app.route('/HOME')
def home():
    return render_template('HOME.html')


# ----------------------------------------------------SIGNUP FORM-------------------------------------------------------


class SignupForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=4, max=20)])
    user_id = IntegerField('User id', [validators.DataRequired(), validators.Length(min=5, max=5)])
    user_type = SelectField('Type', choices=[('customer', 'Customer'), ('restaurant_manager', 'Restaurant Manager')])
    contact_no = IntegerField('Contact Number', [validators.Length(min=10, max=10)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Password do not match')])
    confirm = PasswordField('Confirm Password')


# ---------------------------------------------------UPDATE FORM--------------------------------------------------------


class UpdateForm(Form):
    name = StringField('name')
    user_id = IntegerField('User id')
    user_type = SelectField('Type', choices=[('customer', 'Customer'), ('restaurant_manager', 'Restaurant Manager')])
    contact_no = IntegerField('Contact Number')


# ---------------------------------------------------REPORTS FORM-------------------------------------------------------


class ReportForm(Form):
    customer_id = IntegerField('customer_id')
    restaurant_name = StringField('restaurant_name')
    restaurant_id = IntegerField('restaurant_id')
    manager_id = IntegerField('manager_id')
    review = StringField('Your opinion about Restaurant')
    rating = IntegerField('rating')


# -------------------------------------------------------DIET FORM------------------------------------------------------


class DietForm(Form):
    text = StringField('text')


# -----------------------------------------------RESTAURANT DETAILS FORM------------------------------------------------


class RestaurantDetailsForm(Form):
    restaurant_id = IntegerField('Restaurant ID', [validators.DataRequired()])
    restaurant_name = StringField('Restaurant Name', [validators.DataRequired()])
    location = StringField('Location', [validators.DataRequired()])
    contact_no = IntegerField('Contact Number', [validators.DataRequired()])
    item_1 = StringField('item_1')
    price_1 = IntegerField('price_1')
    item_2 = StringField('item_2')
    price_2 = IntegerField('price_2')
    item_3 = StringField('item_3')
    price_3 = IntegerField('price_3')
    item_4 = StringField('item_4')
    price_4 = IntegerField('price_4')
    item_5 = StringField('item_5')
    price_5 = IntegerField('price_5')
    item_6 = StringField('item_6')
    price_6 = IntegerField('price_6')
    item_7 = StringField('item_7')
    price_7 = IntegerField('price_7')
    item_8 = StringField('item_8')
    price_8 = IntegerField('price_8')
    item_9 = StringField('item_9')
    price_9 = IntegerField('price_9')
    item_10 = StringField('item_10')
    price_10 = IntegerField('price_10')


# --------------------------------------INSERTING SIGNUP DETAILS INTO DATABASE------------------------------------------


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        user_id = request.form['user_id']
        user_type = request.form['user_type']
        contact_no = request.form['contact_no']
        password = request.form['password']
        confirm = request.form['confirm']
        error = None
        cursor = mysql.connection.cursor()
        if not name:
            error = 'Name is required.'
        elif not user_id:
            error = 'User ID is required.'
        elif not user_type:
            error = 'User type is required.'
        elif not contact_no:
            error = 'Contact Number is required.'
        elif not password:
            error = 'Password is required.'
        elif not password == confirm:
            error = 'Password Confirmation failed.'
        elif cursor.execute('Select user_id from users where user_id = %s', [user_id]).fetchone is not None:
            error = 'User already registered.'
        if error is None:
            cursor.execute("INSERT INTO users(name, user_id, user_type, contact_no, password)VALUES(%s, %s, %s, %s, %s)",(name, user_id, user_type, contact_no, password))
            mysql.connection.commit()
            cursor.close()
            flash('Registered Successfully!!   Thank you for Registering', 'success')
            return redirect(url_for('login'))
        flash(error)
    return render_template('SIGNUP.html', form=form)


# --------------------------------------INSERTING RESTAURANT DETAILS INTO DATABASE--------------------------------------


@app.route('/restaurant_details/<string:id>', methods=['GET', 'POST'])
def restaurant_details():
    manager_id = id
    form = RestaurantDetailsForm(request.form)
    if request.method == 'POST' and form.validate():
        restaurant_id = form.restaurant_id.data
        restaurant_name = form.restaurant_name.data
        location = form.location.data
        contact_no = form.contact_no.data
        item_1 = form.item_1.data
        item_2 = form.item_2.data
        item_3 = form.item_3.data
        item_4 = form.item_4.data
        item_5 = form.item_5.data
        item_6 = form.item_6.data
        item_7 = form.item_7.data
        item_8 = form.item_8.data
        item_9 = form.item_9.data
        item_10 = form.item_10.data
        price_1 = form.price_1.data
        price_2 = form.price_2.data
        price_3 = form.price_3.data
        price_4 = form.price_4.data
        price_5 = form.price_5.data
        price_6 = form.price_6.data
        price_7 = form.price_7.data
        price_8 = form.price_8.data
        price_9 = form.price_9.data
        price_10 = form.price_10.data
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO restaurant(restaurant_id, restaurant_name, contact_no, location, manager_id)VALUES(%s, %s, %s, %s, %s)",
            (restaurant_id, restaurant_name, location, contact_no, manager_id))
        cursor.execute(
            "INSERT INTO item_details(restaurant_id, item_1, price_1, item_2, price_2, item_3, price_3, item_4, price_4, item_5, price_5, item_6, price_6, item_7, price_7, item_8, price_8, item_9, price_9, item_10, price_10)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (restaurant_id, item_1, price_1, item_2, price_2, item_3, price_3, item_4, price_4, item_5, price_5, item_6,
             price_6, item_7, price_7, item_8, price_8, item_9, price_9, item_10, price_10))
        mysql.connection.commit()
        cursor.close()
        flash('Details Successfully Saved!!', 'success')
        redirect(url_for('user_dashboard'))

    cursor = mysql.connection.cursor()
    cursor.execute('select * from restaurant where manager_id = %s',[manager_id])
    res_det = cursor.fetchone()
    res_id = res_det['restaurant_id']
    cursor.execute('select * from item_details where restaurant_id = %s', [res_id])
    items = cursor.fetchone()
    cursor.close()
    return render_template('RESTAURANT_DETAILS.html', form=form, res_det=res_det, items=items)


# ------------------------------------------UPDATING USER DETAILS-------------------------------------------------------

@app.route('/edit_profile2/<user_id>', methods=["GET", "POST"])
def edit_profile2(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from users WHERE user_id = %s", [user_id])
    user = cursor.fetchone()
    cursor.close()
    form = UpdateForm(request.form)
    form.user_id.data = user['user_id']
    form.name.data = user['name']
    form.contact_no.data = user['contact_no']
    form.user_type.data = user['user_type']

    if request.method == "POST" and form.validate():
        user_id = request.form['user_id']
        name = request.form['name']
        contact_no = request.form['contact_no']
        user_type = request.form['user_type']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET user_id = %s, name = %s, contact_no = %s, user_type = %s WHERE user_id = %s", (user_id, name, contact_no, user_type, user_id))
        mysql.connection.commit()
        cursor.close()
        flash('User Details Updated', 'success')
        return redirect(url_for('user_dashboard'))
    return render_template('USER_UPDATE.html', form=form)


# ----------------------------------------------ADD USER'S PROFILE BY ADMIN---------------------------------------------


@app.route('/adduser', methods=["GET", "POST"])
def adduser():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        user_id = request.form['user_id']
        user_type = request.form['user_type']
        contact_no = request.form['contact_no']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name, user_id, user_type, contact_no, password)VALUES(%s, %s, %s, %s, %s)",(name, user_id, user_type, contact_no, password))
        mysql.connection.commit()
        cursor.close()
        flash('User added Successfully!!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('ADD_USER.html', form=form)


# ---------------------------------------------EDIT USER'S PROFILE BY ADMIN---------------------------------------------


@app.route('/edit_profile/<string:id>', methods=["GET", "POST"])
def edit_profile(id):
    form = UpdateForm(request.form)
    cursor = mysql.connection.cursor()
    cursor.execute('select * from users where id= %s', [user_id])
    user = cursor.fetchone()
    cursor.close()
    form.user_id.data = user['user_id']
    form.name.data = user['name']
    form.user_type.data = user['user_type']
    form.contact_no.data = user['contact_no']
    if request.method == "POST" and form.validate():
        user_id = request.form['user_id']
        name = request.form['name']
        user_type = request.form['user_type']
        contact_no = request.form['contact_no']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET user_id = %s, name = %s, user_type = %s, contact_no = %s where user_id =%s',(user_id, name, user_type, contact_no, user_id))
        mysql.connection.commit()
        cursor.close()
        flash('User Details successfully updated.')
    return render_template('USER_UPDATE.html', form=form)


# -------------------------------------------------USER LOGIN PAGE------------------------------------------------------


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST" and form.validate():
        user_id = request.form['user_id']
        password_check = request.form['password']
        cursor = mysql.connection.cursor()
        type = cursor.execute('select user_type from users where user_id = %s', [user_id])
        cursor = mysql.connection.cursor()
        user = cursor.execute("Select * from users WHERE user_id = %s", [user_id])
        if user>0:
            data = cursor.fetchone
            password = data['password']
            if password_check == password:
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['user_id'] = user_id
                if user_id == '11111':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return render_template('INDEX.html', type=type)
            else:
                app.logger.info('PASSWORD NOT MATCHED')
                flash('User ID and Password does not match!! Try Again', 'danger')
                return render_template('LOGIN.html')
            cursor.close()
        else:
            flash('No User Exists With That User Id!!\n Try With Valid User ID ', 'danger')
            app.logger.info('NO USER')
    return render_template('LOGIN.html')


# ------------------------------------------------LOGIN DECORATOR-------------------------------------------------------


def is_logged_in(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'logged_in' in session:
            return view(*args, **kwargs)
        else:
            flash("NOT Authorized!!", 'danger')
            return render_template('LOGIN.html')
    return wrapped_view


# ----------------------------------------------------LOGOUT------------------------------------------------------------


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged Out Successfully')
    return redirect(url_for('login'))


# -------------------------------------------------ADMIN DASHBOARD------------------------------------------------------


@app.route('/admin_dashboard')
@is_logged_in
def admin_dashboard():
    cursor = mysql.connection.cursor()
    count = cursor.execute("select count(user_id) from users")
    cursor.execute("select * from users")
    users = cursor.fetchall()
    cursor.execute("select * from diet")
    diet = cursor.fetchall()
    cursor.close()
    return render_template('/ADMIN_DASHBOARD.html', count=count, users=users, diet=diet)


# -------------------------------------------------ADMIN VIEWING REPORTS------------------------------------------------


@app.route('/admin_reports')
@is_logged_in
def admin_reports():
    cursor = mysql.connection.cursor()
    cursor.execute('select count(id) from reports')
    count = cursor.fetchone()
    cursor.execute('Select * from reports')
    reports = cursor.fetchall()
    cursor.close()
    return render_template('VIEW_REPORTS.html', count=count, reports=reports)


# ---------------------------------------------DELETION OF REPORTS------------------------------------------------------


@app.route('/delete_reports_admin/<string:id>', methods=["POST"])
def delete_reports_admin(id):
    cursor = mysql.connection.cursor()
    cursor.execute('delete from reports where id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash('Report successfully deleted')
    return redirect(url_for('admin_reports'))


# ----------------------------------------ADMIN & CUSTOMER VIEWING RESTAURANT DETAILS-----------------------------------


@app.route('/view_restaurant_details', methods=['GET', 'POST'])
def view_restaurant_details():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from restaurant')
    detail = cursor.fetchall()
    cursor.close()
    return render_template('VIEW_RESTAURANT_DETAILS.html', detail=detail)


#---------------------------------------------------VIEW ITEM DETAILS---------------------------------------------------


@app.route('/view_item_details/<string:id>')
def view_item_details(id):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from item_details where restaurant_id = %s', [id])
    details = cursor.fetchone()
    cursor.close()
    return render_template('VIEW_ITEM_DETAILS.html', details=details)


# ---------------------------------------------EDITING RESTAURANT DETAILS-----------------------------------------------


@app.route('/edit_restaurant_details/<string:id>', methods=['GET', 'POST'])
def edit_restaurant_details(id):
    form = RestaurantDetailsForm(request.form)
    cursor = mysql.connection.cursor()
    rest_id = cursor.execute('select restaurant_id from restaurant where manager_id = %s', [id])
    cursor.execute('select * from restaurant where manager_id = %s', [id])
    details = cursor.fetchall()
    cursor.close()
    form.restaurant_id.data = restaurant_details['restaurant_id']
    form.restaurant_name.data = restaurant_details['restaurant_name']
    form.location.data = restaurant_details['location']
    form.contact_no.data = restaurant_details['contact_no']
    form.item_1.data = restaurant_details['item_1']
    form.price_1.data = restaurant_details['price_1']
    form.item_2.data = restaurant_details['item_2']
    form.price_2.data = restaurant_details['price_2']
    form.item_3.data = restaurant_details['item_3']
    form.price_3.data = restaurant_details['price_3']
    form.item_4.data = restaurant_details['item_4']
    form.price_4.data = restaurant_details['price_4']
    form.item_5.data = restaurant_details['item_5']
    form.price_5.data = restaurant_details['price_5']
    form.item_6.data = restaurant_details['item_6']
    form.price_6.data = restaurant_details['price_6']
    form.item_7.data = restaurant_details['item_7']
    form.price_7.data = restaurant_details['price_7']
    form.item_8.data = restaurant_details['item_8']
    form.price_8.data = restaurant_details['price_8']
    form.item_9.data = restaurant_details['item_9']
    form.price_9.data = restaurant_details['price_9']
    form.item_10.data = restaurant_details['item_10']
    form.price_10.data = restaurant_details['price_10']

    if request.method == "POST" and form.validate():
        restaurant_id = request.form['restaurant_id']
        restaurant_name = request.form['restaurant_name']
        location = request.form['location']
        contact_no = request.form['contact_no']
        item_1 = request.form['item_1']
        price_1 = request.form['price_1']
        item_2 = request.form['item_2']
        price_2 = request.form['price_2']
        item_3 = request.form['item_3']
        price_3 = request.form['price_3']
        item_4 = request.form['item_4']
        price_4 = request.form['price_4']
        item_5 = request.form['item_5']
        price_5 = request.form['price_5']
        item_6 = request.form['item_6']
        price_6 = request.form['price_6']
        item_7 = request.form['item_7']
        price_7 = request.form['price_7']
        item_8 = request.form['item_8']
        price_8 = request.form['price_8']
        item_9 = request.form['item_9']
        price_9 = request.form['price_9']
        item_10 = request.form['item_10']
        price_10 = request.form['price_10']

        cursor = mysql.connection.cursor()
        cursor.execute('update restaurant set restaurant_id = %s, restaurant_name = %s, location = %s, contact_no = %s where restaurant_id = %s', (restaurant_id, restaurant_name, location, contact_no, rest_id))
        cursor.execute(
            "update item_details set item_1 = %s, price_1 = %s, item_2 = %s, price_2 = %s, item_3 = %s, price_3 = %s, item_4 = %s, price_4 = %s, item_5 = %s, price_5 = %s, item_6 = %s, price_6 = %s, item_7 = %s, price_7 = %s, item_8 = %s, price_8 = %s, item_9 = %s, price_9 = %s, item_10 = %s, price_10 = %s, restaurant_id where restaurant_id = %s", (item_1, price_1, item_2, price_2, item_3, price_3, item_4, price_4, item_5, price_5, item_6, price_6, item_7, price_7, item_8, price_8, item_9, price_9, item_10 , price_10, restaurant_id, rest_id))
        mysql.connection.commit()
        cursor.close()
        flash('Restaurant Details Successfully updated!!')
    return render_template('RESTAURANT_DETAILS_UPDATE.html', form=form)


# --------------------------------------------DELETION OF USERS BY ADMIN------------------------------------------------


@app.route('/delete_users/<string:id>', methods=["POST"])
def delete_users(id):
    cursor = mysql.connection.cursor()
    cursor.execute('delete from users where user_id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash('User Account successfully deleted')
    return redirect(url_for('admin_dashboard'))


# ------------------------------------------------------REPORTS---------------------------------------------------------


@app.route('/reports/<string:id>', methods=["POST", "GET"])
def reports(id):
    form = ReportForm(request.form)
    user_id = id
    cursor = mysql.connection.cursor()
    type = cursor.execute('select user_type from users where user_id = %s', [user_id])
    cursor.close()
    if type == 'customer':
        if request.method == "POST" and form.validate():
            customer_id = request.form('customer_id')
            manager_id = request.form('manager_id')
            restaurant_name = request.form('restaurant_name')
            restaurant_id = request.form('restaurant_id')
            review = request.form('review')
            rating = request.form('rating')
            cursor.execute('INSERT INTO reports(customer_id,restaurant_name, review, rating, restaurant_id)VALUES(%s, %s, %s, %s, %s)', (id, restaurant_name, review, rating, restaurant_id))
            cursor.execute('select manager_id from restaurant_manager where restaurant_id = %s',[restaurant_id])
            manager=cursor.fetchone()
            cursor.execute('INSERT INTO reports(manager_id) VALUES(%s)',[manager])
            mysql.connection.commit()
            cursor.close()
            flash('Report successfully added')
            return redirect(url_for('user_dashboard'))
        cursor = mysql.connection.cursor()
        cursor.execute('select * from reports where customer_id = %s', [user_id])
        report = cursor.fetchall()
        cursor.close()
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('select * from reports where manager_id = %s', [user_id])
    return render_template('REPORTS.html', reports=reports, form=form , type=type)


# -------------------------------------RESTAURANT MANAGERS VIEWING REPORTS----------------------------------------------


@app.route('/view_reports/<string:id>')
def view_reports(id):
    user_id = id
    cursor = mysql.connection.cursor()
    cursor.execute('select * from reports where manager_id = %s',[user_id])
    reports = cursor.fetchall()
    cursor.close()
    return render_template('VIEW_REPORTS.html')


# -----------------------------------------------USER'S DASH BOARD------------------------------------------------------


@app.route('/user_dashboard')
@is_logged_in
def user_dashboard():
    return render_template(url_for('INDEX.html'))


# ----------------------------------------DELETION OF REPORTS BY CUSTOMERS----------------------------------------------


@app.route('/delete_reports/<string:id>', methods=['POST'])
def delete_reports(id):
    id = id
    cursor = mysql.connection.cursor()
    cursor.execute('delete from reports where id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash('Report deleted','success')
    return redirect(url_for('user_dashboard'))


# -----------------------------------------------------VIEW DIET MENU---------------------------------------------------


@app.route('/diet_menu')
def diet_menu():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from diet')
    diet = cursor.fetchall()
    cursor.close()
    return render_template('DIET.html', diet=diet)


# --------------------------------------------------------ADD DIET------------------------------------------------------


@app.route('/add_diet_menu')
def add_diet_menu():
    form = offersform(request.form)
    if request.method == 'POST' and form.validate():
        text = form.text.data
        cursor = mysql.connection.cursor()
        cursor.execute('insert into diet(text) values(%s)',[text])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('admin_dashboard'))

    return render_template('ADD_DIET.html', form=form)


# ----------------------------------------------------EDIT DIET MENU----------------------------------------------------


@app.route('/edit_diet_menu/<string:id>', methods=['POST', 'GET'])
def edit_diet_menu():
    cursor = mysql.connection.cursor()
    cursor.execute('select * from diet where id = %s', [id])
    diet = cursor.fetchone()
    cursor.close()
    form = DietForm(request.form)
    form.text.data = diet[text]
    if request.method == 'POST' and form.validate():
        text = request.form['text']
        cursor = mysql.connection.cursor()
        cursor.execute('update diet set text= %s', [text])
        mysql.connection.commit()
        cursor.close()
        flash('Diet Menu Successfully updated!!')
        return redirect(url_for('admin_dashboard'))
    return render_template('DIET_UPDATE.html', form=form)


# --------------------------------------------------DELETING DIET MENU--------------------------------------------------


@app.route('/delete_diet_menu/<string:id>', methods=['POST'])
def delete_diet_menu(id):
    cursor = mysql.connection.cursor()
    id = id
    cursor.execute("delete from diet where id = %s", [id])
    mysql.connection.commit()
    cursor.close()
    flash('Diet Menu Successfully deleted!!')
    return redirect(url_for('admin_dashboard'))


if __name__=='__main__':
	app.secret_key = 'some secret key'
	app.run(debug = True)
