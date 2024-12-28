import os
import time

def get_events(fortnite_username):
    # TODO: Handle multiple languages
    return {
        "kill": [f"<LocalKiller>{fortnite_username}"],
        "death": [f"<TeamVictim>{fortnite_username}", "éliminé"],
        "ko": [f"<TeamVictim>{fortnite_username}", "K.-O."],
    }

class FortniteConnector:
    def __init__(self, log_file_path, fortnite_username):
        """
        Initialize the FortniteConnector object.

        :param log_file_path: The path to the log file to monitor.
        :param fortnite_username: The Fortnite username of the player.
        """
        self.log_file_path = log_file_path
        self.last_read_position = os.path.getsize(log_file_path) if os.path.exists(log_file_path) else 0
        self.fortnite_username = fortnite_username
        self.on_events_functions = {}



    def monitor_logs(self):
        """
        Monitor the log file for events and call the corresponding functions.
        """
        events = get_events(self.fortnite_username)
        while True:
            if os.path.exists(self.log_file_path):
                with open(self.log_file_path, "r", encoding="utf-8") as file:
                    file.seek(self.last_read_position)  
                    new_lines = file.readlines()
                    self.last_read_position = file.tell() 

                    for line in new_lines:
                        for event_name, function_to_call in self.on_events_functions.items():
                            if all(keyword in line for keyword in events[event_name]):
                                print(f"Event detected: {event_name}", line)
                                function_to_call()
                        
            time.sleep(0.1) 
