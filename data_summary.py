import json
import pandas as pd


def build_dict_of_series(fp):
    result = dict()
    data = json.load(fp)
    for key, value_list in data.items():
        result[key] = pd.Series(value_list)
    return result


def print_q1(fp):
    print('\n' * 2)
    print('Printing Q1:')
    data = json.load(fp)
    l = list(data.keys())
    l.sort()
    print(l)
    print('\n' * 2)


def print_q2(input_dict, nr_records):
    print('Printing Q2:')
    for key, value_series in input_dict.items():
        print('{0:s}: {1:.2f}%'.format(key, len(value_series) * 100 / nr_records))
        print(value_series.value_counts()[:5])
        print('\n')
    print('\n' * 2)


def print_q3_4(input_dict):
    print('Printing Q3 and Q4: Number of distinct first names and steet names:')
    for key, value_series in input_dict.items():
        if key in ('name.firstname', 'address.street'):
            print('{0:s}: {1:d}'.format(key, value_series.nunique()))
    print('\n' * 2)


def get_area_codes(phonenr):
    import regex
    pattern = r'\D'
    pieces = regex.split(pattern, phonenr)
    if len(pieces) is 1:
        # If no separators are present in the phone number, return the first 3 digits that are starting from the
        # first non 0, non 1 digits because area codes do not start with those digits
        pattern = r'[^01]'
        p = regex.search(pattern, pieces[0]).start()  # First non 0, non 1 digit
        return pieces[0][p:p + 3]
    else:
        for piece in pieces:
            if len(piece) is 3:
                return piece
    # If none of the above methods work, return the first 3 digits of the last piece if at least 3 digits exist
    return pieces[-1][:3] if len(pieces[-1]) >= 3 else '???'


def print_q5(input_dict, phone_nr_header='phone'):
    input_dict['area_code'] = input_dict[phone_nr_header].apply(get_area_codes)
    print('5 most common US area codes:')
    print(input_dict['area_code'].value_counts()[:5])


def main():
    import sys
    DATA_LOC = sys.argv[1] if len(sys.argv) > 1 else './201702/data/ida_wrangling_exercise_data.2017-02-13.jsonl'
    OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else 'no_nesting_json.json'

    from parse_json import jsonl_to_json
    n_records = jsonl_to_json(data_loc=DATA_LOC, result_file_name=OUTPUT_FILE)
    # n_records = 150000

    # Question 1:
    with open(OUTPUT_FILE, 'r') as f:
        print_q1(f)

    # Make a dict of pandas series to be used in the next questions
    with open(OUTPUT_FILE, 'r') as f:
        series_dict = build_dict_of_series(f)

    # Question 2:
    print_q2(series_dict, n_records)

    # Question 3, 4:
    print_q3_4(series_dict)

    # Question 5:
    print_q5(series_dict, phone_nr_header='phone')


if __name__ == '__main__':
    main()
