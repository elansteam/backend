import pika
from config import Config
from loguru import logger
from db.models.annotations import IntIdAnnotation


def produce_submission(submission_id: IntIdAnnotation):
    with pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost')) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=Config.rabbitmq_main_queue)

        channel.basic_publish(exchange="",
                              routing_key=Config.rabbitmq_main_queue,
                              body=f"{submission_id}")
        logger.info(f'Published submission with id {submission_id}')
