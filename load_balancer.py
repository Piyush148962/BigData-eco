import random
import time
from datetime import datetime, timedelta

class LoadBalancer:
    def __init__(self):
        self.servers = {
            'server_1': {'capacity': 1000, 'current_load': 0, 'status': 'healthy'},
            'server_2': {'capacity': 1000, 'current_load': 0, 'status': 'healthy'},
            'server_3': {'capacity': 1000, 'current_load': 0, 'status': 'healthy'},
            'server_4': {'capacity': 1000, 'current_load': 0, 'status': 'healthy'},
        }
        self.request_queue = []
        self.peak_hours = range(10, 20)  # 10 AM to 8 PM
    
    def simulate_requests(self, duration_minutes=60):
        results = []
        start_time = datetime.now()
        
        for minute in range(duration_minutes):
            current_time = start_time + timedelta(minutes=minute)
            current_hour = current_time.hour
            
            # Determine request rate based on time of day
            if current_hour in self.peak_hours:
                requests_this_minute = random.randint(800, 1200)
            else:
                requests_this_minute = random.randint(100, 400)
            
            # Add requests to queue
            self.request_queue.extend([{
                'id': f'req_{minute}_{i}',
                'timestamp': current_time,
                'type': random.choice(['page_view', 'add_to_cart', 'checkout', 'search'])
            } for i in range(requests_this_minute)])
            
            # Process requests
            processed = self.process_requests()
            
            # Update server statuses
            self.update_server_status()
            
            results.append({
                'minute': minute,
                'time': current_time.strftime('%H:%M'),
                'requests_received': requests_this_minute,
                'requests_processed': processed,
                'queue_length': len(self.request_queue),
                'server_loads': {server: data['current_load'] for server, data in self.servers.items()}
            })
        
        return results
    
    def process_requests(self):
        processed = 0
        for server_name, server_data in self.servers.items():
            if server_data['status'] == 'healthy':
                # Process up to 10% of capacity per minute
                max_process = min(server_data['capacity'] // 10, len(self.request_queue))
                if max_process > 0:
                    # Remove requests from queue
                    self.request_queue = self.request_queue[max_process:]
                    processed += max_process
                    # Increase server load
                    self.servers[server_name]['current_load'] += max_process
        
        return processed
    
    def update_server_status(self):
        for server_name, server_data in self.servers.items():
            # If server load exceeds 90% capacity, mark as stressed
            if server_data['current_load'] > server_data['capacity'] * 0.9:
                self.servers[server_name]['status'] = 'stressed'
            # If server load exceeds capacity, mark as overloaded
            elif server_data['current_load'] > server_data['capacity']:
                self.servers[server_name]['status'] = 'overloaded'
                # Reduce load by 20% (simulating auto-scaling or load shedding)
                self.servers[server_name]['current_load'] *= 0.8
            else:
                self.servers[server_name]['status'] = 'healthy'
            
            # Gradually decrease load (simulating request completion)
            self.servers[server_name]['current_load'] *= 0.95
    
    def get_server_status(self):
        return self.servers