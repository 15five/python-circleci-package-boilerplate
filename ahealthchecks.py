#$end # for arepl

# Rough Draft

import json
from typing import List
import requests

API_URL_BASE = "https://healthchecks.io/api/v1/"
API_READONLY_key = "stop looking at my naughty bits"
API_key = "seriously this is private"

cache = {
    "foo": "mock url"
}

default_creation_params = {
    'name': None,
    'tags': None,
    'desc': None,
    'timeout': None,
    'grace': None,
    'schedule': None,
    'tz': None,
    'channels': ["*"],
}


def create_check(check_name: str, creation_params: dict):
    if 'name' not in creation_params:
        creation_params['name'] = check_name
    for param in default_creation_params:
        if param not in creation_params and default_creation_params[param] is not None:
            creation_params[param] = default_creation_params[param]
    channels_response = requests.get(API_URL_BASE + '/channels/', headers={"X-Api-key": API_key})
    channels: List[dict] = channels_response.json()['channels']
    # convert list of channels to dict indexed by name
    # ideally user would just pass in channel id isntead of name
    # in which case this would not be needed
    # however there is no way in the GUI to see the channel ID
    # so the user will be using name instead
    channels_by_name = {}
    for channel in channels:
        channel_name = channel['name'].lower()
        if channel_name in channels_by_name:
            raise ValueError(f"Ahealthchannel requires all channel names to be unique for identifcation purposes. \
                            {channel}\n\nis a duplicate of channel with id {channels_by_name[channel_name]}")
        channels_by_name[channel_name] = channel['id']
    channel_ids = []
    for channel_name in creation_params['channels']:
        channel_name = channel_name.lower()
        if channel_name == "*":
            # * means assign all chanels
            # so no needs to specify individual id's
            break
        channel_ids.append(channels_by_name[channel_name])
    creation_params['channels'] = ','.join(channel_ids)
    creation_response = requests.post(
        API_URL_BASE + '/checks/', headers={"X-Api-key": API_key}, data=json.dumps(creation_params)
    )
    check = creation_response.json()
    endpoint = check['ping_url'][check['ping_url'].rfind('/') + 1:]
    return endpoint


# args: check_name, creation_params
check_name = "foo"
creation_params = {}
# start of func
check_name = check_name.lower()
# try to get endpoint from cache
endpoint = cache.get(check_name)
# if not in cache
if not endpoint:
    # get healthchecks in current project
    checks: List[dict] = requests.get(API_URL_BASE + '/checks/', headers={"X-Api-key": API_key}).json()["checks"]
    # convert list of checks to dict indexed by name like cache
    checks_by_name = {}
    for check in checks:
        existing_check_name = check['name'].lower()
        if existing_check_name in checks_by_name:
            # todo: only raise error if duplicate check_name
            # we don't want everything to fail if there is a single duplicate
            raise ValueError(f"Ahealthcheck requires all check names to be unique for identifcation purposes. \
                              {check}\n\nis a duplicate of check with ping_url {checks_by_name[existing_check_name]}")
        checks_by_name[existing_check_name] = check['ping_url']
    endpoint = checks_by_name.get(check_name)
    # if not in existing healthchecks:
    if not endpoint:
        print('creating check')
        endpoint = create_check(check_name, creation_params)
        # save check_name/endpoint to cache
        cache[check_name] = endpoint
    else:
        print('check already exists')
        print('updating cache')
        for check_name in checks_by_name:
            cache[check_name] = checks_by_name[check_name]
print('endpoint is ' + endpoint)





# def get_endpoint():
#     return "foo"

# def start():
#     endpoint = get_endpoint()
#     try:
#         requests.get(endpoint + "/start", timeout=5)
#     except requests.exceptions.RequestException:
#         # If the network request fails for any reason, we don't want
#         # it to prevent the main job from running
#         pass

"""
### management command
ping(name + '/' + flag)
make sure to prepend vpcname so people can easily tell what vpc the healthcheck
is failing in
"""