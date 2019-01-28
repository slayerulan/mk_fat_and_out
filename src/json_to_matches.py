import logging

from match import Match


def json_to_matches(json_data):
    info = json_data.get('Value')

    matches = []
    for g in info:
        try:
            matches.append(Match(g.get('I')))
        except Exception as e:
            logging.error(e)
            continue

    return matches
