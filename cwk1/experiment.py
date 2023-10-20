from app import app, db, views, models
from datetime import datetime
print("Running experiment.py ...")
userin = input("Enter a property name: ")
userrent = int(input("Enter a rent: "))
p = models.Property(address=userin,start_date=datetime.utcnow(),duration=5, rent=userrent)
with app.app_context():
    db.session.add(p)
    db.session.commit()

#this functions perfectly for adding