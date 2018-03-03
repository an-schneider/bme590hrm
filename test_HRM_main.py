def test_HRM_main():
    import numpy
    import scipy
    import pytest
    import HRM_main

    # Test import_csv_data
    from HRM_main import import_csv_data
    file_path = '/Users/AnthonySchneider/Desktop/' \
                'bme590hrm/test_data/test_data2.csv'
    time, voltage = import_csv_data(file_path)
    assert time[1] == 0.003
    assert voltage[1] == -0.345

    # Test class modules
    file_path = '/Users/AnthonySchneider/Desktop/' \
                'bme590hrm/test_data/test_data1.csv'
    time, voltage = import_csv_data(file_path)
    test_data = HRM_main.HeartRateData(time, voltage)

    # Test find_interval
    assert test_data.find_interval() == 0.800

    # Test count_beats
    test_data.count_beats()
    assert test_data.num_beats == 35

    # Test get_voltage_extremes
    test_data.get_voltage_extremes()
    assert test_data.voltmax == 1.05        # Determined from excel sheet
    assert test_data.voltmin == -0.68       # Determined from excel sheet

    # Test get_duration
    test_data.get_duration()
    assert test_data.duration == 27.775     # Determined from excel sheet

    # Test get_mean_hr_bpm
    beats_counted = 35
    duration_sec = 27.775
    average_bpm = int((beats_counted/duration_sec)*60)
    test_data.get_mean_hr_bpm()
    assert test_data.mean_hr_bpm == average_bpm

    # Test write_json
    import json
    my_dictionary = {"Name": "Anthony Schneider",
                     "NetID": "ans52",
                     "Major": "Biomedical Engineering"}
    test_data.write_json(my_dictionary)

    json_read = json.load(open('test_data/test_data1.json'))
    assert json_read == my_dictionary 