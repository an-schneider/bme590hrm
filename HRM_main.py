filename = '/Users/AnthonySchneider/Desktop/bme590hrm/test_data/test_data3.csv'


def import_csv_data(filename):
    import csv
    import matplotlib.pyplot as plt
    with open(filename, 'r') as my_data:
        csv_reader = csv.reader(my_data, delimiter=',')
        time = []
        voltage = []
        for n, reading in enumerate(csv_reader):
            time.append(float(reading[0]))
            voltage.append(float(reading[1]))
    return time, voltage

time, voltage = import_csv_data(filename)

class HeartRateData:  # remember to have option to set units
    def __init__(self, time, voltage):
        self.timevals = time
        self.voltagevals = voltage

    def visualize(self):
        import matplotlib.pyplot as plt
        plt.plot(self.timevals, self.voltagevals)
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.show()

    def autocorrelate(self):
        import numpy
        import matplotlib.pyplot as plt
        import peakutils
        import scipy.signal
        t = 1
        x = self.voltagevals
        autocorr = (numpy.correlate(x, x, mode='full'))
        autocorr_amplified = autocorr**2
        half_corr = autocorr_amplified[autocorr_amplified.size // 2:]
        plt.plot(half_corr)
        plt.show()


Data1 = HeartRateData(time,voltage)
Data1.autocorrelate()
Data1.visualize()





