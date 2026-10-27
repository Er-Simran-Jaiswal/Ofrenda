# Ofrenda
A private altar builder for Día de los Muertos. You describe someone you miss; a local open-weight model writes a remembrance and a gentle calaverita; you get a candle-lit altar you can save as one HTML file.

## Run it
1. Install Ollama (https://ollama.com) and pull a model: `ollama pull llama3.2`
2. `python3 ofrenda.py` (Python 3.8+, no pip installs)
3. Open http://localhost:8484

Swap models any time: `OFRENDA_MODEL=gemma3 python3 ofrenda.py`

## Why open matters here
- Private: grief and family stories never leave your machine. No account, no server logs.
- Offline: after the model is downloaded it works with the Wi-Fi off, like candles in a power cut.
- Lasting: the saved altar is a plain HTML file and the tool depends on no service that can shut down.
- Yours to change: swap in a model that writes better in Spanish, or edit the system prompt in `ofrenda.py`.

## Design choice
The model is told to use only the details you give it and never to speak as the person who died. It helps you say what you already feel.