"""This is the registration controller"""
def register():
	record = db.register(request.args(0))
	form = SQLFORM(db.register,record)
	
	if form.accepts(request,session,hideerror = True):
			response.flash = 'Thanks the form has been accepted'
			redirect(URL('default','login'))
	elif form.errors:
		response.flash = 'please fill the form correctly'
	else:
		response.flash = 'please fill the form'
	return dict(form = form,x = form.vars.id)


"""This function can be used to see any database. This is only for developer use"""
def all_records():
      grid = SQLFORM.grid(db.login,user_signature=False)
      return dict(grid = grid)




"""This function can be used to delete all the entries of a database. This is only for developer use"""
def delete():
	response.flash = "records are being deleted"
	db(db.Comments.comment != None).delete()



"""This is the login function. This will create a session for the logged in user"""
def login():
	import random
	form = SQLFORM(db.login)
	form.custom.submit['_id'] = "buttonstyle"
	if form.accepts(request,session,hideerror = True):
		if(form.vars.Password == db(db.register.Email == form.vars.Email).select()[0].Password):
			response.flash = "you have successfully logged in"
			x = str(random.randint(1000000,10000000))
			db(db.login.id == form.vars.id).update(session_id = x, session_status = 1)
			redirect(URL('timeline/'+x))
		else:
			response.flash = "Sorry wrong password"
			name = "Stranger"
			redirect(URL('default','login'))
	elif form.errors:
		session.flash = "You have to first Register"
		name = "Guest"
		redirect(URL('register'))
	else:
		response.flash = "Please fill in your login details"
		name = "Guest"
	return dict(form = form,name = name)

def about():
	session_id = request.args[0]	
	return locals()

def contact():
	session_id = request.args[0]
	return locals()

def credits():
	session_id = request.args[0]
	return locals()

def about_log():
	session_id = request.args[0]	
	return locals()

def contact_log():
	session_id = request.args[0]
	return locals()

def credits_log():
	session_id = request.args[0]
	return locals()

def timeline():
	session_id = request.args[0]
        r = check(session_id)
	if(r == '0'):
		response.flash = "Hi!"
		redirect(URL('default','login'))
	name = get_name(session_id)
		
	rows = db(db.Image.owner == name).select(orderby=~db.Image.id)
	ids = []	

	for i in rows:
		r = db(db.Albums.album_name == i.album).select()
		for j in r:
			ids.append(j.id)
	fundates = []
	
	import datetime
	from gluon.tools import prettydate

	for i in rows:	
		d = (i.created_on)
		pretty_d = prettydate(d,T)
		fundates.append(pretty_d)		

	return locals()

	
"""This is for the home page of the user"""
def user():
	session_id = request.args[0]
        r = check(session_id)
	if(r == '0'):
		response.flash = "Hi!"
		redirect(URL('default','login'))
	name = get_name(session_id)
	response.flash = "Welcome " + name
	return dict(name = name,session_id = session_id)



"""Using this controller the user can add an album in his database"""
def add_album():
	msg = "welcome"
	args = request.args
	session_id = args[0]
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	response.flash = "Create Album" + name	
	record = db.Albums(request.args(0))
	form = SQLFORM(db.Albums,record)
	if form.accepts(request,session):
		db(db.Albums.id == form.vars.id).update(owner = name)
		x = db(db.register.Email == name).select()[0].albums
		db(db.register.Email == name).update(albums = x + [form.vars.id])
		redirect(URL('my_albums/' + session_id))		
	if form.errors:
		if(len(form.errors) == 1) and (form.errors.default1 == "enter a value"):
			msg = "Hello There!"
	return dict(form = form,msg = msg,session_id = session_id)




"""This will display all tehe albums of the logged in user"""
def my_albums():
	args = request.args
	session_id= args[0]
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	response.flash = "Welcome " + name
	albums = []
	images = []
	rows = db(db.register.Email == name).select()[0].albums	
	for i in rows:
		row = db(db.Albums.id == i).select()[0]
		albums.append(row.album_name)
		if(row.default1!=None):
			images.append(row.default1)
		else:
			image = db(db.Image.id == 28).select()[0]
			images.append(image)
			console.log(image)
	record = db.Albums(request.args(0))
	
	
	form = SQLFORM(db.Albums,record)
	if form.accepts(request,session):
		db(db.Albums.id == form.vars.id).update(owner = name)
		db(db.Albums.id == form.vars.id).update(created_on = request.now)
		x = db(db.register.Email == name).select()[0].albums
		db(db.register.Email == name).update(albums = x + [form.vars.id])		
		image_id = db.Image.insert(image = form.vars.default1,created_on = request.now, album = form.vars.album_name,owner = name)
		y = db(db.Albums.id == form.vars.id).select()[0].images
		#db(db.Albums.id == form.vars.id).update(tags = [])
		db(db.Albums.album_name == form.vars.album_name).update(images = y + [image_id])
		redirect(URL('my_albums/' + session_id))
	if form.errors:
		response.flash = "Sorry, The album was not created! :("	
	return dict(albums = albums,name = name,images = images,ids = rows,session_id = session_id,form = form)


