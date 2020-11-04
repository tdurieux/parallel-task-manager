import os

from core.renderer.BashRenderer import BashRenderer
from core.renderer.EmptyRenderer import EmptyRenderer


def get_renderer(runner):
    """
    :param runner:
    :return: BashRenderer
    """
    return BashRenderer(runner)