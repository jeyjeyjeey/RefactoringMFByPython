from math import floor
from typing import Dict, Any


class Statement:
    def __init__(self, invoice: Dict[str, Any], plays: Dict[str, Any]):
        self.invoice = invoice
        self.plays = plays

    def play_for(self, playID: str) -> str:
        return self.plays[playID]

    def __call__(self) -> str:
        total_amount: int = 0
        result = f'Statement for {self.invoice["customer"]}\n'

        for performance in self.invoice["performances"]:
            result += f'    {self.play_for(performance["playID"])["name"]}: '
            result += f"{Statement.usd(self.amount_for(performance))}"
            result += f' ({performance["audience"]} seats)\n'
            total_amount += self.amount_for(performance)
        result += f"Amount owed is {Statement.usd(total_amount)}\n"
        result += f"You earned {self.total_volume_credits()} credits\n"
        return result

    def amount_for(self, performance: Dict[str, Any]):
        result = 0
        if self.play_for(performance["playID"])["type"] == "tragedy":
            result = 40000
            if performance["audience"] > 30:
                result += 1000 * (performance["audience"] - 30)
        elif self.play_for(performance["playID"])["type"] == "comedy":
            result = 30000
            if performance["audience"] > 20:
                result += 10000 + 500 * (performance["audience"] - 20)
            result += 300 * performance["audience"]
        else:
            raise Exception(
                f'Unknown type: {self.play_for(performance["playID"])["type"]}'
            )

        return result

    def volume_credits_for(self, performance: Dict[str, Any]):
        result: int = 0
        result += max(performance["audience"] - 30, 0)
        if "comedy" == self.play_for(performance["playID"])["type"]:
            result += floor(performance["audience"] / 5)
        return result

    def total_volume_credits(self):
        volume_credits: int = 0
        for performance in self.invoice["performances"]:
            volume_credits += self.volume_credits_for(performance)
        return volume_credits

    @staticmethod
    def usd(value: float) -> str:
        return f"${value/100:,.2f}"
