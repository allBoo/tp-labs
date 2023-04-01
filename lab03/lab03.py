import argparse
import os
import csv
from prettytable import PrettyTable


FIELDNAMES = ['№', 'дата и время', 'номерной знак', 'марка автомобиля']
INDEX_FIELD = '№'


def count_files_in_directory(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def read_data_csv(file_path):
    data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data[row[INDEX_FIELD]] = row
    return data


def sort_data(data, sort_field):
    sorted_data = sorted(data.items(), key=lambda x: x[1][sort_field])
    return dict(sorted_data)


def filter_data(data, filter_field, filter_value):
    filtered_data = {k: v for k, v in data.items() if v[filter_field] == filter_value}
    return filtered_data


def write_data_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in data.values():
            writer.writerow(row)


def print_table(data):
    table = PrettyTable()
    table.field_names = FIELDNAMES
    for item in data.values():
        table.add_row(item.values())
    print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--dir', type=str, help='directory path')
    parser.add_argument('--csv', type=str, help='data.csv file path')
    parser.add_argument('--sort', type=str, help='sort by field')
    parser.add_argument('--filter', type=str, help='filter by field')
    parser.add_argument('--value', type=str, help='filter by value')
    parser.add_argument('--out', type=str, help='output file path')
    args = parser.parse_args()

    if args.dir:
        count = count_files_in_directory(args.dir)
        print(f'Number of files in {args.dir}: {count}')

    if args.csv:
        data = read_data_csv(args.csv)
        if args.filter and args.value:
            filtered_data = filter_data(data, args.filter, args.value)
            print(f'Filtered by {args.filter} = {args.value}:')
            data = filtered_data

        if args.sort:
            sorted_data = sort_data(data, args.sort)
            print(f'Sorted by {args.sort}:')
            data = sorted_data

        print_table(data)

        if args.out:
            print(f'Write data into outfile {args.out}')
            write_data_csv(args.out, data)
