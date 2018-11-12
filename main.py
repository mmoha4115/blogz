from models import Users,Posts
from app import app , db, request, redirect, render_template, session, flash
from functions import use_pass, empty, author,hash_pwd,pw_validate_hash

@app.before_request
def require_login():
    allowed_routes = ['login', 'register','blog','singleUser','viewpost','index']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']       
        username = Users.query.filter_by(user=user).first()
        if username and pw_validate_hash(username.password,password):
            session['user'] = user
            flash('Logged In', 'error')
            return redirect('/')
        else:
            # TODO - explain why login failed
            flash('User password is invalid or the user does not exist', 'error')
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        verify = request.form['verify']
        
        main_msg = "That's not a valid {0}"
        verify_msg = "Passwords don't match"
        password_error = ''
        verify_error = ''
        user_error = ''
        succes_condition = 0    #counter if no error =0 - return succes.html
        #validate user
        if use_pass(user) == False:
            user = ''
            email_error = main_msg.format('user')
            succes_condition +=1
        #validate password
        if use_pass(password) == False:
            password_error = main_msg.format('password')
            succes_condition+=1
        #validate verify-password
        if verify != password :
            verify_error = verify_msg 
            succes_condition+=1
        #if any error= render user-signup.html with errors else render succes.html
        if succes_condition > 0:
            return render_template('register.html', user=user, user_error=user_error,
            password='', password_error=password_error, 
            verify='', verify_error=verify_error)
        # TODO - validate user's data
        existing_user = Users.query.filter_by(user=user).first()
        if not existing_user:
            password = hash_pwd(password)
            new_user = Users(user, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = user
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"
    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.route('/blog')
def blog():
    page = request.args.get('page',1,type=int)
    posts = Posts.query.order_by(Posts.id.desc()).paginate(page=page,per_page=5)
    #posts = Posts.query.order_by(Posts.title).all()
    return render_template('blog.html', posts=posts)
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ''
        body_error = ''
        bad_field = 0
        if empty(body) == False:
            body_error =  'Please fill in the body.'
            bad_field += 1
        if empty(title) == False:
            title_error = 'Please fiil in the title.' 
            bad_field += 1
        if bad_field > 0:
            return render_template('newpost.html', title=title, body=body,title_error=title_error,body_error=body_error)
        owner = Users.query.filter_by(user=session['user']).first()
        author = session['user']
        new_post = Posts(title,body,owner,author)
        db.session.add(new_post)
        db.session.commit()
        return render_template('viewpost.html',post=new_post)
    if session['user']:
        return render_template('newpost.html')
    else:
        return redirect('/login')

@app.route('/viewpost')
def viewpost():
    post_id = request.args.get('post_id')
    post_id = int(post_id)
    post = Posts.query.filter_by(id = post_id).first()
    post_title = post.title
    post_body = post.body
    post_author = post.author
    return render_template('viewpost.html',post=post)

@app.route('/') #, methods=['GET','POST']
def index():
    users = Users.query.all()
    return render_template('index.html',users = users)

@app.route('/singleUser', methods=['GET','POST'])
def singleUser():
    if request.method == 'GET':
        user = request.args.get('user')
        page = request.args.get('page',1,type=int)
        posts = Posts.query.order_by(Posts.id.desc()).filter_by(author=user).paginate(page=page,per_page=5)
        return render_template('singleUser.html',posts=posts,user=user)
    return redirect('/blog')

if __name__ == '__main__':
    app.run()




