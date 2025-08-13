import json
import time

from performance.base import PerformanceBase


class PerformanceTicketValidate(PerformanceBase):
    def __init__(self):
        super().__init__()
        self.route_tested = '/ticket/validate'

    def generate_qr_data(self):
        # Create ticket
        ticket_id = self.create_ticket()

        # Ticket data
        ticket_data = {
            "ticket_id": ticket_id
        }
        qr_response = self.user_client.post('/ticket/request_qr_data', data=json.dumps(ticket_data),
                                            content_type='application/json')
        assert qr_response.status_code == 200

        return qr_response.json.get('qr_data')

    def run_test(self):
        self.response_times = []
        for i in range(1000):
            qr_data = self.generate_qr_data()

            time0 = time.time()  # Start time

            # Validate data
            validate_data = {
                "event_id": self.test_event_id,
                "qr_data": qr_data,
            }

            # Post request
            response = self.management_client.post('/ticket/validate', data=json.dumps(validate_data),
                                                   content_type='application/json')

            time1 = time.time()  # End time
            self.response_times.append((time1 - time0) * 1000)  # in milliseconds

            assert response.status_code == 200


if __name__ == "__main__":
    performance_test = PerformanceTicketValidate()
    performance_test.run_test()
    performance_test.plot_graph()
    performance_test.drop_db()
