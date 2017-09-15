import json


def update_dict_rec(json_dict, data_dict, parent):
    for key, value in json_dict.items():
        if not isinstance(value, dict):
            key = parent + '.' + key if parent != '' else key
            data_dict[key].append(value)
        else:
            parent = parent + '.' + key if parent != '' else key
            update_dict_rec(value, data_dict, parent)
            roll_back = parent.rfind('.')
            parent = '' if roll_back == -1 else parent[:roll_back]


def update_dict(line, data_dict):
    json_dict = json.loads(line)
    update_dict_rec(json_dict, data_dict, parent='')


def file_to_dataframe(fp):
    from collections import defaultdict
    data_dict = defaultdict(list)
    i = 0
    for line in fp:
        update_dict(line, data_dict)
        i += 1
    return data_dict, i


def jsonl_to_json(data_loc, result_file_name='no_nesting_json.json'):
    print('Reading from the jsonl file...')
    with open(data_loc, 'r') as f:
        data_dict, n_lines = file_to_dataframe(f)
    # df.to_csv('json_to_csv.csv')
    print('Total records in the jsonl file: {0:d}'.format(n_lines))
    print('Writing to the json file...')
    with open(result_file_name, 'w') as f:
        json.dump(data_dict, f)
    return n_lines


if __name__ == '__main__':
    jsonl_to_json('input.jsonl')
