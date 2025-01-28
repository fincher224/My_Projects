import allure
import pytest
from utils.http_methods import HttpMethods
from utils.checking import Checking

base_url = 'https://reqres.in'


class Authorisation:
    @staticmethod
    def get_token(email, password):
        json_body_auth = {
            "email": email,
            "password": password
        }

        print('\n\nАвторизация POST')
        post_resource = '/api/login'
        post_url = base_url + post_resource
        print(f'Авторизация URL: {post_url}')

        try:
            result_post = HttpMethods.post(post_url, json_body_auth)
            Checking.check_status_code(result_post, 200)
            Checking.check_response_time(result_post, 5)

            json_response_post = result_post.json()
            token = json_response_post.get('token')
            print(f'Токен: {token}')

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            return headers
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            allure.attach(
                f"{e}",
                name=f"Ошибка авторизации",
                attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Ошибка авторизации: {e}")
