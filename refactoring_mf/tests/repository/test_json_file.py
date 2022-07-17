from unittest import TestCase
from unittest.mock import patch

from io import StringIO
from os import environ

from refactoring_mf.repository import json_file

class JsonFileTest(TestCase):

    @patch("refactoring_mf.repository.json_file.open")
    def test_get_data_from_json(self, open):
        environ["JSON_DATA_DIR"] = "/sample/json/data/dir"
        entity_name = "foo"
        expected = {
            "foo": "bar"
        }
        open.return_value = StringIO('{"foo": "bar"}')

        actual = json_file.get_data_from_json(entity_name)

        assert actual == expected
