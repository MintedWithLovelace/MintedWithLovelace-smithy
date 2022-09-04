from requests import request
do_name = input('Filter by Image Name String:')
do_limit = int(input('Stop Deleting at pin remaining count:'))
auth_key = input('Paste your Pinata JWT Auth:')


def pinnata(file):
    ipfs_url = 'https://api.pinata.cloud/pinning/unpin/' + file
    ipfs_headers = {"Authorization": "Bearer " + auth_key}
    return request('DELETE', ipfs_url, data={}, headers=ipfs_headers)


while True:
    url = "https://api.pinata.cloud/data/pinList?status=pinned&pinSizeMin=100"
    headers = {"Authorization": "Bearer " + auth_key}
    response = request("GET", url, headers=headers, data={})
    pin_returnJson = response.json()
    pin_count = int(pin_returnJson['count'])
    print('Pin Count Now At: ', str(pin_count))
    if pin_count > do_limit:
        for item in pin_returnJson['rows']:
            if do_name in item['metadata']['name']:
                print('Deleting ', item['metadata']['name'])
                item_hash = item['ipfs_pin_hash']
                unpinret = str(pinnata(item_hash))
                if unpinret == '<Response [200]>':
                    pass
                else:
                    print('!ERR! ', unpinret)
    else:
        break
