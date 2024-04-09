import json

def search_food_json(file_path, search_keyword, fields):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            if search_keyword in data.get('keywords', []):
                result = {}
                for field in fields:
                    result[field] = data.get(field)
                results.append(result)
    return data