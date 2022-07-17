import pytest

from tests.apps import fixtures

from refactoring_mf.apps.statement import Statement


class TestStatement:
    def test_call(self):
        expected_lines = [
            "Statement for BigCo",
            "    Hamlet: $650.00 (55 seats)",
            "    As You Like It: $580.00 (35 seats)",
            "    Othello: $500.00 (40 seats)",
            "Amount owed is $1,730.00",
            "You earned 47 credits",
        ]

        sut = Statement(fixtures.invoice[0], fixtures.plays)
        actual_separated = sut().split("\n")

        for actual, expected in zip(actual_separated, expected_lines):
            assert actual == expected

    amount_for_inputs = [
        (
            {"name": "Hamlet", "type": "tragedy"},
            {"playID": "hamlet", "audience": 55},
            65000,
        ),
        (
            {"name": "As You Like It", "type": "comedy"},
            {"playID": "as-like", "audience": 35},
            58000,
        ),
    ]

    @pytest.mark.parametrize("play, performance, expected", amount_for_inputs)
    def test_amount_for(self, play, performance, expected):
        sut = Statement({}, fixtures.plays)
        actual = sut.amount_for(performance)

        assert actual == expected

    def test_amount_for_with_unknown_type(self):
        perfomance = ({"playID": "XXX", "audience": 99},)

        sut = Statement({}, fixtures.plays)
        with pytest.raises(Exception):
            sut.amount_for(perfomance)

    test_volume_credits_for_inputs = [
        (
            {"playID": "hamlet", "audience": 55},
            25,
        ),
        (
            {"playID": "as-like", "audience": 35},
            12,
        ),
        (
            {"playID": "as-like", "audience": 3},
            0,
        ),
    ]

    @pytest.mark.parametrize(
        "performance, expected", test_volume_credits_for_inputs
    )
    def test_volume_credits_for(self, performance, expected):
        sut = Statement({}, fixtures.plays)
        actual = sut.volume_credits_for(performance)

        assert actual == expected

    def test_total_volume_credits(self):
        sut = Statement(fixtures.invoice[0], fixtures.plays)
        actual = sut.total_volume_credits()
        expected = 47

        assert actual == expected