"""This will display all the images of a paticular album"""
def display_album():
	args = request.args
	session_id = request.args[0]
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	album_name = request.args[1]
	owner = request.args[2]
	album_id = request.args[3]
	response.flash = "Welcome " + name
	images = []
	rows = db(db.Albums.id == album_id).select()[0].images
	for j in rows:
		images.append(db(db.Image.id == j).select()[0].image)
	record = db.Image(request.args(0))
	
	form = SQLFORM(db.Image,record)
	if form.accepts(request,session):
		db(db.Image.id==form.vars.id).update(album=album_name)
		db(db.Image.id==form.vars.id).update(owner=name)
		db(db.Image.id==form.vars.id).update(created_on=request.now)
		rows = db(db.Albums.id == album_id).select()[0]
		x = rows.images		
		db(db.Albums.id == album_id).update(images = x + [form.vars.id])
		redirect(URL('display_album/'+session_id+'/'+album_name+'/' +owner +'/' + album_id ))
	elif form.errors:
		response.flash = "No image selected"
	record2 = db.Tags(request.args(0))
	form2 = SQLFORM(db.Tags,record2)
	form2.custom.widget.tag['_id'] = "tag_id"
	form2.custom.submit.update(_id="upload3",_value="Tag It")
	
	if form2.accepts(request,session):
		x = db(db.Albums.id == album_id).select()[0].tags
		if form2.vars.tag not in db(db.Albums.id == album_id).select()[0].tags:
			db(db.Albums.id == album_id).update(tags = x + [form2.vars.tag])
		c = db(db.Album_by_tag.Tag == form2.vars.tag).count()			
		if c == 0:
			db.Album_by_tag.insert(Tag = form2.vars.tag,albums = [])				
		y = db(db.Album_by_tag.Tag == form2.vars.tag).select()[0].albums
			
		if((int(album_id) in y) == False):
			y.append(album_id)			
			db(db.Album_by_tag.Tag == form2.vars.tag).update(albums = y)

		db(db.Tags.id == form2.vars.id).delete()		
	
	record3 = db.Albums(request.args(0))
			

	return dict(form = form,form2 = form2,images = images,album_name = album_name,name  = name,owner = owner,session_id = session_id, album_id = album_id)

def test():
	return locals()

"""This will display the clicked image and the comments on that image"""
def display_image():
	args = request.args
	session_id = request.args[0]
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	response.flash = "Welcome "+ name

	album = request.args[1]
	image = request.args[2]
	owner = request.args[3]
	album_id = request.args[4]

	album_name = album

	row = db(db.Image.image == image).select()[0]
	owner = row.owner
	image_id1 = row.id
	
	new = db(db.Albums.id == album_id).select()[0]
	pics = new.images
	
	i = 0
	prev_id = image_id1
	next_id = image_id1

	for i in range(0,len(pics)):
		if image_id1 == pics[i]:
			if i > 0:
				prev_id = pics[i-1]
			else:
				prev_id = pics[i]
		
			if i < len(pics)-1:			
				next_id = pics[i+1]
			else:
				next_id = pics[i]
			break

	p = db(db.Image.id == prev_id).select()
	for j in p:
		previmage = j.image 

	n = db(db.Image.id == next_id).select()
	for j in n:
		nextimage = j.image 
	
	record = db.register(request.args(0))
	form = SQLFORM(db.Comments,record)

	
	form.custom.widget.comment['_id'] = "feedback"
	form.custom.widget.comment['_placeholder'] = "Comment here ..."
	form.custom.widget.comment['_type'] = "textarea"
	
	form.custom.submit['_id'] = "postcomment"
	form.custom.submit['_value'] = "Post Comment"	

	if form.accepts(request,session):
		db(db.Comments.id == form.vars.id).update(commentator = name)
		db(db.Comments.id == form.vars.id).update(image_id = image_id1)
		db(db.Comments.id == form.vars.id).update(created_on = request.now)
		#if(owner!=name):
		#	db(db.Comments.id == form.vars.id).update(comment_status = 0)
		#	arr = db(db.register.Email == owner).select()[0].requests
		#	db(db.register.Email == owner).update(requests = arr + [form.vars.id])
		#else:
		db(db.Comments.id == form.vars.id).update(comment_status = 1)
	rows = db(db.Comments.image_id == image_id1).select()
	commentator = []
	comment = []
	fundates = []
	
	import datetime
	from gluon.tools import prettydate	

	for i in rows:
		if(int(i.comment_status) == 1):
			commentator.append(i.commentator)
			comment.append(i.comment)
			d = (i.created_on)
			pretty_d = prettydate(d,T)
			fundates.append(pretty_d)	
			
	person_name_first = []
	person_name_last = []

	for i in range(0,len(commentator)):
		person = db(db.register.Email == commentator[i]).select()[0].First_Name
		person_2 = db(db.register.Email == commentator[i]).select()[0].Last_Name
		person_name_first.append(person)
		person_name_last.append(person_2)

	return dict( name = name, previmage = previmage, nextimage = nextimage, fundates = fundates,image = image,owner = owner, album_id = album_id, album_name = album_name, form = form,commentator = commentator,comment = comment,session_id = session_id, person_name_first = person_name_first, person_name_last = person_name_last)


