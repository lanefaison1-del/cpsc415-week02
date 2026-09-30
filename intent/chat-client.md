# Intent: chat-client

## Goal
A command-line tool that sends one question to an AI chat model, prints the answer, and then prints a final line showing which model answered and how many input and output tokens the call used.

## Who it is for
Me, an engineering student in a computer science class learning what a chat API call actually contains. Today I use web chat interfaces, which hide the model details and token counts.

## Constraints
- Python, standard library only (`urllib`, `json`, `os`, `sys`). No packages, no pip install.
- Configuration comes only from environment variables: `CHAT_BASE_URL` (API base URL), `CHAT_MODEL` (model slug), and `OPENROUTER_API_KEY` (key). Nothing secret goes in the code or the repo.
- Models: `minimax/minimax-m3` first, then `deepseek/deepseek-v4-pro-0813`, switched by hand through `CHAT_MODEL`. Each run is one command making one call to one model.
- Cost: cheap models only. Each call should cost cents at most.
- Deadline: none.

## Not in scope
- Multi-turn conversation or chat history
- Streaming output (the full answer prints at once)
- System prompts or parameter flags (temperature, max tokens)
- Automatic fallback or retries between models
- Dollar cost calculation (token counts only)
- A GUI or web interface

## Success looks like
- With the three environment variables set, running the tool with a question prints the model's answer, then a final line with the model name and the input and output token counts.
- Running it once with `CHAT_MODEL=minimax/minimax-m3` and once with `CHAT_MODEL=deepseek/deepseek-v4-pro-0813` works both times, and the final line names the model that answered each time.
- Searching the source for the API key or any secret finds nothing. The key is read only from `OPENROUTER_API_KEY`.

## Open questions
- Confirm the interpretation of "first, then": models are switched by hand between runs, with no automatic fallback. (Interview answer: "Yes, but only once, and it's a single command that I make.")
- What should the tool do when an environment variable is missing, the question argument is missing, or the API returns an error? For example, print a clear message and exit with a non-zero code.
- Should the model name on the final line come from the API response (the model that actually answered) or from `CHAT_MODEL` (the model requested)?
- Should the question be passed as a single quoted argument, or should all command-line arguments be joined together?

**Approved by:** <your name>, <date>
