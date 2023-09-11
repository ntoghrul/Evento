# Evento (Event management system)

### Requirements

Creating a ticketing system for events. Events are scheduled by an event organiser and tickets are allocated to attendees. Events must have a name, date, time, duration, capacity and location. Attendees can view upcoming events and request a ticket for any that have available space. All users (organisers and attendees) need to login before they can change data on the website. However, the public can view events even if they are not logged in. The capacity or popularity of an event is never shown to attendees or the public unless there are fewer than 5% capacity available. In this case ‘last X spaces’ is shown in the list. An event would show ‘FULL’ if the tickets allocated is the same as the capacity. Every ticket that is allocated, will be given a unique value which can be view as a barcode.

Basic functionality is:
• User registration
o Must have two classes of user – organiser and attendee
o All users must provide a valid & verifiable email address and a
password
o Users must provide this 8-character code to register as an organiser
§ Dc5_G1gz
• User authentication
o Login with password
• Adding an event
o Only organisers can create events
o Organisers can promote an attendee’s class to organiser of an event
• Managing events
o Organisers can cancel an event, but they cannot change the date or time of an event; all attendees with tickets will be notified of any cancellation
o Organisers will be notified when an event is near capacity
• Ticket allocation
o Attendees can request a single ticket for an event in the future
o Attendees can cancel tickets for events in the future
• Viewing tickets
o Attendees can view ticket and barcode for each event for which they have tickets

A complete application:
• Implements the functionality of the basic specification above using Python,
Flask and Flask-SQLAlchemy with sqlite3.
• Make use of JavaScript to enhance the user experience.
• Have a consistent styling.
• Consider security issues.
• implements additional features.
