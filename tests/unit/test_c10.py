
from unittest.mock import Mock

import pytest

from chapter10 import c10
from fixtures import SAMPLE


def test_next():
    with open(SAMPLE, 'rb') as f:
        assert next(c10.C10(f)).packet_length == 6680


def test_next_stop():
    with pytest.raises(StopIteration):
        next(c10.C10(Mock(read=Mock(side_effect=EOFError))))
