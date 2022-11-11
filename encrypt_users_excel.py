import string
import pandas as pd
import yaml
import base64

with open('config.yml', 'r') as file:
    con = yaml.safe_load(file)
with open('users_format.txt', 'r+') as f:
    data = f.readlines()


def get_encrypted_users():
    user_details = pd.read_excel(con['workbook_path'])
    user_details[con['column_user_type']] = user_details[con['column_user_type']].str.strip()
    count = 0
    for value in con['excel_roles']:
        each_user_type = user_details[user_details[con['column_user_type']] == value]
        if len(each_user_type.index):
            each_user_type = each_user_type.filter([con['column_id'], con['column_username']])
            each_user_type.rename(columns={con['column_id']: 'id'}, inplace=True)
            each_user_type.rename(columns={con['column_username']: 'name'}, inplace=True)
            each_user_type.to_excel(f'{value}.xlsx', index=False)
            js = each_user_type.to_dict(orient='records')
            json_str = str(js).replace("'", "\"")
            data[
                count + 1] = f"   \"{con['default_roles'][count]}\":{json_str.translate(str.maketrans('', '', string.whitespace))},\n"

        count += 1
    data_str = ''.join(data)

    encoded_users = str(data_str).encode("UTF-8")
    base64_bytes = base64.b64encode(encoded_users)
    base64_string = base64_bytes.decode("UTF-8")
    return base64_string


if __name__ == "__main__":
    result = get_encrypted_users()
    with open('Test/test_decoded_json_manual.txt', 'r') as f:
        test_data_set = f.read()
    with open('Test/test_decoded_json_automate.txt', 'w') as f:
        f.write(result)

    if test_data_set == result:
        print('Automated and manual provide same results. Success !')
    else:
        print('Automation failed !')
