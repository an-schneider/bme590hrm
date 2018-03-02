# Set up logger
import logging
log_format = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='divlog.txt', format=log_format,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()

# Import necessary modules
try:
    import numpy
except ImportError:
    print('Please install numpy')
    logger.error('numpy not installed in virtual environment')
try:                                            # Comment out when testing
    import matplotlib.pyplot as plt             # Comment out when testing
except ImportError:                             # Comment out when testing
    print('Please install matplotlib')          # Comment out when testing
    logger.error('matplotlib not installed in virtual environment') # Comment out when testing
try:
    import scipy.signal
except ImportError:
    print('Please install scipy')
    logger.error('Scipy not installed in virtual environment')

# Specify the type of file being imported
# Options: .csv
file_type = '.csv'

# Insert desired file path and file name here
file_name = 'test_data1'
path = '/Users/AnthonySchneider/Desktop/bme590hrm/test_data/'
file = path + file_name + file_type
logger.info('Intended File Path: %s' % file)

# Insert the voltage units in the incoming file
VoltUnit = 'mV'
logger.info('Specified Units: %s' % VoltUnit)


def import_csv_data(import_file):
    """Import ECG voltage and times from a csv file

    :param: import_file: ECG reading time and voltages
    :returns: list of time values and list of voltage values
    """
    import csv
    with open(import_file, 'r') as my_data:
        csv_reader = csv.reader(my_data, delimiter=',')
        time = []
        voltage = []
        for n, reading in enumerate(csv_reader):
            time.append(float(reading[0]))
            voltage.append(float(reading[1]))
    return time, voltage


if file_type is '.csv':
    time, voltage = import_csv_data(file)
    logger.info('.CSV File Successfully Imported')
else:
    logger.error('Input file type not supported')
    raise TypeError('The input file type is not supported by this version of the software')


