import json
from jsonpath_ng import parse
from collections import deque


# Методы для проверки
class Checking:

    # Метод для проверки статус кода
    @staticmethod
    def check_status_code(result, status_code):
        assert status_code == result.status_code, 'Статус код не совпадает'
        print(f"Статус код = {result.status_code}")
        return result.status_code

    # Метод для обработки JSON и извлечения ключей
    @classmethod
    def extract_keys(cls, data):
        keys = []
        key_values = {}
        queue = deque([(data, '')])  # Очередь

        while queue:
            current_data, current_key = queue.popleft()
            if isinstance(current_data, dict):
                for key, value in current_data.items():
                    new_key = f"{current_key}.{key}" if current_key else key
                    keys.append(new_key)
                    key_values[new_key] = value
                    queue.append((value, new_key))
            elif isinstance(current_data, list):
                for idx, item in enumerate(current_data):
                    new_key = f"{current_key}[{idx}]"
                    keys.append(new_key)
                    key_values[new_key] = item
                    queue.append((item, new_key))
        return keys, key_values

    @staticmethod
    def check_json_key(result, expected_keys, detail=False):
        try:
            parsed_json = json.loads(result.text)
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Ошибка парсинга JSON: {e.msg} (позиция: {e.pos})",
                "missing_keys": []
            }

        # Извлекаем все ключи и значения
        actual_keys, key_values = Checking.extract_keys(parsed_json)

        if detail:
            print("\nИзвлеченные ключи:", actual_keys)

        # Проверяем наличие обязательных ключей
        missing_keys = [key for key in expected_keys if key not in actual_keys]

        result = {
            "success": {len(missing_keys) == 0},
            "missing_keys": missing_keys
        }

        if detail:
            if result["success"]:
                print("Проверка структуры JSON - успешно")
            else:
                assert False, f"Проверка структуры JSON - неуспешно. Отсутствуют ключи: {missing_keys}"
        return result

    # Метод для проверки значения обязательных полей в ответе запроса
    @staticmethod
    def check_json_value(result, fields_and_values):
        try:
            check = json.loads(result.text)
        except json.JSONDecodeError as e:
            print(f"Ошибка при парсинге JSON: {e}")
            return False

        success = True
        result_messages = []

        for field_path, expected_value in fields_and_values:
            # Используем точный JSONPath
            try:
                jsonpath_expr = parse(field_path)  # JSONPath-выражение
            except Exception as e:
                result_messages.append(f"Некорректный JSONPath '{field_path}': {e}")
                success = False
                continue

            matches = jsonpath_expr.find(check)

            if not matches:
                result_messages.append(f'Ключ "{field_path}" не найден в ответе')
                print(f'Ключ "{field_path}" не найден в ответе')
                success = False
                continue

            # Ожидаемое значение должно быть уникальным
            if len(matches) > 1:
                result_messages.append(f"Ключ '{field_path}' возвращает несколько значений: {matches}. Уточните путь.")
                print(f"Ключ '{field_path}' возвращает несколько значений: {matches}. Уточните путь.")
                success = False
                continue

            # Проверяем точное соответствие значения
            actual_value = matches[0].value
            if actual_value != expected_value:
                result_messages.append(
                    f"Ожидаемое значение для ключа '{field_path}' не совпадает: "
                    f"'{expected_value}' != '{actual_value}'"
                )
                print(
                    f"Ожидаемое значение для ключа '{field_path}' не совпадает: "
                    f"'{expected_value}' != '{actual_value}'"
                )
                success = False
            else:
                result_messages.append(f'Проверка ключа "{field_path}" - успешно')
                print(f'Проверка ключа "{field_path}" - успешно')

        return success, "\n".join(result_messages)

    # Метод для проверки времени ответа
    @staticmethod
    def check_response_time(result, expected_time):
        elapsed_time = result.elapsed.total_seconds()
        if elapsed_time >= expected_time:
            print(f"Время ответа: {elapsed_time} секунд")
            assert False, 'Ожидаемое время превышено'
        else:
            assert True
            print(f"Время ответа: {elapsed_time} секунд")
        return elapsed_time

    @staticmethod
    def get_slise(number, slise):
        number_str = str(number)
        first_three_digits_str = number_str[:slise]
        first_three_digits = int(first_three_digits_str)
        return first_three_digits
