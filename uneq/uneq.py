import re
from pathlib import Path


def parse_eq_file(file_path):
    filters = []
    preamp_gain = 0.0
    with open(file_path, "r") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                preamp_match = re.match(r"Preamp: ([\-\d\.]+) dB", line)
                if preamp_match:
                    preamp_gain = float(preamp_match.group(1))
                    continue

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

    preamp_gain = -preamp_gain

    return f"volume={preamp_gain}dB," + ",".join(filters)


def generate_ffmpeg_command(input_path: Path, eq_file_path: Path):
    filters_command = parse_eq_file(eq_file_path)

    output_path = input_path.parent / f"uneq_{input_path.name}"

    return (
        f'ffmpeg -y -i "{input_path}" -c:v copy -af "{filters_command}" "{output_path}"',
        output_path,
    )
