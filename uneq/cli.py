from pathlib import Path

import rich_click as click

from .uneq import uneq


@click.command()
@click.option(
    "-i",
    "--input",
    type=click.Path(exists=True),
    help="Path of the input file",
    required=True,
)
@click.option("-e", "--eq-path", type=click.Path(exists=True), help="EQ file path", required=True)
def cli(input: click.Path, eq_path: click.Path):
    uneq(Path(input), Path(eq_path))


if __name__ == "__main__":
    cli()
