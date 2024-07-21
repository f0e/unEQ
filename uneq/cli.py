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
@click.option(
    "--copy-meta", type=bool, is_flag=True, show_default=True, default=False, help="Copy file metadata (creation date, etc)"
)
def cli(input: click.Path, eq_path: click.Path, copy_meta: bool):
    uneq(Path(input), Path(eq_path), copy_meta)


if __name__ == "__main__":
    cli()
