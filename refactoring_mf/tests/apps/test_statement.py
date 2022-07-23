from unittest.mock import patch, call
import pytest
from tests.apps import fixtures

from refactoring_mf.apps.statement import (
    StatementDataCreator,
    StatementData,
    StatementRenderer,
    PerformanceCalculator,
    PerformanceCalculatorFactory,
    TragedyCalculator,
    ComedyCalculator,
)


class TestPerformanceCalculatorFactory:
    test_cpc_input = [
        (
            "tragedy",
            {"playID": "hamlet", "audience": 55},
            {"name": "Hamlet", "type": "tragedy"},
        ),
        (
            "comedy",
            {"playID": "as-like", "audience": 35},
            {"name": "As You Like It", "type": "comedy"},
        ),
    ]

    @pytest.mark.parametrize("play_type, performance, play", test_cpc_input)
    @patch("refactoring_mf.apps.statement.ComedyCalculator")
    @patch("refactoring_mf.apps.statement.TragedyCalculator")
    def test_create(
        self,
        tragedy_calculator_cls,
        comedy_calculator_cls,
        play_type,
        performance,
        play,
    ):
        PerformanceCalculatorFactory.create(performance, play)

        if play_type == "tragedy":
            tragedy_calculator_cls.assert_called_once_with(performance, play)
        elif play_type == "comedy":
            comedy_calculator_cls.assert_called_once_with(performance, play)

    def test_create_performance_calculator_unknown_play_type(self):
        with pytest.raises(ValueError):
            PerformanceCalculatorFactory.create(
                {"playID": "XXX", "audience": 99},
                {"name": "XXXXX", "type": "X"},
            )


class TestPerformanceCalculator:
    def test_init(self):
        performance = {"playID": "hamlet", "audience": 55}
        play = {"name": "Hamlet", "type": "tragedy"}
        sut = PerformanceCalculator(performance, play)

        assert sut.performance == performance
        assert sut.play == play

    def test_amount(self):
        perfomance = (
            {
                "playID": "XXX",
                "audience": 99,
            },
        )
        play = {"name": "XXXXX", "type": "XXXXX"}

        sut = PerformanceCalculator(perfomance, play)
        with pytest.raises(NotImplementedError):
            sut.amount()

    def test_volume_credits(self):
        performance = {
            "playID": "XXX",
            "audience": 99,
        }
        play = {"name": "XXXXX", "type": "XXXXX"}
        sut = PerformanceCalculator(performance, play)
        with pytest.raises(NotImplementedError):
            sut.volume_credits()


class TestTragedyCalculator:
    def test_init(self):
        performance = {"playID": "hamlet", "audience": 55}
        play = {"name": "Hamlet", "type": "tragedy"}
        sut = TragedyCalculator(performance, play)

        assert issubclass(TragedyCalculator, PerformanceCalculator)
        assert sut.performance == performance
        assert sut.play == play

    def test_amount(self):
        play = {"name": "Hamlet", "type": "tragedy"}
        performance = {
            "play": {"name": "Hamlet", "type": "tragedy"},
            "playID": "hamlet",
            "audience": 55,
        }
        expected = 65000

        sut = TragedyCalculator(performance, play)
        actual = sut.amount()

        assert actual == expected

    def test_volume_credits(self):
        play = {"name": "Hamlet", "type": "tragedy"}
        performance = {
            "playID": "hamlet",
            "audience": 55,
        }
        expected = 25

        sut = TragedyCalculator(performance, play)
        actual = sut.volume_credits()

        assert actual == expected


class TestComedyCalculator:
    def test_init(self):
        performance = {"playID": "hamlet", "audience": 55}
        play = {"name": "Hamlet", "type": "tragedy"}
        sut = ComedyCalculator(performance, play)

        assert issubclass(ComedyCalculator, PerformanceCalculator)
        assert sut.performance == performance
        assert sut.play == play

    def test_amount(self):
        play = {"name": "As You Like It", "type": "comedy"}
        performance = {
            "play": {"name": "As You Like It", "type": "comedy"},
            "playID": "as-like",
            "audience": 35,
        }
        expected = 58000

        sut = ComedyCalculator(performance, play)
        actual = sut.amount()

        assert actual == expected

    test_comedy_volume_credits_inputs = [
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
        "play, performance, expected", test_comedy_volume_credits_inputs
    )
    def test_volume_credits(self, play, performance, expected):
        sut = ComedyCalculator(performance, play)
        actual = sut.volume_credits()

        assert actual == expected


