from argparse import ArgumentParser

from refactoring_mf.apps.statement import (
    StatementDataCreator,
    StatementRenderer,
)
from refactoring_mf.repository.json_file import get_data_from_json


def main():
    parser = ArgumentParser()
    parser.add_argument("invoice_json_file_path")
    args = parser.parse_args()

    statement_data = StatementDataCreator(
        get_data_from_json(args.invoice_json_file_path)[0],
        get_data_from_json("plays"),
    )()
    out = StatementRenderer.render_plain_text(statement_data)

    print(out)


if __name__ == "__main__":
    main()
