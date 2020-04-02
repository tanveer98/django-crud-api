from ..models import Category

def init_category(app,se):
    	entry = Category()
    	entry.category_name = 'MISCELLANEOUS'
    	entry.id = 0
    	entry.save()
    	return 
