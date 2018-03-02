

filename = '/Users/AnthonySchneider/Desktop/bme590hrm/test_data/test_data5.csv'


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
        return interval

    def count_beats(self):
        import matplotlib.pyplot as plt

        interval_sec = self.find_interval()
        interval_indices = self.timevals.index(interval_sec)
        num_intervals = int(max(self.timevals)/interval_sec)

        # Create interval "search bins" to find peaks
        bin_ends = []
        for i in range(1,num_intervals+1):
            bin_ends.append((i*interval_indices)-1)

        start = 0
        peak_val = []
        peak_val_index= []

        for n,i in enumerate(bin_ends):
            bin = self.voltagevals[start:i]
            peak_val.append(max(bin))
            peak_val_location = start + bin.index(peak_val[n])
            peak_val_index.append(peak_val_location)
            start = i+1

        peak_val_times = []
        for i in peak_val_index:
            peak_val_times.append(self.timevals[i])

        # Graph each "search bin" and mark maxima
        for i in range(1,num_intervals+1):
            plt.axvline(i*interval_sec,c='red')
        plt.plot(self.timevals, self.voltagevals)
        plt.scatter(peak_val_times, peak_val, marker='x', c='red')
        plt.show()








Data1 = HeartRateData(time, voltage)
Data1.visualize()
Data1.count_beats()





