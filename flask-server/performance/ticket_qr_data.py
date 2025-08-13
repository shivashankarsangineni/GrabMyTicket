import json
import time

from performance.base import PerformanceBase


class PerformanceTicketQRData(PerformanceBase):
    def __init__(self):
        super().__init__()
        self.route_tested = '/ticket/request_qr_data'

    def run_test(self):
        self.response_times = []
        for i in range(1000):
            ticket_id = self.create_ticket()

            time0 = time.time()  # Start time

            # Ticket data
            ticket_data = {
                "ticket_id": ticket_id
            }

            # Post request
            response = self.user_client.post('/ticket/request_qr_data', data=json.dumps(ticket_data),
                                             content_type='application/json')

            time1 = time.time()  # End time
            self.response_times.append((time1 - time0) * 1000)  # in milliseconds

            assert response.status_code == 200


if __name__ == "__main__":
    performance_test = PerformanceTicketQRData()
    performance_test.run_test()
    performance_test.plot_graph()
    performance_test.drop_db()
