# Carpet

## What is Carpet ?

Carpet is good because Carpet finds wideos in [Anthonk's explains series](https://www.youtube.com/playlist?list=PLWBKAf81pmOaP9naRiNAqug6EBnkPakvY)

## Usage

```console
usage: carpet [-h] {fetch,find} ...

positional arguments:
  {fetch,find}
    fetch             Fetch transcripts from explains videos, may take a while. This generates a .carpet.json file.
    find              Find a video (and corresponding timestamp) corresponding to a specific input text. This suppose that .carpet.json exists.

optional arguments:
  -h, --help          show this help message and exit
```

### `fetch`

```console
usage: carpet fetch [-h] [--force]

optional arguments:
  -h, --help  show this help message and exit
  --force
```

### `find`

```console
usage: carpet find [-h] text

positional arguments:
  text        text to look for

optional arguments:
  -h, --help  show this help message and exit
```

## Example :

```console
$ carpet find "carmen san diego"
There you go ! (intro to python namedtuples! (beginner - intermediate)) : https://youtu.be/iqXnBE4htUc?t=519
```