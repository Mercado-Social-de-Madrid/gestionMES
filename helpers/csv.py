import codecs
import csv


def csv_value_to_boolean(value):
    return value == 'true' or value == 'si' or value == '1' or value == 1 or value == 'verdadero'


def csv_missing_fields(file, required_fields):
    reader = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=';')
    header = next(reader)

    missing_headers = []
    for field in required_fields:
        if not field in header:
            missing_headers.append(field)

    return  missing_headers if len(missing_headers) > 0 else False