import json
import time

from performance.base import PerformanceBase


class PerformanceTicketAdd(PerformanceBase):
    def __init__(self):
        super().__init__()
        self.route_tested = '/ticket/add'

    def run_test(self):
        self.response_times = []
        for i in range(1000):
            time0 = time.time()  # Start time

            # Get request
            token_response = self.user_client.get('/ticket/add')

            # Request data
            ticket_data = {
                "event_id": self.test_event_id,
                "ticket_type": "Standard",
                "token": token_response.json.get('key'),
                "ticket_quantity": 1,
            }

            # Post request
            response = self.user_client.post('/ticket/add', data=json.dumps(ticket_data),
                                             content_type='application/json')

            time1 = time.time()  # End time
            self.response_times.append((time1 - time0) * 1000)  # in milliseconds

            assert response.status_code == 200


if __name__ == "__main__":
    performance_test = PerformanceTicketAdd()
    performance_test.run_test()
    performance_test.plot_graph()
    performance_test.drop_db()
