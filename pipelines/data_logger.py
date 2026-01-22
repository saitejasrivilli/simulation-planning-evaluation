class DataLogger:
    def __init__(self):
        self.data = []

    def log(self, record):
        self.data.append(record)

    def flush(self):
        return self.data
