

filename = '/Users/AnthonySchneider/Desktop/bme590hrm/test_data/test_data12.csv'


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
        x = self.voltagevals
        autocorr = (numpy.correlate(x, x, mode='full'))
        autocorr_sqd = autocorr**2
        autocorr_sqd = autocorr_sqd[len(autocorr_sqd)//2:]

        return autocorr_sqd

    def find_interval(self):
        import numpy
        import matplotlib.pyplot as plt
        import peakutils
        import scipy.signal
        data = self.autocorrelate()
        peaks_indices = scipy.signal.find_peaks_cwt(data,numpy.arange(5,10),min_snr=4)
        max_values = []
        for n,i in enumerate(peaks_indices):
           max_values.append(data[i])
        plt.plot(data)
        plt.scatter(peaks_indices, max_values,marker='x', c='red')
        plt.show()
        # Time to second peak in autocorr rep. one period
        interval_time_index = peaks_indices[1]
        interval = self.timevals[interval_time_index]
        print(interval)





Data1 = HeartRateData(time, voltage)
Data1.visualize()
Data1.autocorrelate()
Data1.find_interval()





