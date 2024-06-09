import unittest
from src.Dataset import LogLine, LogDataset

class TestLogLines(unittest.TestCase):
    # Test invalid log lengths
    def test_valid_length(self):
        # Check exception raises in bad log lines cases
        with self.assertRaises(ValueError):
            LogLine("")
        with self.assertRaises(ValueError):
            self.assertRaises(LogLine("143920 a"), ValueError)
        # Check good log lines
        LogLine("402310 Madrid Paris")
    
    # Test invalid timestamp formats
    def test_valid_timestamp(self):
        LogLine("10821801 Barcelona Rome")
        # Check exception raises in bad timestamp cases
        with self.assertRaises(ValueError):
            LogLine("sldcn Barcelona Rome")

class TestLogDataset(unittest.TestCase):
    # Test read of logs
    def test_log_dataset_read(self):
        logs_test = """18181839 London Paris
20824292 Bilbao Touluse
24879237 Viena Prague
adaw Mars John"""
        with open('tests/test_log_file.txt', 'w') as f:
            f.write(logs_test)

        dataset = LogDataset('tests/test_log_file.txt')
        # 3 log lines since last one is invalid
        self.assertEqual(len(dataset.logs), 3)

    # Test sorting
    def test_log_dataset_sort(self):
        logs_test = """18181839 London Paris
31218962 Bilbao Touluse
31218962 Viena Prague
137248 Mars John
109249 July Poly"""
        with open('tests/test_log_file.txt', 'w') as f:
            f.write(logs_test)

        dataset = LogDataset('tests/test_log_file.txt')
        # Sorted dataset
        timestamps_dataset = [log.timestamp for log in dataset]
        self.assertEqual(timestamps_dataset, [109249, 137248, 18181839, 31218962, 31218962])

    # Test logs connected to hosts in time interval
    def test_connected_hostnames(self):
        # Write test log data to a file
        log_data = """18141239 London Paris
18151539 Aron Dine
18151839 Dine John
18161839 Dine Buenos_aires
18181839 Dine Mark"""
        with open('test_log_file.txt', 'w') as f:
            f.write(log_data)

        dataset = LogDataset('test_log_file.txt')
        connected_hosts = dataset.connected_hostnames('Dine', 18151539, 18171839)
        self.assertEqual(sorted(connected_hosts), sorted(['John', 'Buenos_aires']))

if __name__ == '__main__':
    unittest.main()