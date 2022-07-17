from unittest import TestCase

from refactoring_mf.apps.statement import Statement

class StatementTestCase(TestCase):
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

        statement = Statement()
        actual_separated = statement(invoice[0], plays).split("\n")
        
        for actual, expected in zip(actual_separated, expected_lines):
            assert actual == expected
