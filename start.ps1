param($port)
$env:DEVICE="127.0.0.1:$port"
uv run .\main.py