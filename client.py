import requests

while True:
    command = input('CMD>> ')
    command = command.strip()
    if command[0] == 'post':
        r = requests.post('localhost:9000', command[1])
        print('posted')
    if command[0] == 'q':
        break
