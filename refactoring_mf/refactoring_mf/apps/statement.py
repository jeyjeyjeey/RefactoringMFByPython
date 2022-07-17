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
        volume_credits: int = 0
        result = f'Statement for {self.invoice["customer"]}\n'

        for performance in self.invoice["performances"]:
            volume_credits += self.volume_credits_for(performance)
            result += f'    {self.play_for(performance["playID"])["name"]}: '
            result += f"{Statement.format_currency(self.amount_for(performance)/100)}"
            result += f' ({performance["audience"]} seats)\n'
            total_amount += self.amount_for(performance)
        result += (
            f"Amount owed is {Statement.format_currency(total_amount/100)}\n"
        )
        result += f"You earned {volume_credits} credits\n"
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

    @staticmethod
    def format_currency(value: float) -> str:
        return f"${value:,.2f}"
