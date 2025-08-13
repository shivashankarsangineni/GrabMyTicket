import json
from datetime import datetime
from werkzeug.security import generate_password_hash
import numpy as np
import matplotlib.pyplot as plt

from app import create_app
from exts import db
from models import User, Venue, Event, UserTicket

USER = {
    "email_address": "test@test.com",
    "password": "test1234",
    "phone_number": "12345",
    "role": "user",
}

MANAGEMENT = {
    "email_address": "admin@test.com",
    "password": "test1234",
    "phone_number": "12346",
    "role": "management",
}


def login(client, email_address, password):
    data = {
        "email_address": email_address,
        "password": password
    }
    response = client.post('/user/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200


class PerformanceBase:
    def __init__(self):
        # Performance
        self.route_tested = None
        self.response_times = []

        # App
        self.app = create_app('config.TestConfig')

        # User
        self.user_client = self.app.test_client()
        self.user_client.testing = True

        # Management
        self.management_client = self.app.test_client()
        self.management_client.testing = True

        # Database
        with self.app.app_context():
            db.create_all()

            # Create accounts
            for user in [USER, MANAGEMENT]:
                self.test_user = User(
                    email_address=user.get('email_address'),
                    passwd_hash=generate_password_hash(user.get('password'), method="sha256", salt_length=32),
                    firstname='Test',
                    surname='Test',
                    date_of_birth=datetime.strptime('2000-01-01', "%Y-%m-%d").date(),
                    postcode='AB12 3DC',
                    phone_number=user.get('phone_number'),
                    role=user.get('role'),
                )
                self.test_user.save()

                if user == USER:
                    self.test_user_id = self.test_user.user_id

            # Create venue
            self.venue = Venue(
                name='Test',
                location='Test',
                postcode='Test',
                capacity=5000,
            )

            # Create event
            self.test_event = Event(
                venue=self.venue,
                event_name='Test event',
                datetime=datetime.now(),
                genre='Test',
                description='Test',
            )

            # Save venue and event
            self.venue.save()
            self.test_event.save()
            self.test_event_id = self.test_event.event_id

            # Login as user and management
            self.login_user()
            self.login_management()

    def login_user(self):
        login(self.user_client, USER.get('email_address'), USER.get('password'))

    def login_management(self):
        login(self.management_client, MANAGEMENT.get('email_address'), MANAGEMENT.get('password'))

    def create_ticket(self):
        with self.app.app_context():
            test_ticket = UserTicket(
                event_id=self.test_event_id,
                user_id=self.test_user_id,
                ticket_type="Standard",
                valid=True,
            )
            test_ticket.save()
            ticket_id = test_ticket.ticket_id
        return ticket_id

    def plot_graph(self):
        # Calculate average
        avg_response_time = np.mean(self.response_times)

        # Plot the results as a line graph
        x = range(1, 1001)  # Number of response time measurements
        y = self.response_times
        plt.plot(x, y)

        # Plot the average as a red line and annotate its value
        plt.axhline(y=avg_response_time, color='r', linestyle='--')
        plt.annotate(f'Average: {avg_response_time:.2f} ms', xy=(0.5, avg_response_time), xytext=(5, -10),
                     textcoords='offset points', ha='center', color='r')

        plt.xlabel('Run')
        plt.ylabel('Response time (ms)')
        if self.route_tested:
            plt.title(f"Performance of '{self.route_tested}' route")
        plt.show()

    def drop_db(self):
        with self.app.app_context():
            db.drop_all()
