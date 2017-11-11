import requests

while True:
    command = input('CMD>> ')
    command = command.strip()
    if command[0] == 'q':
        break
    if command[0] == 'post':
        r = requests.post(
            'https://localhost:9000',
            data={
                'accessory-name': 'my-desktop-lamp',
                'action': '{}'.format(command[1]),
                'passwd': 'ilovekaling'
            },
            verify='root.crt')
        print(r.text)
