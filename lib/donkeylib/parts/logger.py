import sys, json
from prettytable import PrettyTable


class ConsoleLogger:
    def __init__(self, interval=20, labels=[]):
        self.interval = interval
        self.labels = labels
        self.count = 0

    def run(self, *args):
        self.count += 1
        if self.count % self.interval == 0:
            t = PrettyTable()
            t.field_names = ['Key', 'Value']
            for i in range(len(args)):
                t.add_row([self.labels[i], args[i]])
            print(t)