class HeartRateData:
    def __init__(self, time, voltage, voltmin=None, voltmax=None, units=None, num_beats=None, beat_times=None, duration=None, mean_hr_bpm=None):
        self.timevals = time
        self.voltagevals = voltage
        self.units = units
        self.num_beats = num_beats
        self.beat_times = beat_times
        self.duration = duration
        self.mean_hr_bpm = mean_hr_bpm
        self.voltmin = voltmin
        self.voltmax = voltmax

    def visualize(self):
        """Generates simple plot of raw ECG Data

        :param: self.timevals: list of times from imported file
        :param: self.voltagevals: list of voltages from imported file
        """

        # plt.plot(self.timevals, self.voltagevals)    # Comment out when testing
        # plt.xlabel('Time')                           # Comment out when testing
        # plt.ylabel('Voltage (%s)' % self.units)      # Comment out when testing
        # plt.show()                                   # Comment out when testing

    def autocorrelate(self):
        """Calculates autocorrelation of input data

        :param: self.voltagevals: list of voltages from imported file
        :returns: autocorrelated data
        """

        x = self.voltagevals
        autocorr = (numpy.correlate(x, x, mode='full'))
        autocorr = autocorr[len(autocorr)//2:]
        logger.info('Autocorrelation Complete')
        return autocorr

    def find_interval(self):
        """Finds interval between first two R peaks of QRS complex using autocorrelate method

        :param: self.voltagevals: list of voltages from imported file
        :returns: interval: interval in seconds between the first two R peaks
        """

        data = self.autocorrelate()
        data = data**2
        peaks_indices = scipy.signal.find_peaks_cwt(data, numpy.arange(5, 10), min_snr=2)
        max_values = []
        for n, i in enumerate(peaks_indices):
            max_values.append(data[i])

        # plt.plot(data)                                             # Comment out when testing
        # plt.scatter(peaks_indices, max_values,marker='x', c='red') # Comment out when testing
        # plt.show()                                                 # Comment out when testing

        # Time to second peak in autocorr rep. one period
        interval_time_index = peaks_indices[1]
        interval = self.timevals[interval_time_index]
        logger.info('Calculated time interval between R peaks: %s sec' % interval)
        return interval

    def count_beats(self):
        """Finds number of beats in the ECG and the times at which they occur.

        :param: interval: interval in seconds between the first two R peaks
        :param: self.voltagevals: list of voltages from imported file
        :param: self.timevals: list of times from imported file
        :returns: num_beats: number of beats counted in the ECG recording
        :returns: beats: array containing the times at which these beats occurred """

        interval_sec = self.find_interval()
        interval_indices = self.timevals.index(interval_sec)
        num_intervals = int(max(self.timevals)/interval_sec)

        # Create interval "search bins" in which to find local peaks
        bin_ends = []
        for i in range(1, num_intervals+1):
            bin_ends.append((i*interval_indices)-1)
        bin_ends.append(len(self.voltagevals))
        start = 0
        peak_val = []
        peak_val_index = []

        for n, i in enumerate(bin_ends):
            bin = self.voltagevals[start:i]
            peak_val.append(max(bin))
            peak_val_location = start + bin.index(peak_val[n])
            peak_val_index.append(peak_val_location)
            start = i+1

        peak_val_times = []
        for i in peak_val_index:
            peak_val_times.append(self.timevals[i])

        # Collect Desired Values
        num_beats = len(peak_val)
        beats = numpy.array(peak_val_times)
        self.num_beats = num_beats
        self.beat_times = beats
        print('Number of Beats Detected: %s' % num_beats)
        print('Times at which beats were detected: %s sec' % str(beats))
        logger.info('Number of beats detected: %s' % num_beats)
        logger.info('Times at which beats occurred: %s sec' % str(beats))

        # Graph each "search bin" and mark maxima
        # for i in range(1,num_intervals+1): Uncomment for visual representation of the 'bins'
        #    plt.axvline(i*interval_sec,c='red',)

        plt.plot(self.timevals, self.voltagevals)                   # Comment out when testing
        plt.xlabel('Time (sec)')                                    # Comment out when testing
        plt.ylabel('Voltage (%s)' % VoltUnit)                       # Comment out when testing
        plt.scatter(peak_val_times, peak_val, marker='x', c='red')  # Comment out when testing
        plt.grid()                                                  # Comment out when testing
        plt.title('ECG Reading: %s' % file_name+file_type)          # Comment out when testing
        plt.show()                                                  # Comment out when testing
        logger.info('Data plotted with marked peaks')
        return num_beats, beats

    def get_voltage_extremes(self):
        """ Finds the minimum and maximum lead voltages in the ECG recording

        :param: self.voltagevals: list of voltages from imported file
        :returns: voltage_extremes: minimum and maximum lead voltages"""

        min_voltage = min(self.voltagevals)
        max_voltage = max(self.voltagevals)
        voltage_extremes = (min_voltage, max_voltage)
        # Need to change the units depending on user input
        print('Minimum Lead Voltage: %s mV, Maximum Lead Voltage: %s mV' % voltage_extremes)
        logger.info('Minimum Lead Voltage: %s %s, Maximum Lead Voltage: %s %s' % (min_voltage, VoltUnit, max_voltage,
                                                                                  VoltUnit))
        self.voltmin = min_voltage
        self.voltmax = max_voltage
        return voltage_extremes

    def get_duration(self):
        """ Finds the time duration of the ECG recording

        :param: self.timevals: list of times from the input data
        :returns: time_duration: time duration of the ECG signal in seconds"""

        time_duration = max(self.timevals)
        self.duration = time_duration
        print('ECG Reading Duration: %s sec' % time_duration)
        logger.info('ECG Reading Duration: %s sec' % time_duration)
        return time_duration

    def get_mean_hr_bpm(self):
        """ Calculates heart rate of the sample data in beats per minute

        :param: self.num_beats: number of heartbeats contained in the ECG recording
        :param: self.duration: time duration of ECG recording
        :returns: avg_hr_bpm: calculated heart rate in beats per minute"""

        avg_hr_bps = self.num_beats/self.duration
        avg_hr_bpm = int(avg_hr_bps*60)
        self.mean_hr_bpm = avg_hr_bpm
        if avg_hr_bpm > 180:
            logger.warning('Heart rate is abnormally high (>180 BPM)')
        if avg_hr_bpm < 40:
            logger.warning('Heart rate is abnormally low (<40 BPM)')
        print('Average Heart Rate: %s BPM' % avg_hr_bpm)
        logger.info('Average Heart Rate: %s BPM' % avg_hr_bpm)
        return avg_hr_bpm

    def write_json(self, dictionary):
        """ Writes data outputs to json files

        :param: dictionary: dictionary containing the data to be written to a json file
        :returns: json file with the same name as the input file"""

        import json
        with open(path+file_name+'.json', 'w') as outfile:
            json.dump(dictionary, outfile)
        logger.info('Calculated data written to %s' % file_name+'.json')

    def main(self):
        num_beats, beats = self.count_beats()
        voltage_extremes = self.get_voltage_extremes()
        time_duration = self.get_duration()
        avg_hr_bpm = self.get_mean_hr_bpm()
        ECG_outputs = {"Mean Heart Rate BPM": avg_hr_bpm,
                       "Minimum Voltage (%s)" % self.units: voltage_extremes[0],
                       "Maximum Voltage (%s)" % self.units: voltage_extremes[1],
                       "Duration of Reading": time_duration,
                       "Number of Beats": num_beats,
                       "Beat Times": str(beats)}
        self.write_json(ECG_outputs)


DataSet = HeartRateData(time, voltage, units=VoltUnit)
DataSet.main()
