def index():
	form = FORM(INPUT(_name='name', requires=IS_NOT_EMPTY()),
        INPUT(_type='submit'))
