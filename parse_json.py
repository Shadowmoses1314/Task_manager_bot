import json


def parse_json(json_str):
    try:
        with open(json_str, 'r') as file:
            json_data = json.load(file)
        return json_data
    except FileNotFoundError:
        print("Файл не найден:", json_str)
        return None
    except json.JSONDecodeError as e:
        print("Ошибка при разборе JSON:", e)
        return None
