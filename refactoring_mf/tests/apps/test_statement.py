from unittest import TestCase
import pytest

from refactoring_mf.apps.statement import Statement

class TestStatement:
    def test_statement(self):
        invoice = [
            {
                "customer": "BigCo",
                "performances": [
                    {
                        "playID": "hamlet",
                        "audience": 55
                    },
                    {
                        "playID": "as-like",
                        "audience": 35
                    },
                    {
                        "playID": "othello",
                        "audience": 40
                    },
                ]
            }
        ]
        plays = {
            "hamlet": {"name": "Hamlet", "type": "tragedy"},
            "as-like": {"name": "As You Like It", "type": "comedy"},
            "othello": {"name": "Othello", "type": "tragedy"}
        }
        expected_lines = [
            "Statement for BigCo",
            "    Hamlet: $650.00 (55 seats)",
            "    As You Like It: $580.00 (35 seats)",
            "    Othello: $500.00 (40 seats)",
            "Amount owed is $1,730.00",
            "You earned 47 credits"
        ]

        sut = Statement(invoice[0], plays)
        actual_separated = sut().split("\n")
        
        for actual, expected in zip(actual_separated, expected_lines):
            assert actual == expected

    amount_for_inputs = [
        (
            {"name": "Hamlet", "type": "tragedy"},
            {
                "playID": "hamlet",
                "audience": 55
            },
            65000
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {
                "playID": "as-like",
                "audience": 35
            },
            58000
        ),
    ]
    @pytest.mark.parametrize("play, performance, expected", amount_for_inputs)
    def test_amount_for(self, play, performance, expected):
        sut = Statement({}, {})
        actual = sut.amount_for(play, performance)
        
        assert actual == expected

    def test_amount_for_with_unknown_type(self):
        play = {"name": "X", "type": "XX"},
        perfomance = {
            "playID": "XXX",
            "audience": 99
        },

        sut = Statement({}, {})
        with pytest.raises(Exception):
            actual = sut.amount_for(play, perfomance)
