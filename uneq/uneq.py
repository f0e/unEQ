import re
import shlex
import shutil
from pathlib import Path

from ffmpeg_progress_yield import FfmpegProgress
from rich.progress import Progress

from . import console


def parse_eq_file(file_path):
    filters = []

    with open(file_path, "r") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                # Preamp
                preamp_match = re.match(r"Preamp: ([\-\d\.]+) dB", line)
                if preamp_match:
                    preamp_gain = float(preamp_match.group(1))

                    preamp_gain = -preamp_gain

                    filter_str = f"volume={preamp_gain}dB"
                    filters.append(filter_str)

                    continue

                # Filters
                filter_match = re.match(
                    r"Filter (\d+): ON (\w+) Fc (\d+) Hz Gain ([\-\d\.]+) dB(?: Q ([\d\.]+))?",
                    line,
                )
                if filter_match:
                    _filter_num = int(filter_match.group(1))
                    filter_type = filter_match.group(2)
                    frequency = int(filter_match.group(3))
                    gain = float(filter_match.group(4))
                    q_value = float(filter_match.group(5)) if filter_match.group(5) else None

                    gain = -gain

                    if filter_type == "PK":
                        filter_str = f"equalizer=f={frequency}:width_type=q:width={q_value}:gain={gain}"
                    elif filter_type == "LSC":
                        filter_str = f"lowshelf=f={frequency}:width_type=q:width={q_value}:gain={gain}"
                    elif filter_type == "HSC":
                        filter_str = f"highshelf=f={frequency}:width_type=q:width={q_value}:gain={gain}"

                    filters.append(filter_str)

                    continue

    return ",".join(filters)


def generate_ffmpeg_command(input_path: Path, eq_file_path: Path):
    filters_command = parse_eq_file(eq_file_path)

    output_path = input_path.parent / f"uneq_{input_path.name}"

    return (
        f'ffmpeg -y -i "{input_path}" -map 0 -c:v copy -filter:a:0 "{filters_command}" "{output_path}"',
        output_path,
    )


def uneq(input_path: Path, eq_file_path: Path, copy_meta: bool):
    console.print(f"Running uneq for file [dim]{input_path}[/dim] with EQ loaded from [dim]{eq_file_path}[/dim]")

    ffmpeg_command, output_path = generate_ffmpeg_command(input_path, eq_file_path)

    with Progress(console=console) as progress:
        task = progress.add_task("[red]Encoding...", total=100)

        ff = FfmpegProgress(shlex.split(ffmpeg_command))

        for ff_progress in ff.run_command_with_progress():
            progress.update(task, completed=ff_progress)

    if copy_meta:
        # Copy metadata (modified date etc)
        shutil.copystat(input_path, output_path)

    console.print(f"Done, wrote output file to [dim]{output_path}[/dim]")
