class HeartRateMonitor:
    def __init__(self, time, voltage):
        self.timevals = time
        self.voltagevals = voltage

    def import_data():
        import csv
        with open('test_data1.csv','r') as my_data:
            csv_reader = csv.reader(my_data)

            for reading in my_data:
                time = reading[0]
                voltage = reading[1]

HeartRateMonitor.import_data()