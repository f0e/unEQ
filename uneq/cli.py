import shlex
from pathlib import Path

import rich_click as click
from ffmpeg_progress_yield import FfmpegProgress
from rich.console import Console
from rich.progress import Progress

from .uneq import generate_ffmpeg_command

console = Console(highlight=False)


def uneq(input_path: Path, eq_file_path: Path):
    console.print(f"Running uneq for file [dim]{input_path}[/dim] with EQ loaded from [dim]{eq_file_path}[/dim]")

    ffmpeg_command, output_path = generate_ffmpeg_command(input_path, eq_file_path)

    with Progress(console=console) as progress:
        task = progress.add_task("[red]Encoding...", total=100)

        ff = FfmpegProgress(shlex.split(ffmpeg_command))

        for ff_progress in ff.run_command_with_progress():
            progress.update(task, completed=ff_progress)

    console.print(f"Done, wrote output file to [dim]{output_path}[/dim]")


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
