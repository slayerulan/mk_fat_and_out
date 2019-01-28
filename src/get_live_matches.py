import api
from json_to_matches import json_to_matches


def get_live_matches():
    url = f"{api.get_current_mirror()}/LiveFeed/Get1x2_Zip?sports=103&count=1000&mode=4&cyberFlag=1&country=1"
    session = api.retry_session(url)
    json_info = api.json_request(session, url)
    if not json_info:
        return []

    return json_to_matches(json_info)
