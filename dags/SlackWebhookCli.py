import json

import requests


class SlackCli:

    @staticmethod
    def post(text, url=None):
        headers = {'Content-type': 'application/json'}
        payload = {}
        payload['text'] = text
        url = SlackCli.defaultUrl() if url is None else url
        requests.post(url=url, headers=headers, data=json.dumps(payload))

    @staticmethod
    def defaultUrl():
        return 'https://hooks.slack.com/services/<workspace>/<channel>/<token>'
