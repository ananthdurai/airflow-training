import json

import requests
from airflow.hooks.base_hook import BaseHook

'''
A simplified slack hook implementation to post message to the configured channel.
Documentation for configuring webhook in Slack https://api.slack.com/incoming-webhooks
'''


class SlackWebhookImpl(BaseHook):

    def __init__(self, url, text=None):
        """
        construct with url and payload to sent
        :param url:
        incoming webhook url.
        (e.g) https://hooks.slack.com/services/<workspace>/<channel>/<token>
        :param text: payload to post in a slack channel
        """
        self.url = url
        self.text = text

    def execute(self):
        self.run(sql=None)

    def run(self, sql):
        SlackCli.post(url=self.url, text=self.text)


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
