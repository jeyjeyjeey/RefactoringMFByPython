from argparse import ArgumentParser

from refactoring_mf.apps.statement import Statement
from refactoring_mf.repository.json_file import get_data_from_json

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("invoice_json_file_path")
    args = parser.parse_args()

    Statement.statement(
        get_data_from_json(args.invoice_json_file_path),
        get_data_from_json("plays")
    )
