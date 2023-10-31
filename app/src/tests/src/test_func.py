import pytest

from tests.data import data
from tests.conftest import class_service

@pytest.mark.parametrize('inpt, expected_answer',
                         data.data)
def test_short_url_creation(class_service, inpt, expected_answer):

    link = class_service.create_short_url(inpt)
    assert link[:7] == expected_answer