class TestStatementDataCreator:
    @patch("refactoring_mf.apps.statement.PerformanceCalculatorFactory")
    @patch("refactoring_mf.apps.statement.StatementDataCreator.play_for")
    def test_init(self, play_for, PCFacotry):
        invoice = {
            "customer": "BigCo",
            "performances": [
                {"playID": "hamlet", "audience": 55},
            ],
        }
        plays = {
            "hamlet": {"name": "Hamlet", "type": "tragedy"},
        }
        PCFacotry.create_performance_calculator.return_value.volume_credits.return_value = (
            25
        )
        PCFacotry.create_performance_calculator.return_value.amount.return_value = (
            65000
        )
        play_for.return_value = {"name": "Hamlet", "type": "tragedy"}
        PCFacotry.create_performance_calculator.return_value.play = (
            play_for.return_value
        )

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

        sut = StatementDataCreator(invoice, plays)

        PCFacotry.create_performance_calculator.assert_has_calls(
            [
                call(
                    {"playID": "hamlet", "audience": 55},
                    {"name": "Hamlet", "type": "tragedy"},
                )
            ]
        )
        play_for.assert_called_once()
        PCFacotry.create_performance_calculator.return_value.amount.assert_called_once()
        PCFacotry.create_performance_calculator.return_value.volume_credits.assert_called_once()
        assert sut.invoice == expected_invoice
        assert sut.plays == plays

    @pytest.fixture
    @patch("refactoring_mf.apps.statement.StatementDataCreator.__init__")
    def init_statement_data_creator_mocked(self, init):
        init.return_value = None
        sut = StatementDataCreator(fixtures.invoice, fixtures.plays)
        sut.invoice = fixtures.invoice_enriched
        sut.plays = fixtures.plays
        return sut

    @patch(
        "refactoring_mf.apps.statement.StatementDataCreator.total_volume_credits"
    )
    @patch("refactoring_mf.apps.statement.StatementDataCreator.total_amount")
    @patch("refactoring_mf.apps.statement.StatementData")
    def test_call(
        self,
        StatementData,
        total_amount,
        total_volume_credits,
        init_statement_data_creator_mocked,
    ):
        sut = init_statement_data_creator_mocked
        sut()

        total_amount.assert_called_once_with(
            fixtures.invoice_enriched["performances"]
        )
        total_volume_credits.assert_called_once_with(
            fixtures.invoice_enriched["performances"]
        )
        StatementData.has_called_assert_once_with(
            fixtures.invoice_enriched["customer"],
            fixtures.invoice_enriched["performances"],
            total_amount.return_value,
            total_volume_credits.return_value,
        )

    def test_play_for(self, init_statement_data_creator_mocked):
        performance = {
            "play": {"name": "As You Like It", "type": "comedy"},
            "playID": "as-like",
            "audience": 35,
        }
        expected = {
            "name": "As You Like It",
            "type": "comedy",
        }

        sut = init_statement_data_creator_mocked
        actual = sut.play_for(performance)

        assert actual == expected

    def test_total_volume_credits(self, init_statement_data_creator_mocked):
        sut = init_statement_data_creator_mocked

        actual = sut.total_volume_credits(sut.invoice["performances"])
        expected = 47

        assert actual == expected

    def test_total_amount(self, init_statement_data_creator_mocked):
        sut = init_statement_data_creator_mocked

        actual = sut.total_amount(sut.invoice["performances"])
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

        statement_data = StatementData(
            fixtures.invoice_enriched["customer"],
            fixtures.invoice_enriched["performances"],
            173000,
            47,
        )
        sut = StatementRenderer()
        actual_separated = sut.render_plain_text(statement_data).split("\n")

        for actual, expected in zip(actual_separated, expected_lines):
            assert actual == expected
