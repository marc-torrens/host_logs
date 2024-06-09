from Dataset import LogDataset

if __name__ == '__main__':
    log_data = LogDataset(txt_path='Data/input-file-10000.txt')
    connected_hostnames = log_data.connected_hostnames(hostname='Natoshia',
                                                       ini_timestamp=1565652284545, end_timestamp=1565716158982)
    print(connected_hostnames)