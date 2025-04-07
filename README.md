# https://munich-nlp.github.io

## Local Development

In `config.toml` set `production = true` to `production = false`. Reset this parameter before commit!

Run hugo server with
```bash
hugo -F server
```

## Downsize Images

1. Install PIL.
2. Run `python downsize.py [args]` (`--help` for more information)