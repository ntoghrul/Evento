!IMPORTANT


Somehow, ./setup.sh does not help to run application.To run this application on your DCS machine, follow the steps:
1. Go the project folder, which is coursework-3 in our case.
2. Run the following commands:
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt
6. python3.6 main.py -- for DSC machine or python3 main.py -- any other machine.

I don't know why it does not run with python3 main.py, hence, for DCS machine use python3.6 main.py.


You should now be able to access the application by navigating to http://localhost:5000 in your web browser.

1.User registration and login: Users can register for an account with a unique email address and password, or they can log in to an existing account.

Attendee home page: Once logged in, attendees are directed to a home page that displays upcoming events. They can view details about each event and buy tickets.

Organizer home page: Organizers can create new events, view their  events, and see a list of attendees.

Event creation: Organizers can create new events by providing a title, description, venue, date, and capacity.

Event details: Users can view detailed information about each event, including the title, description, venue, and date.

Ticket purchasing: Attendees can purchase tickets for events through the application. Each ticket has a unique barcode (string).


Ticket validation: Tickets can be validated using the barcode. The application will verify that the ticket is valid or not.

User management: Organizers can view a list of attendees and promote the attendee as an organizer.


Error handling: The application includes error handling to prevent users from entering invalid input or performing unauthorized actions.

Styling: The application has a clean and modern design with consistent styling throughout all pages.

