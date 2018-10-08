# sabergen

Beat Saber song generator

## Installation / Development

### Installing Python/Pipenv

You probably already have python.  Just make sure you have 3.5 or higher.  Only chumps use 2.\*
To get pipenv on OSX, you'll need xcode-select, then brew install pipenv.

```bash
xcode-select --install
brew install pipenv
```

For other operating systems, see [pipenv's documentation](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv).

### Installing python and dependencies

Once pipenv is installed,

```bash
cd /path/to/sabergen/
pipenv install --dev
```

You'll also need [ffmpeg](https://www.ffmpeg.org/download.html). Note that you will need
to have the libvorbis encoder.

Installing on macOS using `brew`:

```bash
brew install ffmpeg --with-theora --with-libvorbis --with-libvpx
```
