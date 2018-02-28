filename = 'test_data1.csv'
def import_data():
    import csv
    with open(filename, 'r') as my_data:
        csv_reader = csv.reader(my_data)

        for reading in my_data:
            time = reading[0]
            voltage = reading[1]
    return time, voltage


class HeartRateData:
    def __init__(self, time, voltage):
        self.timevals = time
        self.voltagevals = voltage

    def visualize(self):
        import pandas
        import matplot.pyplot as pl


