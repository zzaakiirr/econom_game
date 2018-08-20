import json


def load_json_data_from_json_package(file_name):
    try:
        with open(file_name) as f_obj:
            database = json.load(f_obj)
    except FileNotFoundError:
        database = {}
    return database


def load_json_data_to_json_package(file_name, data):
    with open(file_name, 'w') as f_obj:
        json.dump(data, f_obj)


def load_account_to_db(email, password):
    database_filename = 'accounts.json'
    accounts_database = load_json_data_from_json_package(database_filename)
    accounts_database[email] = password
    load_json_data_to_json_package(database_filename, accounts_database)
