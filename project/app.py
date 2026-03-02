from application import create_app
from application.models import db
    
app = create_app('DevelopmentConfig')    
    
# Create the table
with app.app_context():
	db.create_all()

app.run()