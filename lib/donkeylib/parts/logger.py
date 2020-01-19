
class ConsoleLogger:
    def __init__(self, interval=20, labels=[]):
        self.interval = interval
        self.labels = labels
        self.count = 0

    def run(self, *args):
        self.count += 1
        v = zip(self.labels, args)
        if self.count % self.interval == 0:
            print(dict(v))