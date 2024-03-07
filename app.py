from flask import*#importing flask
import pymysql

app=Flask(__name__)#calling function flask()
connection=pymysql.connect(host='localhost',user='root',password='',database='tai1_soko_garden')#We are connecting to database tai1_soko_garden which is the localhost server.
cursor=connection.cursor()

app.secret_key="mysecretkey"#set secret key to secure our session



@app.route('/') #routing function home
def home():
    connection=pymysql.connect(host='localhost',user='root',password='',database='tai1_soko_garden')#We are connecting to database tai1_soko_garden which is the localhost server.

    print('Database connected succesfully')
    
    sql='SELECT * FROM products WHERE product_category="Smartphones"'
    cursor=connection.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()#fetchall() is used to fetch the remaiining rows from the search query
    #fetching category electronics
    sql2='SELECT * FROM products WHERE product_category="Electronics"'
    cursor.execute(sql2)
    data2=cursor.fetchall()
    data3=cursor.fetchall()

    sql3='SELECT * FROM products WHERE product_category="Clothing"'
    cursor.execute(sql3)
    data3=cursor.fetchall()

    sql4='SELECT * FROM products WHERE product_category="Other"'
    cursor.execute(sql4)
    data4=cursor.fetchall()

    sql5='SELECT * FROM products WHERE product_category="Utensils"'
    cursor.execute(sql5)
    data5=cursor.fetchall()
    return render_template('index.html',category_smartphones=data, category_Electronics=data2, category_Clothing=data3, 
                                    category_Other=data4, category_Utensils=data5)

@app.route('/upload', methods=['POST','GET'])
def upload():

    if request.method == 'POST':
        #We are receiving all variables sent/submitted from the form
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        product_image_name = request.files['product_image_name']
        product_image_name.save('static/images/'+product_image_name.filename)

        connection=pymysql.connect(host='localhost',user='root',password='',database='tai1_soko_garden')#We are connecting to database tai1_soko_garden which is the localhost server.
        print('Database connected succesfully')
        cursor=connection.cursor() #Function cursor allows code to execute sql commands in a database session

        data= (product_name,product_desc,product_cost,product_category,product_image_name.filename)

        sql= "INSERT INTO products (product_name,product_desc,product_cost,product_category,product_image_name)VALUES (%s,%s,%s,%s,%s)"
        #$s is used as a place holder for the variables in the data variable
        cursor.execute(sql,data)#the execute function is used to execute the query in the variable sql
        connection.commit()#commitfunction is used to write changes in the variables
        return render_template('upload.html', message=' successfully added products')
    else:
        return render_template('upload.html', message='add products')
@app.route('/single_item/<product_id>')
def single_item(product_id):
    sql='SELECT * FROM products WHERE product_id=%s'
    cursor.execute(sql,product_id)
    data=cursor.fetchone()

    return render_template('single_item.html', product=data)


@app.route('/signup',methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username= request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        
        
        #validating passwords
        if len(password1) <8:
            return render_template('signup.html',error='PASSWORD MUST BE MORE THAN 8 CHARACTERS' )
        elif password1 !=password2:
            return render_template('signup.html', error1="PASSWORDS DON'T MATCH")
        
        sql='''INSERT INTO users (username,email,phone,password) VALUES (%s,%s,%s,%s)'''
        cursor.execute(sql,(username,email,phone,password1))
        connection.commit()
        return render_template('signup.html',success='SIGN UP SUCCESSFULLY')                                                    
    else:

        return render_template('signup.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username= request.form['username']
        password1 = request.form['password1']


        tai_sql="SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(tai_sql,(username,password1))
        connection.commit()

        if cursor.rowcount==0:
                return render_template('login.html',error='INVALID CREDENTIALS')
        else:
                session['key']=username#when we log in the user creates his or her own session, we are linking the session with username
                return redirect('/')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear()#we are terminating our session everytime we log out
    return redirect('login')

@app.route('/mpesa',methods=['POST','GET'])
def mpesa():
    #request the amount and phone from single_item.html
    phone=request.form['phone']
    amount=request.form['amount']

    #import mpesa.py module
    import mpesa
    #call stk_push function present in mpesa.py
    mpesa.stk_push(phone,amount)
    #print a message
    return '<h3>please complete payment in your phone and we will deliver in minutes</h3>'\
    '<a href='"/"' class"btn btn-dark">Back to Home</a>'


@app.route('/suppliers',methods=['POST','GET'])
def suppliers():
    if request.method == 'POST':
        firstname= request.form['firstname']
        lastname= request.form['lastname']
        national_ID=request.form['national_ID']
        email=request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
       

        #validating passwords
        if len(password1) <8:
            return render_template('suppliers.html',error='PASSWORD MUST BE MORE THAN 8 CHARACTERS' )
        elif password1 !=password2:
            return render_template('suppliers.html', error1="PASSWORDS DON'T MATCH")
      
        sql='''INSERT INTO suppliers(firstname,lastname,national_ID,email,password) VALUES (%s,%s,%s,%s,%s)'''
        cursor.execute(sql,(firstname,lastname,national_ID,email,password1))
        connection.commit()
        return render_template('suppliers.html', success='supplier added ')                                                    
    else:

        return render_template('suppliers.html')

    
if __name__=='__main__':
 app.run(debug=True)
