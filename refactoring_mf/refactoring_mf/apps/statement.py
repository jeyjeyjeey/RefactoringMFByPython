from dataclasses import dataclass
from math import floor
from typing import Dict, List, Any


@dataclass
class StatementData:
    customer: str
    performances: List[Dict[str, Any]]
    total_amount: int
    total_volume_credits: int


class PerformanceCalculator:
    def __init__(
        self, performance: Dict[str, Any], play: Dict[str, Any]
    ) -> None:
        self.performance = performance
        self.play = play

    def amount(self):
        result = 0
        if self.play["type"] == "tragedy":
            result = 40000
            if self.performance["audience"] > 30:
                result += 1000 * (self.performance["audience"] - 30)
        elif self.play["type"] == "comedy":
            result = 30000
            if self.performance["audience"] > 20:
                result += 10000 + 500 * (self.performance["audience"] - 20)
            result += 300 * self.performance["audience"]
        else:
            raise Exception(f'Unknown type: {self.play["type"]}')
        return result


class StatementDataCreator:
    def __init__(self, invoice: Dict[str, Any], plays: Dict[str, Any]):
        self.invoice = invoice
        self.plays = plays
        self.invoice["performances"] = list(
            map(self._enrich_performance, self.invoice["performances"])
        )

    def _enrich_performance(self, performance):
        calculator = PerformanceCalculator(
            performance, self.play_for(performance)
        )
        result = performance.copy()
        result["play"] = calculator.play
        result["amount"] = calculator.amount()
        result["volume_credits"] = self.volume_credits_for(result)
        return result

    def __call__(self) -> str:
        return StatementData(
            self.invoice["customer"],
            self.invoice["performances"],
            self.total_amount(self.invoice["performances"]),
            self.total_volume_credits(self.invoice["performances"]),
        )

    def amount_for(self, performance: Dict[str, Any]):
        return PerformanceCalculator(
            performance, self.play_for(performance)
        ).amount()

    def play_for(self, performance: Dict[str, Any]) -> str:
        return self.plays[performance["playID"]]

    def volume_credits_for(self, performance: Dict[str, Any]):
        result: int = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == performance["play"]["type"]:
            result += floor(performance["audience"] / 5)
        return result

    def total_volume_credits(self, performances: List[Dict[str, Any]]):
        volume_credits: int = 0
        for performance in performances:
            volume_credits += performance["volume_credits"]
        return volume_credits

    def total_amount(self, performances: List[Dict[str, Any]]):
        total_amount: int = 0
        for performance in performances:
            total_amount += performance["amount"]
        return total_amount


class StatementRenderer:
    @staticmethod
    def render_plain_text(
        data: StatementData,
    ) -> str:
        result = f"Statement for {data.customer}\n"

        for performance in data.performances:
            result += f'    {performance["play"]["name"]}: '
            result += StatementRenderer.usd(performance["amount"])
            result += f' ({performance["audience"]} seats)\n'
        result += (
            f"Amount owed is {StatementRenderer.usd(data.total_amount)}\n"
        )
        result += f"You earned {data.total_volume_credits} credits\n"
        return result

    @staticmethod
    def usd(value: float) -> str:
        return f"${value/100:,.2f}"
