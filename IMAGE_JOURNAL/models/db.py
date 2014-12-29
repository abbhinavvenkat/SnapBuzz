db = DAL('sqlite://webform.sqlite')
db.define_table('Comments',
		Field('image_id'),
		Field('commentator'),
		Field('comment_status'),
		Field('created_on','datetime'),
		Field('comment',requires = IS_NOT_EMPTY()))



db.define_table('Image',
		Field('image','upload',requires = IS_NOT_EMPTY()),
		Field('created_on','datetime'),		
		Field('album'),
		Field('owner'),
		Field('comments','list:integer'))



db.define_table('Albums',
		Field('album_name',requires = IS_NOT_EMPTY()),
		Field('owner'),
		Field('default1','upload',requires = IS_NOT_EMPTY()),
		Field('created_on','datetime'),
		Field('permission',requires = IS_IN_SET(['PUBLIC','PRIVATE']),default='PRIVATE'),
		Field('tags','list:string'),
		Field('images','list:integer'))

db.define_table('Tags',
		Field('tag',requires = IS_IN_SET(['Nature','Travel','Entertainment','Work','Others'])))

db.define_table('register',
	Field('First_Name',requires = IS_NOT_EMPTY()),
	Field('Last_Name',requires = [IS_NOT_EMPTY(),IS_ALPHANUMERIC()]),
	Field('Email',unique = True,requires = [IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'register.Email')]),
	Field('Password','password',requires = IS_NOT_EMPTY()),
	Field('validate','password',requires = IS_EQUAL_TO(request.vars.Password)),
	Field('albums','list:integer'),
	Field('requests','list:integer')
)

db.define_table('login',
	Field('Email',requires = IS_NOT_EMPTY()),
	Field('Password','password',requires = IS_NOT_EMPTY()),
	Field('session_id'),
	Field('session_status'))

db.define_table('Album_by_tag',
	Field('Tag',requires = IS_IN_SET(['Nature','Travel','Entertainment','Work','Others'])),
	Field('albums','list:integer'))
	
