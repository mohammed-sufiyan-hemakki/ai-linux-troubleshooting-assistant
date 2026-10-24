import json
import urllib.request
import urllib.error

OLLAMA_URL = "http://172.18.13.209:11434/api/generate"
MODEL = "qwen2.5:1.5b"
MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT = """
You are a beginner-friendly Linux troubleshooting assistant.

Rules:
- Answer the user's actual question before offering further troubleshooting.
- If asked what they said earlier, summarize their earlier problem directly.
- Use conversation history to understand follow-up questions.
- For troubleshooting, give exactly one relevant diagnostic command.
- Explain that command briefly and ask for its output.
- Prefer safe, read-only commands without sudo.
- Do not guess causes without evidence.
- Do not recommend fixes before sufficient evidence.
- Never claim to execute commands on the user's machine.
- Keep answers concise and relevant.
"""

print("AI Linux Troubleshooting Assistant")
print("Type 'exit' to quit.\n")

conversation_history = []


def remember(user_message, assistant_message):
    """Save the exchange and keep recent context."""
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Assistant: {assistant_message}")
    del conversation_history[:-MAX_HISTORY_MESSAGES]


def get_rule_based_answer(problem):
    """Handle common issues with predictable diagnostic steps."""
    text = problem.lower()

    if (
        "nginx.service could not be found" in text
        or "unit nginx.service could not be found" in text
    ):
        return (
            "The Nginx service unit was not found. "
            "First, check whether Nginx is installed.\n"
            "Command: dpkg -s nginx\n"
            "Share the output before making changes."
        )

    if "permission denied" in text:
        return (
            "This may be a file or directory permission issue. "
            "Inspect the file's permissions and ownership.\n"
            "Command: ls -l /path/to/file\n"
            "Replace the placeholder with your actual file path, "
            "then share the output."
        )

    if "temporary failure in name resolution" in text:
        return (
            "This may be a DNS or name-resolution issue. "
            "First, test connectivity to an IP address.\n"
            "Command: ping -c 3 1.1.1.1\n"
            "Share the output before changing network settings."
        )

    if "linux server is running slowly" in text or "server is slow" in text:
        return (
            "Let's start by checking system load and uptime.\n"
            "Command: uptime\n"
            "Share the output so we can choose the next diagnostic step."
        )

    return None


def ask_ollama(problem):
    """Ask the local Ollama model using recent conversation context."""
    history = "\n".join(conversation_history)
    prompt = f"{history}\nUser: {problem}" if history else problem

    payload = {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read().decode("utf-8"))

    answer = result.get("response", "").strip()
    if not answer:
        raise ValueError("The model returned an empty response.")

    return answer


while True:
    try:
        problem = input("Describe your Linux problem: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break

    if problem.lower() == "exit":
        print("Goodbye!")
        break

    if not problem:
        continue

    answer = get_rule_based_answer(problem)

    if answer is None:
        try:
            answer = ask_ollama(problem)
        except (urllib.error.URLError, TimeoutError, ValueError,
                json.JSONDecodeError, KeyError) as error:
            print(f"\nCould not get a valid response from Ollama: {error}\n")
            continue

    print(f"\nAssistant: {answer}\n")
    remember(problem, answer)
