from dataclasses import dataclass
from math import floor
from typing import Dict, List, Any


@dataclass
class StatementData:
    customer: str
    performances: List[Dict[str, Any]]


class Statement:
    def __init__(self, invoice: Dict[str, Any], plays: Dict[str, Any]):
        self.invoice = invoice
        self.plays = plays
        self.invoice["performances"] = list(
            map(self.enrich_performance, self.invoice["performances"])
        )

    def enrich_performance(self, performance):
        result = performance.copy()
        result["play"] = self.play_for(performance)
        result["amount"] = self.amount_for(result)
        result["volume_credits"] = self.volume_credits_for(result)
        return result

    def __call__(self) -> str:
        statement_data = StatementData(
            self.invoice["customer"],
            self.invoice["performances"],
        )
        return self.render_plain_text(statement_data)

    def render_plain_text(
        self,
        data: StatementData,
    ) -> str:
        result = f"Statement for {data.customer}\n"

        for performance in data.performances:
            result += f'    {performance["play"]["name"]}: '
            result += self.usd(performance["amount"])
            result += f' ({performance["audience"]} seats)\n'
        result += "Amount owed is "
        result += f"{self.usd(self.total_amount(data.performances))}\n"
        result += "You earned "
        result += f"{self.total_volume_credits(data.performances)} credits\n"
        return result

    def amount_for(self, performance: Dict[str, Any]):
        result = 0
        if performance["play"]["type"] == "tragedy":
            result = 40000
            if performance["audience"] > 30:
                result += 1000 * (performance["audience"] - 30)
        elif performance["play"]["type"] == "comedy":
            result = 30000
            if performance["audience"] > 20:
                result += 10000 + 500 * (performance["audience"] - 20)
            result += 300 * performance["audience"]
        else:
            raise Exception(f'Unknown type: {performance["play"]["type"]}')
        return result

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

    def usd(self, value: float) -> str:
        return f"${value/100:,.2f}"
