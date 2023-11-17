from app import app, models, db
from flask import render_template, flash, request
from .forms import IdeaForm
# We need to import JSON in order to parse the data sent by the JS
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    form = IdeaForm()
    if form.validate_on_submit():
        # Save idea
        new_idea = models.Idea(text=form.idea.data)
        db.session.add(new_idea)
        db.session.commit()

        flash("Thanks for your bright new idea: " + str(form.idea.data))

    # Fetch all the ideas submitted thus far and return to display
    ideas = models.Idea.query.all()
    print("Number of ideas in db:", len(ideas))

    return render_template('index.html', form=form, ideas=ideas)

@app.route('/vote', methods=['POST'])
def vote():
        # Load the JSON data and use the ID of the idea that was clicked to get the object
    data = json.loads(request.data)
    idea_id = int(data.get('idea_id'))
    idea = models.Idea.query.get(idea_id)

        # Increment the correct vote
    if data.get('vote_type') == "up":
        idea.upvotes += 1
    else:
        idea.downvotes += 1

        # Save the updated vote count in the DB
    db.session.commit()
        # Tell the JS .ajax() call that the data was processed OK
    return json.dumps({'status':'OK','upvotes': idea.upvotes, 'downvotes': idea.downvotes })