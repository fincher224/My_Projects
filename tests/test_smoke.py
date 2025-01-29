import allure
import pytest
from utils.http_methods import HttpMethods
from utils.checking import Checking
import json
from tests.authorisation_request_web import Authorisation
from faker import Faker

base_url = 'https://reqres.in/api/users'


class TestSmoke:
    @pytest.mark.smoke
    @allure.tag('api')
    @allure.parent_suite("Тест")
    @allure.suite('https://reqres.in')
    @allure.sub_suite('Запросы')
    @allure.title('API add_user')
    def test_api_add_user(self):
        with allure.step('Авторизация'):
            token = Authorisation.get_token('eve.holt@reqres.in', 'cityslicka')

        with allure.step('Создание пользователя'):
            try:
                url = 'https://reqres.in/api/users'

                fakes = Faker()
                first_name = fakes.first_name()
                last_name = fakes.last_name()

                request_body = {
                    "name": f"{first_name}",
                    "job": f"{last_name}"
                }

                print(f'\nСоздание пользователя\nPOST URL: {url}')
                result_post = HttpMethods.post(url, request_body, token)
                json_body_response = result_post.json()

                status_code = Checking.check_status_code(result_post, 201)
                response_time = Checking.check_response_time(result_post, 5)

                log_message = (
                    f"URL: {url}\n"
                    f"\nСтатус-код: {status_code}\n"
                    f"Время ответа: {response_time}\n"
                    f"\nJSON Response:\n{json.dumps(json_body_response, ensure_ascii=False, indent=4)}"

                )
                allure.attach(
                    log_message,
                    name="Детализация проверки",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                print(f"Ошибка: {e}")
                allure.attach(
                    f"{e}",
                    name=f"Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Ошибка: {e}")

    @pytest.mark.smoke
    @allure.tag('api')
    @allure.parent_suite("Тест")
    @allure.suite('https://reqres.in')
    @allure.sub_suite('Запросы')
    @allure.title('API list_user')
    def test_api_list_user(self):
        with allure.step('Авторизация'):
            token = Authorisation.get_token('eve.holt@reqres.in', 'cityslicka')

        with allure.step('Проверка структуры Json'):
            try:
                url = 'https://reqres.in/api/users'

                print(f'\nВывод всех пользователей\nGET URL: {url}')
                result_post = HttpMethods.get(url, token)
                json_body_response = result_post.json()

                status_code = Checking.check_status_code(result_post, 200)
                response_time = Checking.check_response_time(result_post, 5)

                key, result = Checking.check_json_key(result_post,  [
                    'page', 'per_page', 'total', 'total_pages', 'data', 'support',
                    'data[0]', 'data[1]', 'data[2]', 'data[3]', 'data[4]', 'data[5]',
                    'support.url', 'support.text', 'data[0].id', 'data[0].email',
                    'data[0].first_name', 'data[0].last_name', 'data[0].avatar',
                    'data[1].id', 'data[1].email', 'data[1].first_name', 'data[1].last_name',
                    'data[1].avatar', 'data[2].id', 'data[2].email', 'data[2].first_name',
                    'data[2].last_name', 'data[2].avatar', 'data[3].id', 'data[3].email',
                    'data[3].first_name', 'data[3].last_name', 'data[3].avatar', 'data[4].id',
                    'data[4].email', 'data[4].first_name', 'data[4].last_name', 'data[4].avatar',
                    'data[5].id', 'data[5].email', 'data[5].first_name',
                    'data[5].last_name', 'data[5].avatar',], detail=True)

                key_value, result_1 = Checking.check_json_value(result_post, [
                    ('$.data[5].email', 'tracey.ramos@reqres.in'),
                    ('$.data[5].id', 6)
                ])

                log_message = (
                    f"URL: {url}\n"
                    f"\nСтатус-код: {status_code}\n"
                    f"Время ответа: {response_time}\n"
                    f"Проверка json структуры: {result}\n"
                    f"{result_1}\n"
                    f"\nJSON Response:\n{json.dumps(json_body_response, ensure_ascii=False, indent=4)}"

                )
                allure.attach(
                    log_message,
                    name="Детализация проверки",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:
                print(f"Ошибка: {e}")
                allure.attach(
                    f"{e}",
                    name=f"Ошибка",
                    attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Ошибка: {e}")