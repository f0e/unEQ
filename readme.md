# unEQ

CLI application for removing EQ from video files.

## Why is this needed?

When you apply an EQ to your audio device through something like Equalizer APO, any screen recordings you make will also have the same EQ applied to their audio. This results in double-EQing when you play it back, and for anyone listening without the same EQ they'll hear your EQ which will sound weird. This is an annoying issue and not one I've seen much discussion on, leading me to create this script.

Counteracting this issue is pretty elegant though, you can just apply a new EQ to the video which is the opposite of your EQ. This restores the original correct audio. That is what this script does.

## Use case - automatically fixing OBS recordings

I've created a bash script that runs post-save in my OBS, which runs `uneq` to fix up the audio. This script is triggered by [my fork of obs-hadowplay](https://github.com/f0e/obs-hadowplay) which has a post-save script option, but I'm sure there are other methods for doing this too.

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

- Only supports Equalizer APO configs (Peace supported)

- Only applies filters to the first audio track in the input file

- Limited to handling the following filters:

  - Preamp
  - PK (peak with Q factor)
  - LSC (low shelf with Q factor)
  - HSC (high shelf with Q factor)

- Does not support Graphic EQ
