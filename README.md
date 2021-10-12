# album-splitter
Given a csv file and an audio file, split the audio file, into multiple tracks using `ffmpeg`.

## Test

If you have `make` installed, run

```bash
make
```

else, you can run

```bash
python albumsplit.py examples/demo.opus examples/demo.csv
```

This should produce three `.opus` files and a `log.txt` file.
