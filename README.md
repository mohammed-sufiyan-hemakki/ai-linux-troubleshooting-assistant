# AI Linux Troubleshooting Assistant

A beginner-friendly Linux troubleshooting tool built with Python and a locally hosted language model through Ollama.

## Features

- Provides diagnostic guidance for common Linux issues.
- Includes rule-based checks for Nginx, file permissions, DNS resolution, and slow system performance.
- Uses a local language model to answer other Linux troubleshooting questions.
- Maintains recent conversation context for follow-up questions.
- Prioritizes safe, read-only diagnostic commands.

## Technologies

- Python
- Linux / Ubuntu
- Ollama
- Qwen 2.5 (1.5B)

## Requirements

- Python 3
- Ollama installed and running
- The `qwen2.5:1.5b` model downloaded in Ollama

## Run the Project

1. Clone or download this repository.
2. Start Ollama and ensure the configured Ollama API URL in `app.py` is reachable.
3. Open a terminal in the project directory.
4. Activate your virtual environment if you have created one:

   ```bash
   source .venv/bin/activate
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Describe a Linux problem and follow the diagnostic guidance. Type `exit` to quit.

## Example Issues

- `Unit nginx.service could not be found`
- `Permission denied when reading a file`
- `Temporary failure in name resolution`
- `My Linux server is running slowly`

## Limitations

This is a learning and portfolio project. Diagnostic guidance may not always be correct. Review commands before running them, and do not use the tool as a replacement for production incident procedures.

The Ollama API URL in `app.py` may need to be adjusted for your own machine.

## Future Improvements

- Add automated tests.
- Improve diagnostic accuracy and error handling.
- Add support for more common Linux troubleshooting scenarios.
