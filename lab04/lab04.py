from dataclasses import dataclass
from abc import ABC, abstractmethod
import argparse
import csv
from typing import List, Generator, Iterator
from prettytable import PrettyTable


@dataclass
class CarPassport:
    FIELDNAMES = ['№', 'дата и время', 'номерной знак', 'марка автомобиля']

    number: int
    date_time: str
    number_plate: str
    brand: str

    def __getattr__(self, item):
        if item == self.FIELDNAMES[0]:
            return self.number
        elif item == self.FIELDNAMES[1]:
            return self.date_time
        elif item == self.FIELDNAMES[2]:
            return self.number_plate
        elif item == self.FIELDNAMES[3]:
            return self.brand
        else:
            raise AttributeError

    def __str__(self):
        return '#{number}: {brand} {number_plate} at {date_time}'.format(
            number=self.number,
            brand=self.brand,
            number_plate=self.number_plate,
            date_time=self.date_time,
        )


class DataLoader(ABC):
    @abstractmethod
    def load(self) -> Generator[CarPassport, None, None]:
        raise NotImplementedError


class BaseDumper(ABC):
    @abstractmethod
    def dump(self, data: Iterator):
        raise NotImplementedError


class CarsList:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.data = []
        self.index = {}
        self.load_data()

    def load_data(self):
        for row in self.data_loader.load():
            self.data.append(row)
        self._reindex()

    def sort(self, field):
        self.data.sort(key=lambda x: getattr(x, field))
        self._reindex()

    def filter(self, field, value):
        self.data = [d for d in self.data if getattr(d, field) == value]
        self._reindex()

    def _reindex(self):
        self.index = {int(item.number): k for k, item in enumerate(self.data)}

    def out(self, dumper: BaseDumper):
        dumper.dump(self)

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self) -> CarPassport:
        if self.current >= len(self.data):
            raise StopIteration
        else:
            result = self.data[self.current]
            self.current += 1
            return result

    def __getitem__(self, number) -> CarPassport:
        if number in self.index:
            return self.data[self.index[number]]
        else:
            raise AttributeError


class CSVDataLoader(DataLoader):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def load(self) -> Generator[CarPassport, None, None]:
        fieldnames = CarPassport.FIELDNAMES
        with open(self.file_name, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield CarPassport(row[fieldnames[0]], row[fieldnames[1]], row[fieldnames[2]], row[fieldnames[3]])


class CsvFileDumper(BaseDumper):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def dump(self, data: CarsList):
        with open(self.file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CarPassport.FIELDNAMES)
            writer.writeheader()
            for row in data:
                writer.writerow(dict(zip(CarPassport.FIELDNAMES, [str(row.number), row.date_time, row.number_plate, row.brand])))


class TableDumper(BaseDumper):
    def dump(self, data: CarsList):
        table = PrettyTable()
        table.field_names = CarPassport.FIELDNAMES
        for passport in data:
            table.add_row([passport.number, passport.date_time, passport.number_plate, passport.brand])
        print(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--csv', type=str, required=True, help='data.csv file path')
    parser.add_argument('--sort', type=str, help='sort by field')
    parser.add_argument('--filter', type=str, help='filter by field')
    parser.add_argument('--value', type=str, help='filter by value')
    parser.add_argument('--get', type=int, help='get item by its number')
    parser.add_argument('--out', type=str, help='output file path')
    args = parser.parse_args()

    reader = CSVDataLoader(args.csv)
    data_list = CarsList(reader)

    if args.filter and args.value:
        data_list.filter(args.filter, args.value)
        print(f'Filtered by {args.filter} = {args.value}:')

    if args.sort:
        data_list.sort(args.sort)
        print(f'Sorted by {args.sort}:')

    printer = TableDumper()
    data_list.out(printer)

    if args.out:
        print(f'Write data into outfile {args.out}')
        writer = CsvFileDumper(args.out)
        data_list.out(writer)

    if args.get:
        print(f'Data item by the number #{args.get}:')
        print(data_list[args.get])
