from unittest.mock import patch
import pytest
from tests.apps import fixtures

from refactoring_mf.apps.statement import (
    StatementDataCreator,
    StatementData,
    StatementRenderer,
    PerformanceCalculator,
)


class TestPerformanceCalculator:
    def test_init(self):
        performance = {"playID": "hamlet", "audience": 55}
        play = {"name": "Hamlet", "type": "tragedy"}
        sut = PerformanceCalculator(performance, play)

        assert sut.performance == performance
        assert sut.play == play

    amount_inputs = [
        (
            {"name": "Hamlet", "type": "tragedy"},
            {
                "play": {"name": "Hamlet", "type": "tragedy"},
                "playID": "hamlet",
                "audience": 55,
            },
            65000,
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {
                "play": {"name": "As You Like It", "type": "comedy"},
                "playID": "as-like",
                "audience": 35,
            },
            58000,
        ),
    ]

    @pytest.mark.parametrize("play, performance, expected", amount_inputs)
    def test_amount(self, play, performance, expected):
        sut = PerformanceCalculator(performance, play)
        actual = sut.amount()

        assert actual == expected

    def test_amount_for_with_unknown_type(self):
        perfomance = (
            {
                "playID": "XXX",
                "audience": 99,
            },
        )
        play = {"name": "XXXXX", "type": "XXXXX"}

        sut = PerformanceCalculator(perfomance, play)
        with pytest.raises(Exception):
            sut.amount(perfomance)

    test_volume_credits_inputs = [
        (
            {"name": "Hamlet", "type": "tragedy"},
            {
                "playID": "hamlet",
                "audience": 55,
            },
            25,
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {
                "playID": "as-like",
                "audience": 35,
            },
            12,
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {
                "playID": "as-like",
                "audience": 3,
            },
            0,
        ),
    ]

    @pytest.mark.parametrize(
        "play, performance, expected", test_volume_credits_inputs
    )
    def test_volume_credits(self, play, performance, expected):
        sut = PerformanceCalculator(performance, play)
        actual = sut.volume_credits()

        assert actual == expected


class TestStatementDataCreator:
    @patch("refactoring_mf.apps.statement.StatementDataCreator.play_for")
    @patch("refactoring_mf.apps.statement.PerformanceCalculator")
    def test_init(self, PerformanceCalculator, play_for):
        invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 55},
            ],
        }
        plays = {
            "hamlet": {"name": "Hamlet", "type": "tragedy"},
        }
        expected_invoice = {
            "customer": "BigCo",
            "performances": [
                {
                    "play": {"name": "Hamlet", "type": "tragedy"},
                    "playID": "hamlet",
                    "audience": 55,
                    "amount": 65000,
                    "volume_credits": 25,
                },
            ],
        }

        PerformanceCalculator.return_value.volume_credits.return_value = 25
        PerformanceCalculator.return_value.amount.return_value = 65000
        play_for.return_value = {"name": "Hamlet", "type": "tragedy"}
        PerformanceCalculator.return_value.play = play_for.return_value
        sut = StatementDataCreator(invoice, plays)

        PerformanceCalculator.assert_called_once()
        play_for.assert_called_once()
        PerformanceCalculator.return_value.amount.assert_called_once()
        PerformanceCalculator.return_value.volume_credits.assert_called_once()
        assert sut.invoice == expected_invoice
        assert sut.plays == plays

    @patch("refactoring_mf.apps.statement.StatementRenderer.render_plain_text")
    def test_call(self, render_plain_text):
        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        statement_data = StatementData(
            "customer",
            "performances",
            sut.total_amount(sut.invoice["performances"]),
            sut.total_volume_credits(sut.invoice["performances"]),
        )
        sut()

        render_plain_text.has_called_assert_once_with(statement_data)

    amount_for_inputs = [
        (
            {"name": "Hamlet", "type": "tragedy"},
            {
                "play": {"name": "Hamlet", "type": "tragedy"},
                "playID": "hamlet",
                "audience": 55,
            },
            65000,
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {
                "play": {"name": "As You Like It", "type": "comedy"},
                "playID": "as-like",
                "audience": 35,
            },
            58000,
        ),
    ]

    @pytest.mark.parametrize("play, performance, expected", amount_for_inputs)
    def test_amount_for(self, play, performance, expected):
        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        actual = sut.amount_for(performance)

        assert actual == expected

    def test_amount_for_with_unknown_type(self):
        perfomance = (
            {
                "play": {"name": "XXXXX", "type": "XXXXX"},
                "playID": "XXX",
                "audience": 99,
            },
        )

        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        with pytest.raises(Exception):
            sut.amount_for(perfomance)

    def test_play_for(self):
        performance = {
            "play": {"name": "As You Like It", "type": "comedy"},
            "playID": "as-like",
            "audience": 35,
        }
        expected = {
            "name": "As You Like It",
            "type": "comedy",
        }

        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        actual = sut.play_for(performance)

        assert actual == expected

    def test_total_volume_credits(self):
        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        data = StatementData(
            "customer",
            sut.invoice["performances"],
            sut.total_amount(sut.invoice["performances"]),
            sut.total_volume_credits(sut.invoice["performances"]),
        )
        actual = sut.total_volume_credits(data.performances)
        expected = 47

        assert actual == expected

    def test_total_amount(self):
        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        data = StatementData(
            "customer",
            sut.invoice["performances"],
            sut.total_amount(sut.invoice["performances"]),
            sut.total_volume_credits(sut.invoice["performances"]),
        )
        actual = sut.total_amount(data.performances)
        expected = 173000

        assert actual == expected


class TestStatementDataRenderer:
    def test_render_plain_text(self):
        expected_lines = [
            "Statement for BigCo",
            "    Hamlet: $650.00 (55 seats)",
            "    As You Like It: $580.00 (35 seats)",
            "    Othello: $500.00 (40 seats)",
            "Amount owed is $1,730.00",
            "You earned 47 credits",
        ]

        statement_data = StatementDataCreator(
            fixtures.invoice, fixtures.plays
        )()
        sut = StatementRenderer()
        actual_separated = sut.render_plain_text(statement_data).split("\n")

        for actual, expected in zip(actual_separated, expected_lines):
            assert actual == expected
