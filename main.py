from flask import  send_from_directory
from flask import session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, login_required
from flask_login import current_user
from flask_login import logout_user
from werkzeug.utils import secure_filename
import os
from decimal import Decimal
import random
import string
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_login import UserMixin
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash






app = Flask(__name__)
app.secret_key = 'your_secret_key'
''''
# MySQL Remote Configuration
app.config['MYSQL_HOST'] = 'sql.freedb.tech'
app.config['MYSQL_USER'] = 'freedb_shanid'
app.config['MYSQL_PASSWORD'] = '@#APC4wbcfHMq2C'
app.config['MYSQL_DB'] = 'freedb_AUCTION'
# MySQL  Configuration
'''
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'auction'

mysql = MySQL(app)


















# Initialize Flask-Login
login_manager = LoginManager(app)
home_directory = os.path.expanduser("~")

# Construct the full path for UPLOAD_FOLDER and UPLOAD_FOLDER1

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "seller_documents")
app.config['UPLOAD_FOLDER1'] = os.path.join(os.getcwd(), "products")
app.config['UPLOAD_FOLDER2'] = os.path.join(os.getcwd(), "images")


class User(UserMixin):
    def __init__(self, user_id, username, role, password,address,status,wallet):
        self.id = user_id
        self.username = username
        self.role = role
        self.password = password
        self.address=address
        self.status=status
        self.status=wallet

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'shanidsulthan@gmail.com'  # Your Gmail email address
SMTP_PASSWORD = 'pvhtbatctnnuktke' # Your Gmail password
def send_reset_email(recipient, token):
    sender_email = SMTP_USERNAME

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = 'Password Reset Link h'

    body = f'Click the link to reset your password: http://127.0.0.1:5000/reset-password/{token}'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return str(e)
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, role, password,address,status,wallet FROM users WHERE id = %s", [user_id])
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        user_id, username, role, password,address,status,wallet = user_data
        user = User(user_id, username, role, password,address,status,wallet)
        return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

         return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password, role,status FROM users WHERE username = %s", [username])
        user_data = cur.fetchone()

        if user_data:
            user_id, user_username, user_password, user_role,status = user_data

            if user_password==password and status=="approved":
                user = load_user(user_id)
                login_user(user)
                session['user_id'] = user_id
                session['username'] = user_username
                session['role'] = user_role
                flash('Login successful', 'success')
                return redirect(url_for('dashboard'))
            if status == "pending":
                flash('Login failed. Admin Approval Needed', 'error')
            else:
                flash('Login failed. Check your password.', 'error')
        else:
            flash('User not found. Check your username.', 'error')

    return render_template('login.html')
@app.route('/css/<path:path>')
def send_report(path):
    return send_from_directory('css', path)
@app.route('/fonts/<path:path>')
def send_report1(path):
    return send_from_directory('fonts', path)
@app.route('/images/<path:path>')
def send_report2(path):
    return send_from_directory('images', path)
@app.route('/js/<path:path>')
def send_report3(path):
    return send_from_directory('js', path)
@app.route('/vendor/<path:path>')
def send_report4(path):
    return send_from_directory('vendor', path)
@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user.role


    if current_user.role == 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('admin_dashboard'))
    if current_user.role=='seller':
       return redirect('seller/dashboard')
    return render_template('dashboard.html',user=user)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        user_id = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE id = %s", [user_id])
        stored_password_tuple = cur.fetchone()

        # Extract the password from the tuple (assuming it's in the first element)
        stored_password = stored_password_tuple[0]

        print("Stored Password:", stored_password)
        print("Old Password:", old_password)

        if stored_password == old_password:

            new_password_hashed = new_password
            cur.execute("UPDATE users SET password = %s WHERE id = %s", (new_password_hashed, user_id))
            mysql.connection.commit()
            cur.close()

            flash('Password changed successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid old password. Password not changed.', 'error')

    return render_template('change_password.html')
