# sabergen

Beat Saber song generator

## Installation / Development

### Installing Python/Poetry

Ensure you have Python 3.6 or higher installed and then run:

```bash
make init
```

To invoke Poetry and initialize your virtual environment. If you don't yet have
Poetry please [see their documentation to install it](https://python-poetry.org/docs/#installation).

### Installing Dependencies

You'll also need [ffmpeg](https://www.ffmpeg.org/download.html). Note that you will need
to have the libvorbis encoder.

Installing on macOS using `brew`:

```bash
brew install ffmpeg --with-theora --with-libvorbis --with-libvpx
```
