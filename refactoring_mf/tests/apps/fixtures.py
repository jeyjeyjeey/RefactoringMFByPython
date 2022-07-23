invoice = {
    "customer": "BigCo",
    "performances": [
        {"playID": "hamlet", "audience": 55},
        {"playID": "as-like", "audience": 35},
        {"playID": "othello", "audience": 40},
    ],
}
invoice_enriched = {
    "customer": "BigCo",
    "performances": [
        {
            "play": {"name": "Hamlet", "type": "tragedy"},
            "playID": "hamlet",
            "audience": 55,
            "amount": 65000,
            "volume_credits": 25,
        },
        {
            "play": {"name": "As You Like It", "type": "comedy"},
            "playID": "as-like",
            "audience": 35,
            "amount": 58000,
            "volume_credits": 12,
        },
        {
            "play": {"name": "Othello", "type": "tragedy"},
            "playID": "othello",
            "audience": 40,
            "amount": 50000,
            "volume_credits": 10,
        },
    ],
}
plays = {
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As You Like It", "type": "comedy"},
    "othello": {"name": "Othello", "type": "tragedy"},
}