@app.route('/logout')
@login_required
def logout():
    # Use Flask-Login's logout_user function to log the user out
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        # Check for duplicate username
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", [username])
        existing_username = cur.fetchone()
        cur.close()

        # Check for duplicate email
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE email = %s", [email])
        existing_email = cur.fetchone()
        cur.close()

        if existing_username:
            flash('Username already exists. Choose a different username.', 'error')
        elif existing_email:
            flash('Email address is already registered. Use a different email.', 'error')
        else:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form['role']  # Get the selected role from the form
            address = request.form['address']

            if password == confirm_password:
                password_hash = password


                if role == 'seller':
                    # Handle file upload for seller's proof of document
                    document = request.files['document']
                    if document:
                        # Save the uploaded document with a unique filename
                        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                        document_filename = secure_filename(document.filename)
                        document.save(os.path.join(app.config['UPLOAD_FOLDER'], document_filename))
                        cur = mysql.connection.cursor()
                        cur.execute("INSERT INTO seller_documents (user_id, document_filename) VALUES (%s, %s)",
                                    (username, document_filename))
                        mysql.connection.commit()
                        cur.close()

                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO users (username, password, email, role, status,address) VALUES (%s, %s, %s, %s, %s,%s)",
                    (username, password_hash, email, role, 'approved' if role == 'buyer' else 'pending', address))

                mysql.connection.commit()
                cur.execute(
                    "SELECT id from users where username=%s",
                    [username])
                id=cur.fetchone()
                print(id)
                cur.execute(
                    "INSERT INTO wallet (user_id, balance) VALUES (%s, %s)",
                    (id, '0'))
                mysql.connection.commit()
                cur.close()



                # Get the user ID of the newly created user


                # Create a wallet for the user with an initial balance (e.g., 0.00)

                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Password and confirm password do not match.', 'error')

    return render_template('registration.html')

@app.route('/admin/dashboard')
@login_required  # Ensure that the user is an authenticated admin
def admin_dashboard():
    if current_user.role != 'admin':
        # Only admin users are allowed to access the admin dashboard
        return redirect(url_for('dashboard'))



    return render_template('admin_dashboard.html')

