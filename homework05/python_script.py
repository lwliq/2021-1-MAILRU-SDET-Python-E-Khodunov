from collections import Counter
import json
import re
import sys

with open("access.log") as log:
    lines = [line.split(' ') for line in log]
result = {}

# 1
result['Task 01'] = {'count': sum(1 for _ in lines)}

# 2
types_counted = Counter([line[5].strip('"') for line in lines])
result['Task 02'] = [
    {'type': r_type, 'count': value}
    for r_type, value in sorted(types_counted.items(), key=lambda item: item[1], reverse=True)
]

# 3
locations_counted = Counter([line[6] for line in lines])
result['Task 03'] = [
    {'location': url, 'count': value}
    for url, value in sorted(locations_counted.items(), key=lambda item: item[1], reverse=True)[:10]
]

# 4
client_error_requests = [
    {'ip': line[0], 'location': line[6], 'status': line[8], 'size': int(line[9])}
    for line in lines if re.match('4[0-9]{2}$', line[8])
]
result['Task 04'] = [
    request for request in sorted(client_error_requests, key=lambda item: item['size'], reverse=True)[:5]
]

# 5
server_error_clients_counted = Counter([line[0] for line in lines if re.match('5[0-9]{2}$', line[8])])
result['Task 05'] = [
    {'ip': ip, 'count': value}
    for ip, value in sorted(server_error_clients_counted.items(), key=lambda item: item[1], reverse=True)[:5]
]

if '--json' in sys.argv:
    with open('result_python.json', 'w') as file:
        json.dump(result, file, indent=4)
else:
    with open("result_python.txt", "w") as file:
        file.write('Общее количество запросов\n')
        file.write(str(result['Task 01']['count']) + '\n')

        file.write('\nОбщее количество запросов по типу\n')
        for request in result['Task 02']:
            file.write(f'{request["type"]}-{request["count"]}\n')

        file.write('\nТоп 10 самых частых запросов\n')
        for request in result['Task 03']:
            file.write(f'{request["location"]} {request["count"]}\n')

        file.write('\nТоп 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой\n')
        for request in result['Task 04']:
            file.write(f'{request["location"]} {request["status"]} {request["size"]} {request["ip"]}\n')

        file.write('\nТоп 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой\n')
        for request in result['Task 05']:
            file.write(f'{request["ip"]} {request["count"]}\n')
