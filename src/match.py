import logging

import retry
from requests_html import HTMLSession

import api
from scripts import get_mirror


class Match:
    def __init__(self, id):
        self._id = id
        self._brut_coef = 0
        self.score = [-1, -1]
        self.W_coefs = [' - ', ' - ']
        self.WR_coefs = [-1, -1]
        self.finishes = {
            'R': -1,
            'F': -1,
            'B': -1
        }

        self.get_info_by_id()
        self.fill_info()

    def __repr__(self):
        return f"""
*{self._left_fighter} - {self._right_fighter}*
П1 в матче: {self.W_coefs[0]}
П2 в матче: {self.W_coefs[1]}
кэф на Фат: {self.finishes.get('F')}
кэф на Руку: {self.finishes.get('R')}
{'Фаталити и добивание' if self.is_fat_r_algo() else ''}
{'Матч с аутсайдером' if self.is_out_algo() or self.is_out_algo_with_blank() else ''}
"""

    def __str__(self):
        return f"""
*{self._left_fighter} - {self._right_fighter}*
П1 в матче: {self.W_coefs[0]}
П2 в матче: {self.W_coefs[1]}
кэф на Фат: {self.finishes.get('F')}
кэф на Руку: {self.finishes.get('R')}
{'Фаталити и добивание' if self.is_fat_r_algo() else ''}
{'Матч с аутсайдером' if self.is_out_algo() or self.is_out_algo_with_blank() else ''}
"""

    @retry.retry(tries=5, delay=1)
    def get_info_by_id(self):
        url = f"{get_mirror.get_current_mirror()}/LiveFeed/GetGameZip?id={self._id}"
        session = api.retry_session(url)
        try:
            response = session.get(url, timeout=10)
        except Exception as e:
            logging.error(e)
            raise e
        json_data = response.json()
        self._json_info = json_data.get('Value')

    def fill_info(self):
        self.is_before()
        self.is_first_round()
        self.fill_fighters()
        self.fill_coefs()

    def is_before(self):
        score_info = self._json_info.get('SC')
        self._is_before = score_info.get(
            'I') and score_info.get('FS') == {}

    def is_first_round(self):
        score_info = self._json_info.get('SC')
        self._is_first_round = score_info.get('CP') == 1

    def fill_coefs(self):
        coefs = self._json_info.get('E')
        if not coefs:
            return
        for c in coefs:
            # W1
            if c.get('T') == 1:
                self.W_coefs[0] = c.get('C')
            # W2
            if c.get('T') == 3:
                self.W_coefs[1] = c.get('C')
            # R
            if c.get('T') == 4059:
                self.finishes['R'] = c.get('C')
            # F
            if c.get('T') == 4057:
                self.finishes['F'] = c.get('C')
            # BRUT
            if c.get('T') == 4058:
                self.finishes['B'] = c.get('C')
            # WR1
            if c.get('T') == 2140:
                self.WR_coefs[0] = c.get('C')
            # WR2
            if c.get('T') == 2141:
                self.WR_coefs[1] = c.get('C')

    def fill_fighters(self):
        self._left_fighter = self._json_info.get('O1')
        self._right_fighter = self._json_info.get('O2')

    def is_coef_more_than(self, coef, threshold):
        return self.finishes.get(coef) >= threshold

    def is_fat_r_algo(self):
        return ((self.is_coef_more_than('F', 2.0) and self.is_coef_more_than('R', 2.9))
                or
                (self.is_coef_more_than('R', 2.0) and self.is_coef_more_than('F', 2.9)))

    def is_out_algo(self):
        if ' - ' in self.W_coefs:
            return False
        return self.W_coefs[0] / self.W_coefs[1] >= 8 or self.W_coefs[1] / self.W_coefs[0] >= 8

    def is_out_algo_with_blank(self):
        if ' - ' in self.W_coefs:
            if self.W_coefs[0] == ' - ' and self.W_coefs[1] >= 8:
                return True
            elif self.W_coefs[1] == ' - ' and self.W_coefs[0] >= 8:
                return True
        return False

    @property
    def fighters(self):
        return f"{self._left_fighter} - {self._right_fighter}"

    @property
    def id(self):
        return self._id
