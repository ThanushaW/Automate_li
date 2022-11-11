import encrypt_users_excel
import base64


def edit_specific_li(li_path):
    with open(li_path, 'r') as f:
        encrypted_li = f.read()
    base64_bytes = encrypted_li.encode('UTF-8')
    message_bytes = base64.b64decode(base64_bytes)
    decrypted_li = message_bytes.decode('UTF-8')
    print(decrypted_li)


if __name__ == "__main__":
    edit_specific_li('Li/EIP/li.cab')
