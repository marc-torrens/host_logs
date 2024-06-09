from typing import List
from bisect import bisect_left, bisect_right

class LogLine:
    def __init__(self, line: str):
        elements = line.split(' ')
        if len(elements) != 3:
            raise ValueError(f"Invalid line format: '{line}'")
        try:
            self.timestamp = int(elements[0])
        except ValueError:
            raise ValueError(f"Bad format timestamp: '{elements[0]}'")

        self.from_hostname = elements[1]
        self.to_hostname = elements[2]

    # Sort LogLines by their timestamps
    def __lt__(self, other: 'LogLine'):
        return self.timestamp < other.timestamp

class LogsDatasetIterator(object):
    def __init__(self, logs):
        self.idx = 0
        self.logs = logs
    def __iter__(self):
        return self
    def __next__(self):
        if self.idx < len(self.logs):
            result = self.logs[self.idx]
            self.idx += 1
            return result
        else:
            raise StopIteration # Done iterating.


class LogDataset:
    def __init__(self, txt_path: str):
        # Read data from the text file
        with open(txt_path, 'r') as f:
            # List of lines
            lines = f.read().split('\n')
            # Split elements of the line (3 elements)
            logs = []
            # Validate data
            for i,line in enumerate(lines):
                try:
                    logline = LogLine(line)
                    logs.append(logline)
                except ValueError as e:
                    print(f"Line {i} is invalid: Line skipped {e}")
            self.logs = logs
            # Sort logs
            self.sort()
    
    def __iter__(self):
        return LogsDatasetIterator(self.logs)

    
    def sort(self):
        # Logs are sorted by timestamp
        #TODO: Can be optimized with the Assumption that logs are previously sorted with an error of max 5 min
        self.logs = sorted(self.logs)
    
    def connected_hostnames(self, hostname:str, ini_timestamp: int, end_timestamp: int) -> List[str]:
        # Check all hostnames connected to a hostname during a period of time

        # Find the left and right indices of the timestamp (>= and <=)
        left_index = bisect_left(self.logs, LogLine(f"{ini_timestamp} from to"))
        right_index = bisect_right(self.logs, LogLine(f"{end_timestamp} from to"))
        # Obtain the list of hostnames connected to the given host
        connected_hostnames = set()
        for logline in self.logs[left_index:right_index]:
            if logline.from_hostname == hostname:
                connected_hostnames.add(logline.to_hostname)
        return list(connected_hostnames)