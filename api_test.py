import requests
import json
import base64


def authentication():
    r = requests.post('http://188.18.13.78:9000/api/m/account/dev',
                      data={"devType": "A", "pushToken": "firebaseSecretToken", "brand": 'YIT'}
                      )

    # Лучше упасть с ошибкой сейчас, чем что-нибудь отвалится потом из-за отсутствующего токена
    r.raise_for_status()

    response_content = json.loads(r.text)
    token = response_content['auth_Token']
    token_b64 = base64.b64encode(token.encode())

    return token_b64, str(r.status_code)


def set_phone_number():
    token_b64 = authentication()[0]
    r = requests.post('http://188.18.13.78:9000/api/m/account/phone',
                      headers={'Authorization': 'basic ' + token_b64.decode("utf-8")},
                      data={"phone": "9125212573"}
                      )

    error_code = json.loads(r.text)['errorCode']

    return str(r.status_code), str(error_code)


def confirm_phone_number():
    token_b64 = authentication()[0]
    r = requests.post('http://188.18.13.78:9000/api/m/account/phone/confirm',
                      headers={'Authorization': 'basic ' + token_b64.decode("utf-8")},
                      data={"phone": "9125212573", "code": "12345"}
                      )

    error_code = json.loads(r.text)['errorCode']
    return str(r.status_code), str(error_code)


test_authentication = authentication()
assert test_authentication[1] == '200', 'Func "authentication" returns status code:' + test_authentication[1]

test_set_phone_number = set_phone_number()
assert test_set_phone_number[0] == '200', 'Func "set_phone_number" returns status code:' + test_set_phone_number[0]
assert test_set_phone_number[1] in ['1', '2'], 'Func "set_phone_number" returns unknown error code:' + test_set_phone_number[1]

test_confirm_phone_number = confirm_phone_number()
assert test_confirm_phone_number[0] == '200', 'Func "confirm_phone_number" returns status code:' + test_confirm_phone_number[0]
assert test_confirm_phone_number[1] in ['1', '2', '3'], 'Func "confirm_phone_number" returns unknown error code:' + test_confirm_phone_number[1]

print('Test "authentication" returns status code: ' + test_authentication[1] + '. \n',
      'Test "set_phone_number" returns status code: ' + test_set_phone_number[0] + ', error code: '+ test_set_phone_number[1] + '. \n',
      'Test "confirm_phone_number" returns status code: ' + test_confirm_phone_number[0] + ', error code: ' + test_confirm_phone_number[1] + '. \n',
      )
