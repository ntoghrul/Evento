from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import User, OrganizerEvent, Event, Ticket
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db,login_manager, mail
from datetime import datetime
import random, string
from flask_mail import Message
import time

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    events = Event.query.all()
    return render_template('home.html', events=events)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist, please try again or register for an account.', category='error')

    return render_template('login.html',user=current_user)



@views.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        organizer_code = request.form.get('organizer_code')


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='error')
        elif password != password2:
            flash('Passwords don\'t match', category='error')
        
        elif not organizer_code:
         # User is registering as attendee
            new_user = User(firstname=first_name, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

        elif organizer_code != 'Dc5_G1gz':
            flash('Organizer code is incorrect', category='error')

        else:
         # User is registering as an organizer
            new_user = User(firstname=first_name, email=email, password=generate_password_hash(password, method='sha256'), is_organizer=True)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    


    return render_template('register.html')


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@views.route('/ticket-buy/<int:event_id>', methods=['POST'])
@login_required
def ticket_buy(event_id):
    # Getting the current user object
    user = current_user

    # Getting the event object
    event = Event.query.get_or_404(event_id)

    # Checking if the event is sold out
    if len(event.tickets) >= event.capacity:
        flash('Sorry, this event is sold out', 'warning')
        return redirect(url_for('views.events', event_id=event_id))


    # Generating a random barcode for the ticket
    barcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    # Creating a new ticket object and add it to the database
    ticket = Ticket(barcode=barcode, attendee_id=user.id, event_id=event_id)
    db.session.add(ticket)
    db.session.commit()

    flash('Ticket purchased successfully', 'success')

    # Checking if the event is near capacity
    tickets_sold = len(event.tickets)
    capacity = event.capacity
    percentage_left = (capacity - tickets_sold) / capacity
    if percentage_left <= 0.1:
        # Sending notification to event organizer
        organizers = User.query.filter_by(is_organizer=True).all()
        for organizer in organizers:
            msg = Message('Event Near Capacity', recipients=[organizer.email])
            msg.body = "Dear {name},\n\nThe event '{title}' is almost sold out. Only {percentage:.2%} of tickets are left.\n\nRegards,\nThe Evento Team".format(name=organizer.firstname, title=event.title, percentage=percentage_left)
            mail.send(msg)

    return redirect(url_for('views.events', event_id=event_id))





@views.route('/attendee')
@login_required
def attendee():
    if  current_user.is_organizer:
        attendees = User.query.filter_by(is_organizer=0).all()
        return render_template('attendee.html', attendees=attendees)


@views.route('/organize-event', methods=['GET', 'POST'])
@login_required
def organize_event():
    if request.method == 'POST':
        # getting form data
        title = request.form['title']
        description = request.form['description']
        venue = request.form['venue']
        date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        capacity = int(request.form['capacity'])

        # creating new event object
        event = Event(title=title, description=description, venue=venue, date=date, capacity=capacity)
        db.session.add(event)
        db.session.commit()

        # creating OrganizerEvent object to establish many-to-many relationship
        organizer_event = OrganizerEvent(organizer_id=current_user.id, event_id=event.id)
        db.session.add(organizer_event)
        db.session.commit()

        # redirecting to home page
        return redirect(url_for('views.home'))

    return render_template('organize_event.html')



@views.route('/my-tickets')
@login_required
def my_tickets():
    # Getting the current user's tickets
    tickets = current_user.tickets

    # Rendering the template and pass in the tickets
    return render_template('my_tickets.html', tickets=tickets)


@views.route('/ticket/cancel/<int:ticket_id>', methods=['POST'])
@login_required
def ticket_cancel(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Your ticket has been cancelled', 'success')
    return redirect(url_for('views.my_tickets'))




@views.route('/events/<int:event_id>')
def events(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event.html', event=event)


@views.route('/events/<int:event_id>/cancel', methods=['POST'])
@login_required
def event_cancel(event_id):
    event = Event.query.get_or_404(event_id)

    # sending email to all attendees
    tickets = Ticket.query.options(db.joinedload(Ticket.attendee)).filter_by(event_id=event_id).all()
    attendees = [ticket.attendee for ticket in tickets]
    

    for attendee in attendees:
        msg = Message('Event Canceled', recipients=[attendee.email])
        msg.body = "Dear {name},\n\nThe event '{title}' has been canceled.\n\nRegards,\nThe Evento Team".format(name=attendee.firstname, title=event.title)
        mail.send(msg)

        



    # Deleting all associated tickets before deleting the event
    for ticket in event.tickets:
        db.session.delete(ticket)


    db.session.delete(event)
    db.session.commit()
    flash('Event cancelled successfully', 'success')
    return redirect(url_for('views.home'))




@views.route('/make-organizer/<int:attendee_id>', methods=['POST'])
@login_required
def make_organizer(attendee_id):
    if current_user.is_organizer:
        attendee = User.query.get_or_404(attendee_id)
        attendee.is_organizer = 1
        db.session.commit()
        flash('{} is now an organizer!'.format(attendee.firstname), 'success')
        return redirect(url_for('views.attendee'))


@views.route('/ticket-validation', methods=['GET', 'POST'])
def ticket_validation():
    if request.method == 'POST':
        barcode = request.form.get('barcode')
        ticket = Ticket.query.filter_by(barcode=barcode).first()
        if ticket:
            flash('Ticket is valid', 'success')
        else:
            flash('The ticket is not valid', 'danger')
            
    return render_template('validation.html')

   

