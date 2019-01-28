import logging
from requests_html import HTMLSession


def get_current_mirror():
    """
    Returns current available mirror of the 1xbet.com, 
    first try to redirects, if fails, trying to use google
    """
    session = HTMLSession()
    url = 'http://1xstavka.ru'
    try:
        return session.get(url, timeout=10).url.split('?')[0]
    except Exception as e:
        logging.error(f"{e}")
        url = 'https://www.google.ru/search?&q=1xbet.com'
        try:
            response = session.get(url, timeout=10)
        except Exception as e:
            logging.error(f"{e}")
            return "Second try, doesn't work"

        return f'https://{response.html.search("⇒ {} ⇒")[0]}'
