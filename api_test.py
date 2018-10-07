import base64
import json
import time

import requests


def authentication():
    url = 'http://188.18.13.78:9000/api/m/account/dev'
    data = {"devType": "A", "pushToken": "firebaseSecretToken", "brand": 'YIT'}

    r = requests.post(url, data=data)

    # Лучше упасть с ошибкой сейчас, если код ответа не 200, чем что-нибудь отвалится потом из-за отсутствующего токена
    r.raise_for_status()

    response_content = json.loads(r.text)
    token = response_content['auth_Token']
    token_b64 = base64.b64encode(token.encode())

    return token_b64, str(r.status_code)


def set_phone_number(test=False):
    token_b64 = authentication()[0]
    url = 'http://188.18.13.78:9000/api/m/account/phone'
    headers = {'Authorization': 'basic ' + token_b64.decode("utf-8")}
    data = {"phone": "9125212573"}

    r = requests.post(url, headers=headers, data=data)

    r.raise_for_status()

    if test:
        # Кейс с верным ответом, без таймаута
        time.sleep(200)
        r = requests.post(url, headers=headers, data=data)

        r.raise_for_status()
        error_code = str(json.loads(r.text)['errorCode'])
        assert error_code == '1', 'Function "set_phone_number" returns wrong error code: ' + error_code

        # Кейс с таймаутом (повторный запрос в течение 180 секунд)
        r = requests.post(url, headers=headers, data=data)
        r = requests.post(url, headers=headers, data=data)

        r.raise_for_status()
        error_code = str(json.loads(r.text)['errorCode'])
        assert error_code == '2', 'Function "set_phone_number" returns wrong error code: ' + error_code

    return str(r.status_code)


def confirm_phone_number(test=False):
    set_phone_number()
    token_b64 = authentication()[0]
    url = 'http://188.18.13.78:9000/api/m/account/phone/confirm'
    headers = {'Authorization': 'basic ' + token_b64.decode("utf-8")}
    data = {"phone": "9125212573", "code": "12345"}

    # Кейс с верным ответом, без таймаута
    r = requests.post(url, headers=headers, data=data)

    r.raise_for_status()
    error_code = str(json.loads(r.text)['errorCode'])
    assert error_code == '1', 'Function "confirm_phone_number" returns wrong error code: ' + error_code

    if test:
        # Кейс с истекшим кодом подтверждения (больше 180 секунд)
        time.sleep(200)
        r = requests.post(url, headers=headers, data=data)

        r.raise_for_status()
        error_code = str(json.loads(r.text)['errorCode'])
        assert error_code == '2', 'Function "confirm_phone_number" returns wrong error code: ' + error_code
        # Кейс с неправильным кодом подтверждения
        set_phone_number()
        data = {"phone": "9125212573", "code": "wrong_code"}
        r = requests.post(url, headers=headers, data=data)

        r.raise_for_status()
        error_code = str(json.loads(r.text)['errorCode'])
        assert error_code == '3', 'Function "confirm_phone_number" returns wrong error code: ' + error_code

    return str(r.status_code)


test_authentication = authentication()
test_set_phone_number = set_phone_number(test=True)
test_confirm_phone_number = confirm_phone_number(test=True)

print('Test "authentication" returns status code: ' + test_authentication[1] + ' and valid error code "1". \n',
      'Test "set_phone_number" returns status code: ' + test_set_phone_number[0] + ' and valid error codes: "1", "2". \n',
      'Test "confirm_phone_number" returns status code: ' + test_confirm_phone_number[0] + ' and valid error codes: "1", "2", "3".\n',
      )