@app.route('/image/p/<filename>')
def serve_image1(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER1'], filename)
@app.route('/image/i/<filename>')
def serve_image2(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER2'], filename)
@app.route('/seller_document/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
@app.route('/admin/approve_seller/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Ensure that the user is an authenticated admin
def approve_seller(user_id):
    if current_user.role != 'admin':
        # Only admin users are allowed to approve seller registrations
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET status = 'approved' WHERE id = %s AND role = 'seller'", [user_id])
    mysql.connection.commit()
    cur.close()

    flash('Seller registration approved.', 'success')
    return redirect(url_for('admin_dashboard'))
reset_tokens = {}

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Generate a random token
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

            import datetime

            # Set token expiration time (e.g., 1 hour from now)
            expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            reset_tokens[token] = (email, expiration_time)
            email_sent = send_reset_email(email, token)

            if email_sent is True:
                flash('Password reset email sent. Check your inbox.', 'success')
            else:
                flash('Email could not be sent. Check your email configuration.', 'error')

            return redirect(url_for('login'))
            # Send a password reset email (not implemented here)



        flash('Email not found. Check your email address.', 'error')

    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    if token in reset_tokens:
        email, expiration_time = reset_tokens[token]
        import datetime
        if datetime.datetime.now() <= expiration_time:
            if request.method == 'POST':
                new_password = request.form['password']
                cur = mysql.connection.cursor()

                cur.execute('UPDATE users SET password = %s WHERE email = %s', (new_password, email))

                mysql.connection.commit()
                cur.close()


                del reset_tokens[token]

                flash('Password reset successful. You can now log in with your new password.', 'success')
                return redirect(url_for('login'))

            return render_template('reset_password.html', token=token)

    flash('Invalid or expired token. Request a new password reset link.', 'error')
    return redirect(url_for('login'))














@app.route('/admin/buyers')
@login_required  # Ensure that the user is an authenticated admin

def admin_buyers():
    if current_user.role != 'admin':

        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE role='buyer';"
    cur.execute(query)

    # Fetch all rows from the result
    buyers = cur.fetchall()

    # Render the template with the buyers data
    return render_template('buyersall.html', buyers=buyers)



@app.route('/admin/sellers')
@login_required  # Ensure that the user is an authenticated admin

def admin_sellers():
    if current_user.role != 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE role='seller';"
    cur.execute(query)

    # Fetch all rows from the result
    sellers = cur.fetchall()

    # Render the template with the buyers data


    return render_template('sellersall.html',sellers=sellers)

# View Buyer/Seller route
@app.route('/admin/view/<role>/<int:user_id>')
@login_required  # Ensure that the user is an authenticated admin

def view_user(role, user_id):
    if current_user.role != 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s and role=%s", (user_id,role))
    user = cur.fetchone()
    return render_template('view_user.html', user=user)


# Edit Buyer/Seller route
@app.route('/admin/edit/<role>/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Ensure that the user is an authenticated admin

def edit_user(role, user_id):
    if current_user.role != 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s and role=%s", (user_id,role))
    user = cur.fetchone()
    if request.method == 'POST':
        # Update user details based on the form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        wallet = int(user[8]) + int(request.form['wallet'])  # Assuming the wallet column is at index 8
        # Execute the UPDATE query
        cur.execute(
            "UPDATE users SET username = %s, email = %s, password = %s, address = %s WHERE id = %s and role=%s",
            (username, email, password, address, user_id,role))

        # Commit the changes
        mysql.connection.commit()
        cur.execute(
            "UPDATE wallet SET balance = %s, last_source_of_update = %s WHERE user_id = %s",
            (wallet, current_user.role + " " + " ADDED AMOUNT " + request.form['wallet'], user_id)
        )
        mysql.connection.commit()
        flash('User details updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_user.html', user=user)


# Delete Buyer/Seller route
@app.route('/admin/delete/<role>/<int:user_id>')
@login_required  # Ensure that the user is an authenticated admin

def delete_user(role, user_id):
    if current_user.role != 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s and role = %s", (user_id,role))
    mysql.connection.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))
@app.route('/approveseller')
@login_required
def approveseller():
    if current_user.role != 'admin':
        # Redirect to the dashboard if the user is already logged in
        return redirect(url_for('dashboard'))
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT u.id, u.username, u.email, s.document_filename FROM users u LEFT JOIN seller_documents s ON u.username = s.user_id WHERE u.role = 'seller' AND u.status = 'pending'")
    pending_seller_data = cur.fetchall()
    cur.close()

    return render_template('approveseller.html', pending_seller_data=pending_seller_data)





@app.route('/seller/dashboard')
@login_required
def seller_dashboard():
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))
    # Add code to display the seller dashboard.
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s and role='seller'", (current_user.id,))
    user = cur.fetchone()
    return render_template('seller_dashboard.html', user=user)



@app.route('/seller/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        document = request.files['document']


        if document:
            # Save the uploaded document with a unique filename
            os.makedirs(app.config['UPLOAD_FOLDER1'], exist_ok=True)
            document_filename = secure_filename(document.filename)
            document.save(os.path.join(app.config['UPLOAD_FOLDER1'], document_filename))

        # Assuming you have a MySQL connection named 'conn'
            cursor = mysql.connection.cursor()

        # Execute an INSERT query to add a new product
            cursor.execute("INSERT INTO products (name, description, supplier_id, path) VALUES (%s, %s, %s, %s)",
                       (name, description, current_user.id, document_filename))

        # Commit the changes
            mysql.connection.commit()

        # Close the cursor

            flash('Product added successfully', 'success')
        return redirect(url_for('seller_dashboard'))

    return render_template('add_product.html')




@app.route('/seller/view_products')
@login_required
def view_products():
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))

    # Assuming you have a MySQL connection named 'conn'
    cursor = mysql.connection.cursor()

    # Execute a SELECT query to fetch products associated with the current seller
    cursor.execute("SELECT * FROM products WHERE supplier_id = %s and id not in (select product_id from auction )", (current_user.id,))

    # Fetch all the rows
    products = cursor.fetchall()





    return render_template('view_products.html', products=products)


