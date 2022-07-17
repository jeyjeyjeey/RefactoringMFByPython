from argparse import ArgumentParser

from refactoring_mf.apps.statement import Statement
from refactoring_mf.repository.json_file import get_data_from_json

def main():
    parser = ArgumentParser()
    parser.add_argument("invoice_json_file_path")
    args = parser.parse_args()

    statement = Statement.statement(
        get_data_from_json(args.invoice_json_file_path)[0],
        get_data_from_json("plays")
    )

    print(statement)

if __name__ == "__main__":
    main()
