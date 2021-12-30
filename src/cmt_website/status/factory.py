import logging

from cmt_website.status.error import ErrorStatus
from cmt_website.status.talon.shm import SHMStatusReader


def make_status_reader():
    try:
        return SHMStatusReader()
    except RuntimeError as e:
        logging.error(f"Error creating status reader, received error {e}")
        logging.info("Creating error status reader")
        return ErrorStatus()
