from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app=Flask(__name__)

@app.route('/users/new')
def form():
  return render_template('index.html')

@app.route('/users/create',methods=['POST'])
def add_user_to_db():
  mysql=connectToMySQL('user')
  query="INSERT INTO users (first_name,last_name,email,created_at) VALUES (%(fn)s,%(ln)s,%(em)s,NOW());"
  #The query_db() method returns the row id when we run an INSERT query.
  data={
    'fn':request.form['fname'],
    'ln':request.form['lname'],
    'em':request.form['email']
  }
  user_created=mysql.query_db(query,data)
  print(user_created)
  return redirect(f'/users/{user_created}')

@app.route('/users/<id>')
def show_one_info(id):
  mysql=connectToMySQL('user')
  query="SELECT*FROM users WHERE id=%(id)s;"
  data={
    'id':id
  }
  user=mysql.query_db(query,data)
  print(user)
  return render_template('user.html', userid=id, select_user=user)

@app.route('/users')
def show_all_info():
  mysql=connectToMySQL('user')
  users=mysql.query_db("SELECT*FROM users")
  print(users)
  return render_template('allusers.html', registered_users=users)

@app.route('/users/<id>/edit')
def edit_info(id):
  mysql=connectToMySQL('user')
  query="SELECT*FROM users WHERE id=%(id)s;"
  data={
    'id':id
  }
  user=mysql.query_db(query,data)
  print(user)
  return render_template('edituser.html', userid=id, select_user=user)

@app.route('/users/<id>/update',methods=['Post']) 
def update_info(id):
  mysql=connectToMySQL('user')
  query="UPDATE users SET first_name=%(fn)s, last_name=%(ln)s, email=%(em)s WHERE id=%(id)s"
  data={
    'fn':request.form['fname'],
    'ln':request.form['lname'],
    'em':request.form['email'],
    'id':id
  }
  update_user=mysql.query_db(query,data)
  #The query_db() method returns nothing when we run an UPDATE or DELETE query.
  print(update_user)
  return redirect(f'/users/{id}')

@app.route('/users/<id>/delete') 
def delete_info(id):
  mysql=connectToMySQL('user')
  query="DELETE FROM users WHERE id=%(id)s"
  data={
    'id':id
  }
  delete_user=mysql.query_db(query,data)
  #The query_db() method returns nothing when we run an UPDATE or DELETE query.
  print(delete_user)
  return redirect('/users')

if __name__=="__main__":
  app.run(debug=True)