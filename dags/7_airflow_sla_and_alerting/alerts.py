from SlackWebhookCli import SlackCli


class AlertManager:

    @staticmethod
    def on_failure_callback(context):
        text = ':red_circle: %s task failed' % str(context['task_instance'])
        SlackCli.post(text=text)

    @staticmethod
    def on_retry_callback(context):
        text = ':blue_circle: %s task retry' % str(context['task_instance'])
        SlackCli.post(text=text)

    @staticmethod
    def on_success_callback(context):
        text = ':green_circle: %s task success' % str(context['task_instance'])
        SlackCli.post(text=text)

    @staticmethod
    def sla_miss_callback(context):
        text = ':red_circle: %s sla miss' % str(context['task_instance'])
        SlackCli.post(text=text)
