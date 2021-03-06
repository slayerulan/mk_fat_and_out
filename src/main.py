import logging
from collections import deque
from time import sleep

import api
from get_live_matches import get_live_matches
from scripts import get_mirror, send_to_channel

sended_ids = deque(maxlen=15)
sended_fighters = deque(maxlen=15)

while True:
    try:
        for g in get_live_matches():
            if g.id in sended_ids:
                continue
            if g.fighters in sended_fighters:
                continue
            if g.is_target():
                logging.error(f"Sending {g}")
                send_to_channel.send_msg(str(g))
                sended_ids.append(g.id)
                sended_fighters.append(g.fighters)
            else:
                logging.error(f"{g}")
#                logging.error(f"""is_before: {g._is_before},
#is_first: {g._is_first_round}
#is_fat: {g.is_fat_r_algo()}
# is_out_algo: {g.is_out_algo()}")
# is_out_algo_blank: {g.is_out_algo_with_blank()}")""")
        else:
            logging.error('No matches now')
    except Exception as e:
        # logging.error(e)
        print(f"39: {e}")
        continue
