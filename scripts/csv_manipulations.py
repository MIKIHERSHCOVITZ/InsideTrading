# scripts/csv_manipulations.py

import csv

def write_to_csv(filename, data):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f'An error occurred while writing to CSV: {e}')

# Additional functions for reading and manipulating CSV files
