import boto.sqs
import logging
import sys
import time
from boto.sqs.message import Message
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY, AWS_REGION
from settings import TORRENT_DAEMON, POLL_INTERVAL
from daemon import exceptions


def load_module(name):
    module_name = 'package.' + name
    klass_name = module_name.split('.')[-1]
    module = __import__(name, fromlist=[klass_name])
    return getattr(module, klass_name)


def get_queue(queue_name):
    sqs_conn = boto.sqs.connect_to_region(AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY)
    queue = sqs_conn.create_queue('inbox', 120)
    return queue

def put_message(body, queue_name='outbox'):
    sqs_conn = boto.sqs.connect_to_region(AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY)
    queue = sqs_conn.create_queue(queue_name, 120)
    msg = Message()
    msg.set_body(body)
    queue.write(msg)

def on_message(msgs, torrent_daemon):
    for msg in msgs:
        torrent = msg.get_body()
        logging.info('Processing file %s', torrent)
        try:
            torrent_daemon.add(torrent)
            logging.info("Torrent %s has been added", torrent)
        except exceptions.InvalidTorrent as ex:
            logging.error('The torrent %s was not valid. Exception follows',
                    msg.body)
            logging.exception('%s', str(ex))
        finally:
            queue.delete_message(msg)

def main():
    klass = load_module(TORRENT_DAEMON)
    torrent_daemon = klass()
    while True:
        try:
            queue = get_queue('inbox')
            msgs = queue.get_messages()
            logging.debug('Polling SQS with %s results', len(msgs))
            on_message(msgs, torrent_daemon)
            time.sleep(POLL_INTERVAL)
            put_message(torrent_daemon.status())
        except boto.exception.SQSError as ex:
            logging.error('Error connecting to AWS SQS. %s', ex.message)
            logging.debug('%s', ex.body)
            sys.exit(-1)


if __name__  == "__main__":
    main()
