import json

import pandas as pd
import yaml
import base64

with open('config.yml', 'r') as file:
    con = yaml.safe_load(file)
with open('users_format.txt', 'r+') as f:
    # data = json.load(f)
    data = f.readlines()

def decompose_excel():
    user_details = pd.read_excel(con['workbook_path'])
    user_details[con['column_user_type']] = user_details[con['column_user_type']].str.strip()
    count = 0
    for value in con['excel_roles']:
        each_user_type = user_details[user_details[con['column_user_type']] == value]
        # print(len(each_user_type.index))
        if len(each_user_type.index):
            each_user_type = each_user_type.filter([con['column_id'], con['column_username']])
            each_user_type.rename(columns={con['column_id']: con['wanted_format_columns'][0]}, inplace=True)
            each_user_type.rename(columns={con['column_username']: con['wanted_format_columns'][1]}, inplace=True)
            each_user_type.to_excel(f'{value}.xlsx', index=False)
            js = each_user_type.to_dict(orient='records')
            data[count+1] = f"   \"{con['default_roles'][count]}\":{js},\n"

            # data[con['default_roles'][count]] = js
        count += 1

    with open('Test/test_json.txt', 'w') as f:
        f.writelines(data)

    encoded_users = str(data).encode("UTF-8")
    base64_bytes = base64.b64encode(encoded_users)
    base64_string = base64_bytes.decode("UTF-8")
    return base64_string



if __name__ == "__main__":
    print(decompose_excel())
