import requests
from libs import log, pictorem as pct

with open('key.txt', 'r') as file:
    key = file.read().replace('\n', '').replace(' ', '')
    file.close()

if len(key) < 5:
    log.warning('You did not put your access token into key.txt')
    exit(0)


def work_on_bdate(bdate):
    spl = bdate.split('.')

    if len(spl) == 3:
        return spl[2]
    else:
        return False


def user_get(user_id):
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': key,
            'v': 5.92,
            'user_ids': user_id,
            'fields': 'city, bdate, domain'
        }

    ).json()

    return response['response'][0]


def friends_get(user_id):
    response = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': key,
            'v': 5.92,
            'user_id': user_id,
            'order': 'random',
            'count': '10000',
            'fields': 'city, bdate, sex'
        }

    ).json()

    try:
        return response['response']

    except:
        log.warning(response['error']['error_msg'])
        exit(0)


def get_count_of_the_same_elements(list, element):
    count = 0

    for el in list:
        if el == element:
            count += 1

    return count


def get_max_count_of_same_elements(list):
    max = 0

    for element in list:
        count = get_count_of_the_same_elements(list, element)

        if count > max:
            max = count

    return max


def get_possible(list, max):
    possible = ''

    for element in list:
        count = get_count_of_the_same_elements(list, element)

        if count == max and element not in possible:
            if len(possible) == 0:
                possible += element

            else:
                possible += ' / ' + element

    return possible


def get_frame(tab, the_longest_str, color):
    n = len(the_longest_str)
    k = len(tab)

    if color == 'red':
        frame = pct.red.bold('+' + ('-' * (n + k)) + '+')

    elif color == 'green':
        frame = pct.green.bold('+' + ('-' * (n + k)) + '+')

    elif color == 'yellow':
        frame = pct.yellow.bold('+' + ('-' * (n + k)) + '+')

    elif color == 'blue':
        frame = pct.blue.bold('+' + ('-' * (n + k)) + '+')

    elif color == 'light_blue':
        frame = pct.light_blue.bold('+' + ('-' * (n + k)) + '+')

    elif color == 'purple':
        frame = pct.purple.bold('+' + ('-' * (n + k)) + '+')

    else:
        frame = 'ERROR'

    return frame


def get_info(user_id):
    fields = 'sex, bdate, city, country'

    response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'v': 5.92,
            'access_token': key,
            'user_ids': user_id,
            'fields': fields,
        }
    ).json()

    return response['response'][0]


def get_reg_date(user_id):
    response = requests.get(
        'https://vk.com/foaf.php?id=' + str(user_id)
    ).text

    a = response.index('ya:created dc:date="') + len('ya:created dc:date="')
    b = response[a+1:].index('T') + a + 1

    return response[a:b].replace('-', '.')