"""This will display all the albums whose permission  has been set to public"""
def public_albums():
	rows = db((db.Albums.album_name!=None) & (db.Albums.permission == 'PUBLIC')).select()
	args = request.args
	session_id = request.args[0]
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	album_name = []
	owners = []
	images = []
	ids = []
	for i in rows:
		album_name.append(i.album_name)
		images.append(i.default1)
		owners.append(i.owner)	
		ids.append(i.id)	
	return dict(albums = album_name,owners = owners, images = images,name = name,ids = ids,session_id = session_id)

def tagged_albums():
	args = request.args
	session_id = args[0]
	tag = args[1]
	
	r = check(session_id)
	if(r == '0'):
		redirect(URL('default','login'))
	name = get_name(session_id)
	
	l = ['Nature','Travel','Entertainment','Work','Others']
	tag_name = l[int(tag)]	
	
	albums = []
	owners = []
	images = []
	ids = []
	album_ids = []

	ab = db(db.Album_by_tag.Tag == l[int(tag)]).select()
	
	for i in ab:
		for j in i.albums:		
			album_ids.append(j)

	for i in album_ids:
		rows = db((db.Albums.id == i) & (db.Albums.permission == 'PUBLIC')).select() 
		for j in rows:
			albums.append(j.album_name)
			images.append(j.default1)
			owners.append(j.owner)
			ids.append(j.id)

	return locals()
	
def download():
        return response.download(request, db)
	
def get_name(session_id):
	return db(db.login.session_id == session_id).select()[0].Email

"""This function checks if the given session is valid or not"""
def check(session_id):
	x = db(db.login.session_id == session_id).select()
	if(len(x) == 0):
		return 0
	else :
		return x[0].session_status
		
def not_logged_in():
	response.flash = "Sorry You Are Not Logged In"
	return dict()

def logout():
	session_id = request.args[0]
	x = db(db.login.session_id == session_id).select()
	if(len(x) == 0):
		redirect(URL('default','login'))
	else:
		db(db.login.session_id == session_id).update(session_status = 0)
		redirect(URL('default','login'))
	return dict()

"""This function will show all the requests for comments"""
def requests():
	session_id = request.args[0]
	name = get_name(session_id)
	requests = db(db.register.Email == name).select()[0].requests
	response.flash = requests
	comments = []
	commentators = []
	ids = []
	for i in requests:
		x = db(db.Comments.id == i).select()[0]
		comments.append(x.comment)
		commentators.append(x.commentator)
		ids.append(i)
	return dict(session_id = session_id,comments = comments,commentators = commentators,ids = ids)

def validate_comment():
	session_id = request.args[0]
	comment_id = request.args[1]
	db(db.Comments.id == int(comment_id)).update(comment_status = 1)
	x = db(db.Comments.id == comment_id).select()[0]
	image_id = x.image_id
	owner = db(db.Image.id == image_id).select()[0].owner
	y = db(db.register.Email == owner).select()[0].requests
	y = y.remove(int(comment_id))
	db(db.register.Email == owner).update(requests = y)
	redirect(URL('requests/' + session_id) )
	return dict()

