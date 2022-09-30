
from flask import Blueprint, render_template,request, flash, jsonify, redirect
from flask_login import login_required, current_user
from . import db
from .models import Note, User
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required    
def home():
    if request.method == 'POST':
        note= request.form.get('note')
        if len(note)< 4:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()    
            flash('Note created!', category='success')
    return render_template('home.html', user=current_user)





@views.route('/delete-note', methods=['POST'])
def delete_note():
    note= json.loads(request.data)
    noteId= note['noteId']
    note= Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    note = Note.query.get(id)
    if request.method == "POST":
        note.data = request.form['update']
        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', note=note, user=current_user)