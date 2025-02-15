# unEQ

CLI application for removing EQ from video files.

## Requirements

- FFmpeg

## Installation

`pip install uneq`

## Usage

`uneq -i [video path] -e [eq config path]`

e.g. `uneq -i "C:/Videos/video.mp4" -e "C:/Program Files/EqualizerAPO/config/peace.txt"`

## Options

To see options, run `uneq --help`.

## Current limitations

- Only supports Equaliser APO configs (Peace supported)

- Only applies filters to the first audio track in the input file

- Limited to handling the following filters:

  - Preamp
  - PK (peak with Q factor)
  - LSC (low shelf with Q factor)
  - HSC (high shelf with Q factor)

- Does not support Graphic EQ
