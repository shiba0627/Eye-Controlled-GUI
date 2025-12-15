from datetime import datetime

now = datetime.now()
now_micro = now.strftime('%Y%m%m_%H%M%S%f')
print(f'now={now}, micro ={now_micro}')

list = []
for i in range(100):
    list.append(i)
print(list)

file_name = f'output/testtxt_{now_micro}.txt'
try:
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(list)
except IOError as e:
    print(e)

