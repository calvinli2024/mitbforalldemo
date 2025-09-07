# Google Agent Development Kit Demo

1. Install Ollama: https://ollama.com/

2. Use `qwen3:8b`: https://ollama.com/library/qwen3:8b
    - `$ ollama pull qwen3:8b`
    - `qwen3:8b` is the smallest tool-calling model I found that can fit on a CPU-only machine. Feel free to substitute any other larger tool-calling models if you have the hardware.

3. Run `$ uv run main.py`