@app.route('/seller/add_to_auction/<int:product_id>', methods=['POST'])
@login_required
def add_to_auction(product_id):
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))

    cursor = mysql.connection.cursor()

    # Execute a SELECT query to fetch products associated with the current seller
    cursor.execute("SELECT * FROM products WHERE id = %s and supplier_id= %s and id not in (select product_id from auction )", (product_id,current_user.id))

    # Fetch all the rows
    product = cursor.fetchone()

    if product:
        try:
            # Validate the end date format
            auction_end_time = datetime.strptime(request.form['end_date'], '%Y-%m-%d')

            # Validate other form data if needed

            # Create a new auction record for the product
            cursor.execute("""
                INSERT INTO auction (product_id, auction_end_time, product_name, base_price,category_id)
                VALUES (%s, %s, %s, %s,%s)
            """, (product_id, auction_end_time, product[1], request.form['base_price'],request.form['category']))

            mysql.connection.commit()

            flash('Product added to the auction', 'success')
        except ValueError:
            flash('Invalid date format', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
    else:
        flash('Product does not exist', 'error')

    return redirect(url_for('seller_dashboard'))
@app.route('/seller/auction/<int:product_id>', methods=['GET'])
@login_required
def add_to_auction1(product_id):
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))
    cursor = mysql.connection.cursor()
    # Fetch category lists from the Category table using a cursor
    cursor.execute("SELECT category_id, name FROM category")
    categories = cursor.fetchall()

    # Pass the product_id and categories to the template as context
    return render_template('add_auction.html', product_id=product_id, categories=categories)


@app.route('/seller/view_products_in_auction')
@login_required
def view_products_in_auction():
    if current_user.role != 'seller':
        return redirect(url_for('dashboard'))

    try:
        # Execute SQL query to get products in auction for the current seller
        query = """
            SELECT products.*, auction.*
            FROM products
            JOIN auction ON products.id = auction.product_id
            WHERE products.supplier_id = %s
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (current_user.id,))
        products_in_auction = cur.fetchall()

        return render_template('view_products_in_auction.html', products_in_auction=products_in_auction)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect(url_for('seller_dashboard'))


@app.route('/')
def homepage():

        # Execute SQL query to get ongoing auctions and join with the Product table
        query = """
            SELECT products.name, products.path, products.description, auction.base_price, auction.auction_end_time, auction.final_bid_amount, auction.id, category.name FROM auction JOIN products ON auction.product_id = products.id JOIN category ON auction.category_id = category.category_id WHERE auction.auction_end_time > NOW();

        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        ongoing_auctions = cur.fetchall()

        return render_template('homepage.html', auctions=ongoing_auctions)


    # Handle the error or redirect as neededF



