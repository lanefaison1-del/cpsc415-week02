# cpsc415-week02: chat client

CPSC 415 (AI Integration), Week 2 lab. `chat.py` sends one question to a language model through an OpenAI-compatible API (OpenRouter by default), prints the answer, then prints one line with the model that answered and the input and output token counts. Results of the checks are in [CHECKS.md](CHECKS.md).

## How to run it

Python 3.9 or later, standard library only. Enter the key with the hidden prompt, one line at a time, so it never appears on screen or in a file:

```
read -s "OPENROUTER_API_KEY?OpenRouter key: "
export OPENROUTER_API_KEY
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL="minimax/minimax-m3"
python3 chat.py "In one sentence, what is a context window?"
```

| Variable | Purpose |
|---|---|
| `CHAT_BASE_URL` | Where the request goes. OpenRouter: `https://openrouter.ai/api/v1`; a local Ollama server: `http://localhost:11434/v1` |
| `CHAT_MODEL` | The model slug, for example `minimax/minimax-m3` |
| `OPENROUTER_API_KEY` | The key, sent in the `Authorization` header and never stored in the repo |
| `CHAT_API_KEY` | Optional. Used instead of `OPENROUTER_API_KEY` when set; any string works for a local model |

The system message and `MAX_TOKENS` (600) are fixed constants at the top of `chat.py`. Changing the model means changing only `CHAT_MODEL`.

## What I corrected in the intent

1. Cost ceiling.The draft stated that each call "should cost cents at most.", which I didn't specify. I replaced it with "cheap models only, no actual cost ceiling," since a constraint I did not choose should not shape the build.
2. Token-count matching.I added that the program's token counts need not match OpenRouter's record exactly because i saw a small discrepancy between what the response reports and what is billed would not indicate a fault in the program. This turned out not to be a problem

I also resolved the draft's open questions: the program prints a clear error when an input is missing, takes the model name from the response (falling back to `CHAT_MODEL`), and joins all command-line arguments into the question. When the build plan omitted my system message and placed `max_tokens` out of scope, I added both to the intent before approving it.

## One line I can explain

```python
usage = data.get("usage") or {}
```

Every response from the API includes a `usage` block: the provider's count of `prompt_tokens` (the input I sent) and `completion_tokens` (the output the model generated). That count is what I am billed for. This line extracts the block from the response; the `or {}` ensures that if a provider omits it, the program prints `?` rather than crashing. The line that follows prints those counts, which is what I compared against OpenRouter's Logs page in CHECKS.md.

## Two models, one question

For this one question I observed the following.

| Model | Answer (short) | Input / output tokens | Observed cost (OpenRouter Logs) |
|---|---|---|---|
| `minimax/minimax-m3` | Maximum amount of text, in tokens, a large language model can consider at one time; "essentially the size of its working memory" | 201 / 142 | $0.000196 |
| `deepseek/deepseek-v4-pro-0813` | Maximum amount of text, in tokens, an AI model can consider at once | 35 / 28 | $0.000112 |

the two definitions were almost identical. MiniMax added a comparison to working memory, but it used~ five times as many output tokens. For this question, it cost about almost twice as muchh  more for a somewhat longer answer.

## Local model

I do not have a local model installed.
