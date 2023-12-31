# -*- coding: utf-8 -*-
"""BlueJay.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dqGhAJaN2bJo9lUDlZDWIGMuHTi0Mijm
"""

import csv
from datetime import datetime, timedelta

def analyze_employee_data(input_file):

    consecutive_workdays = 7
    min_time_between_shifts = 1  # Minimum time between shifts in hours
    max_single_shift_duration = 14  # Maximum duration of a single shift in hours

    # Dictionary to store employee data
    employees = {}

    with open(input_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')  # Assuming tab-delimited file
        current_employee = None
        consecutive_days = 0
        last_shift_end = None

        for row in reader:
            # print(row)
            position = row.get('Position ID', '')
            position_status = row.get('Position Status', '')
            name = row.get('Employee Name', '')
            time_in_str = row.get('Time', '')
            time_out_str = row.get('Time Out', '')
            timecard_hours_str = row.get('Timecard Hours (as Time)', '')

            if not name:
                continue  # Skip rows without an employee name

            if not time_in_str or not time_out_str:
                print(f"Skipping row for {name} with missing time data")
                continue

            try:
                time_in = datetime.strptime(time_in_str, '%m/%d/%Y %I:%M %p')
                time_out = datetime.strptime(time_out_str, '%m/%d/%Y %I:%M %p')
            except ValueError:
                print(f"Skipping row for {name} with invalid time data")
                continue

            # Calculate shift duration in hours
            shift_duration = (time_out - time_in).total_seconds() / 3600

            # Check for consecutive workdays
            if name == current_employee:
                consecutive_days += 1
            else:
                current_employee = name
                consecutive_days = 1

            if consecutive_days == consecutive_workdays:
                print(f"{name} ({position}) has worked for 7 consecutive days starting on {time_in.date()}")

            # Check for time between shifts
            if last_shift_end is not None:
                time_between_shifts = (time_in - last_shift_end).total_seconds() / 3600
                if min_time_between_shifts < time_between_shifts < 10:
                    print(f"{name} ({position}) has less than 10 hours between shifts on {time_in.date()}")

            # Check for single shift duration
            if shift_duration > max_single_shift_duration:
                print(f"{name} ({position}) has worked for more than 14 hours on {time_in.date()}")

            last_shift_end = time_out

if __name__ == "__main__":
    input_file = 'employee_data.csv'  # Replace with the actual path to your input file
    analyze_employee_data(input_file)