@app.route('/bid/<int:auction_id>', methods=['GET', 'POST'])
def bid(auction_id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()

        # Fetch the auction and product information
        cur.execute("SELECT * FROM auction WHERE id = %s", [auction_id])
        auction_data = cur.fetchone()

        cur.execute("SELECT * FROM products WHERE id = %s", [auction_data[1]])

        product_data = cur.fetchone()
        print(product_data)
        # Get the current datetime
        current_time_with_millis = datetime.now()

        # Truncate milliseconds by using replace
        current_time = current_time_with_millis.replace(microsecond=0)

        auction_end_time = auction_data[3].replace(microsecond=0)
        #print(auction_end_time, current_time.replace(microsecond=0))
        # Check if the auction is still ongoing
        if auction_end_time <= current_time:
            print("hi")

            # Fetch all bids for the current auction
            cur.execute("SELECT * FROM bids WHERE auction_id = %s", [auction_id])
            bids = cur.fetchall()

            if bids:
                # Find the highest bid
                highest_bid = max(bids, key=lambda bid: bid[4])


                # Update the auction table with the winner_id
                winner_id = highest_bid[2]
                fine=highest_bid[4]# Assuming user_id is the third column in the bids table
                cur.execute("UPDATE auction SET winner_id = %s WHERE id = %s", [winner_id, auction_id])
                cur.execute("UPDATE auction SET final_bid_amount = %s WHERE id = %s", [fine, auction_id])
                cur.execute("SELECT moneydistributed FROM auction WHERE id = %s", [auction_id])
                condition = cur.fetchone()  # Use fetchone() to get a single value
                mysql.connection.commit()

                if condition and condition[0] == 'no':
                    print("hi")
                    supplier_share = Decimal(highest_bid[4]) * Decimal('0.7')
                    supplier_share = supplier_share.quantize(Decimal('0.01'))  # 70% to supplier
                    admin_share = Decimal(highest_bid[4]) * Decimal('0.2')
                    admin_share = admin_share.quantize(Decimal('0.01'))  # 20% to admin

                    # Update supplier's wallet
                    cur.execute("SELECT supplier_id FROM products WHERE id = %s", [auction_data[1]])
                    supplier_id = cur.fetchone()[0]
                    cur.execute("SELECT wallet FROM users WHERE id = %s", [supplier_id])
                    supplier_wallet = Decimal(cur.fetchone()[0]).quantize(Decimal('0.01'))
                    new_supplier_balance = supplier_wallet + supplier_share
                    cur.execute("UPDATE wallet SET balance = %s, last_source_of_update = %s WHERE user_id = %s",
                                [new_supplier_balance,
                                 f"{supplier_share} ADDED AS SUPPLIER SHARE FOR AUCTION NO {auction_id}",
                                 supplier_id])

                    # Update admin's wallet (assuming you have a specific admin user ID)
                    admin_user_id = 21  # Replace with the actual admin user ID
                    cur.execute("SELECT wallet FROM users WHERE id = %s", [admin_user_id])
                    admin_wallet = Decimal(cur.fetchone()[0]).quantize(Decimal('0.01'))
                    new_admin_balance = admin_wallet + admin_share
                    cur.execute("UPDATE wallet SET balance = %s, last_source_of_update = %s WHERE user_id = %s",
                                [new_admin_balance,
                                 f"{admin_share} ADDED AS ADMIN SHARE FOR AUCTION NO {auction_id}",
                                 admin_user_id])

                    cur.execute("UPDATE auction SET moneydistributed = 'yes' WHERE id = %s", [auction_id])

                    update_query = """
                        UPDATE wallet
                        JOIN (
                            SELECT user_id, MAX(bid_amount) AS total_bid_amount
                            FROM bids, auction
                            WHERE auction.id = %s
                            AND bids.auction_id = auction.id
                            AND bids.user_id != auction.winner_id
                            GROUP BY user_id
                        ) AS subquery ON wallet.user_id = subquery.user_id
                        SET wallet.balance = wallet.balance + subquery.total_bid_amount,
                            wallet.last_source_of_update = CONCAT('REFUND FOR BIDS PLACED IN AUCTION ', %s, ' WHICH ENDED AND YOU DID NOT WIN');
                    """

                    cur.execute(update_query, (auction_id, auction_id))

                    # Commit the changes to the database
                    mysql.connection.commit()

                    # Close the cursor and database connection

                cur.execute("SELECT * FROM auction WHERE id = %s", [auction_id])
                auction_data = cur.fetchone()




        print(auction_end_time, current_time)
        if auction_end_time >= current_time:  # Assuming auction_end_time is the sixth column

            # Fetch all bids for the current product that are still open
            cur.execute("SELECT * FROM bids,users WHERE auction_id = %s and bids.user_id=users.id", [auction_id])
            bids = cur.fetchall()

            # Find the highest bid amount
            highest_bid = max(bids, key=lambda bid: bid[4]) if bids else None  # Assuming bid_amount is the fifth column

            return render_template('bidding_page.html', product_data=product_data, auction_data=auction_data, bids=bids,
                                   highest_bid=highest_bid,current_time=current_time)
        else:
            return render_template('bidding_page.html', product_data=product_data, auction_data=auction_data, bids=None,highest_bid=None,current_time=current_time)

    if request.method == 'POST':

        # Get the bid amount from the form
        bid_amount = float(request.form.get('bid_amount'))

        # Fetch the auction and product information
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM auction WHERE id = %s", [auction_id])
        auction_data = cur.fetchone()


        # Check if the auction is still ongoing
        current_time = datetime.now()
        if auction_data[3] >= current_time:  # Assuming auction_end_time is the sixth column


            # Check if the user has enough funds in their wallet
            try:
             user_id = current_user.id
            except Exception as e:
             flash("login required")
             return redirect(url_for('login'))

            cur.execute("SELECT wallet FROM users WHERE id = %s", [user_id])
            user_data = cur.fetchone()
            wallet_balance = user_data[0]

            # Check if the user has a previous bid for this auction
            cur.execute(
                "SELECT bid_amount FROM bids WHERE auction_id = %s AND user_id = %s ORDER BY timestamp DESC LIMIT 1",
                [auction_id, user_id])
            previous_bid = cur.fetchone()
            if previous_bid:
                previous_bid_amount = Decimal(previous_bid[0])
            else:
                previous_bid_amount = Decimal('0.0')

            # Fetch the current maximum bid for this auction
            cur.execute("SELECT MAX(bid_amount) FROM bids WHERE auction_id = %s", [auction_id])

            current_highest_bid = cur.fetchone()[0] or auction_data[7]

            # Calculate the total bid amount (current highest bid + new bid)
            total_bid_amount = current_highest_bid + Decimal(bid_amount)
            auctual_bid = total_bid_amount-previous_bid_amount
            if wallet_balance >= auctual_bid:
                # Calculate the bid difference between the new bid and the previous bid

                    # Deduct the bid difference from the user's wallet
                    new_balance = float(wallet_balance) - float(auctual_bid)
                    cur.execute("UPDATE wallet SET balance = %s, last_source_of_update = %s WHERE user_id = %s",
                        [new_balance, f"AMOUNT {auctual_bid} DEDUCTED FOR BID IN AUCTION {auction_id}" , user_id])

            # Record the bid in the database
                    cur.execute("INSERT INTO bids (auction_id, user_id, bid_amount, timestamp) VALUES (%s, %s, %s, %s)",
                                [auction_id, user_id, total_bid_amount, current_time])

                    mysql.connection.commit()
                    cur.close()

                    return redirect(url_for('bid', auction_id=auction_id))

            else:
                return "Insufficient funds in your wallet to place this bid."
        else:
            return "Auction has ended, and no more bids can be placed."

        #
@app.route('/delete_product/<int:product_id>', methods=['GET'])
@login_required
def delete_product(product_id):
    try:
        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Fetch the product to check if the current user is the seller
        cur.execute("SELECT supplier_id FROM products WHERE id = %s", [product_id])
        seller_id = cur.fetchone()

        if seller_id and seller_id[0] == current_user.id:
            # Execute the DELETE statement
            cur.execute("DELETE FROM products WHERE id = %s", [product_id])

            # Commit the changes to the database
            mysql.connection.commit()

            # Close the cursor
            cur.close()

            # Redirect back to the page where the products are listed
            return redirect(url_for('view_products'))
        else:
            return "You are not authorized to delete this product."

    except Exception as e:
        # Handle any exceptions (e.g., database errors)
        return "Error deleting the product: " + str(e)
@app.route('/buyer_portal')
@login_required
def buyer_portal():

        # Create a MySQL cursor
        cur = mysql.connection.cursor()

        # Fetch bids made by the current user
        cur.execute("SELECT b.id, p.name, a.auction_end_time, b.bid_amount, a.winner_id " 
                    "FROM bids b "
                    "JOIN auction a ON b.auction_id = a.id "
                    "JOIN products p ON a.product_id = p.id "
                    "WHERE b.user_id = %s", [current_user.id])

        bids = cur.fetchall()

        # Close the cursor
        cur.close()

        return render_template('buyer_portal.html', bids=bids)
@app.route('/admin/list_auctions/<int:seller_id>')
def list_auctions_for_seller(seller_id):
    if current_user.role=="admin":
        # Establish a MySQL connection

        cursor = mysql.connection.cursor()
        # Fetch auctions by the specified seller_id
        query = "SELECT auction.id,products.name,auction.base_price,auction.auction_end_time FROM auction,products WHERE products.id=auction.product_id and products.supplier_id = %s"
        cursor.execute(query, (seller_id,))
        auctions = cursor.fetchall()
        print(auctions)

        # Close the cursor and MySQL connection
        cursor.close()


        # Render the auctions in the HTML template
        return render_template('admin_list_auctions.html', auctions=auctions)
    else:
        return redirect(url_for('dashboard'))
@login_required
@app.route('/wallet_transaction_history/')
def wallet_transaction_history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM walletlog WHERE user_id = %s ORDER BY timestamp DESC", (current_user.id,))

    transactions = cur.fetchall()
    cur.close()

    return render_template('wallet_transaction_history.html', transactions=transactions)


if __name__ == '__main__':
    app.run(debug=True)

