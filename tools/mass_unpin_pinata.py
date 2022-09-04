from math import ceil
from requests import request
from time import sleep


log_file = 'PinataUnpins.log'
filter_name = input('\nEnter String to Filter Name by:')
auth_key = input('\nPaste your Pinata JWT Auth:')


def pinnata(file):
    ipfs_url = 'https://api.pinata.cloud/pinning/unpin/' + file
    ipfs_headers = {"Authorization": "Bearer " + auth_key}
    return request('DELETE', ipfs_url, data={}, headers=ipfs_headers)


def get_pinlist(page, pagelimit):
    pagelimit = 'pageLimit=' + str(pagelimit)
    page = 'pageOffset=' + str(page)
    url = "https://api.pinata.cloud/data/pinList?status=pinned&pinSizeMin=100&" + pagelimit + '&' + page
    headers = {"Authorization": "Bearer " + auth_key}
    return request("GET", url, headers=headers, data={})


def do_delete(page_list, pin_count):
    del_count = 0
    if pin_count > 100:
        page_list = []
        page_count = ceil(pin_count / 100)
        count_up = 0
        while True:
            page_list += [str(count_up)]
            count_up += 1
            page_count -= 1
            if page_count == 0:
                break
        pin_count = 100
    for page in page_list:
        response = get_pinlist(page, pin_count)
        pin_returnJson = response.json()
        pin_count = int(pin_returnJson['count'])
        print('Total Pin Count: ', str(pin_count))
        for item in pin_returnJson['rows']:
            img_name = item['metadata']['name']
            if filter_name in img_name:
                sleep(1)
                pr_str = '\r' + img_name
                print(pr_str + ' being unpinned', end=' ')
                item_hash = item['ipfs_pin_hash']
                unpinret = str(pinnata(item_hash))
                if unpinret == '<Response [200]>':
                    success_str = 'Unpin Success: ' + item_hash + ' (' + img_name + ')'
                    del_count += 1
                    print(pr_str + ' SUCCESS!      ', end=' ')
                    with open(log_file, 'a') as unpinlog:
                        unpinlog.write(success_str + '\n')
                        unpinlog.close()
                else:
                    print('!ERR! ', unpinret)
    return str(del_count)


page_list = ['0']
pin_count = int(get_pinlist(0, 10).json()['count'])
confirm = input('\n\nProceed and delete all pins with ' + filter_name + ' in their name, from your ' + str(pin_count) + ' pins?\n    1 - Yes\n    0 - No\n\nEnter Your Selection:>')
print('\n\n')
try:
    confirm = int(confirm)
except Exception:
    pass
if confirm == 1:
    if not log_file:
        try:
            open(log_file, 'x')
        except OSError:
            pass
    del_ret = do_delete(page_list, pin_count)
    print('\n\nComplete! Unpinned ' + del_ret + ' pins out of ' + str(pin_count))
    print('\nLog file: ' + log_file)
