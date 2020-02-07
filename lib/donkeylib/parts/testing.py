import statistics
from datetime import datetime
import pickle


class ConstantOutput:
    def __init__(self, value=0):
        self.value = value

    def run(self):
        return self.value


class OdomQuality:
    max = 0.
    min = 0.
    vals = []
    dts = []
    last_time = datetime.now()
    filename = f'{last_time.isoformat()}_odom_quality.pkl'
    save_file = None

    def __init__(self, save_file=False):
        self.save_file = save_file

    def run(self, val):
        if val < .05:
            return

        now = datetime.now()
        dt = now - self.last_time
        self.last_time = now
        self.dts.append(dt.total_seconds())
        self.vals.append(val)

        if val > self.max:
            self.max = val

        if val < self.min:
            self.min = val

    def shutdown(self):
        directory = 'quality'
        import os
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, self.filename), 'wb') as f:
            pickle.dump(self.vals, f)

        print('Variance is:', statistics.stdev(self.vals))
        print('dt variance is:', statistics.stdev(self.dts))
