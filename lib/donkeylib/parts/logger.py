
class ConsoleLogger:
    def __init__(self, interval=20):
        self.interval = interval
        self.count = 0

    def run(self, values):
        self.count += 1
        if self.count % self.interval == 0:
            print(values)