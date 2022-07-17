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

        for perf in self.invoice["performances"]:
            play = self.play_for(perf["playID"])
            
            this_amount = self.amount_for(play, perf)

            # add volume credits
            volume_credits += max(perf['audience'] - 30, 0)
            # add extra credits for every ten comedy attendees
            if 'comedy' == play["type"]:
                volume_credits += floor(perf["audience"]/5)
            result += f'    {play["name"]}: {Statement.format_currency(this_amount/100)} ({perf["audience"]} seats)\n'
            total_amount += this_amount
        result += f'Amount owed is {Statement.format_currency(total_amount/100)}\n'
        result += f'You earned {volume_credits} credits\n'
        return result

    def amount_for(self, play: Dict[str, Any], performance: Dict[str, Any]):
        result = 0
        if play["type"] == "tragedy":
            result = 40000
            if performance["audience"] > 30:
                result += 1000 * (performance["audience"] - 30)
        elif play["type"] == "comedy":
            result = 30000
            if performance['audience'] > 20:
                result += 10000 + 500 * (performance["audience"] - 20)
            result += 300 * performance["audience"]
        else:
            raise Exception(f'Unknown type: {play["type"]}')

        return result

    @staticmethod
    def format_currency(value: float) -> str:
        return f'${value:,.2f}'