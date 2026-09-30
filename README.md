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

## How it was built

The intent in `intent/chat-client.md` came from a discovery interview with Claude Code (plain `claude` on my Claude subscription), which drafted it. I corrected the draft and approved it before any code was written. The code was written by Claude from the approved intent. `chat.py` itself calls OpenRouter with my OpenRouter key.

## What I corrected in the intent

1. **Cost.** The draft said each call "should cost cents at most." I never set that limit; the agent made it up. I replaced it with "cheap models only, no actual cost ceiling," because a limit I didn't choose shouldn't constrain the build.
2. **Token counts.** I added that the program's token counts don't need to match OpenRouter's record exactly. The provider can count slightly differently from what the response reports, so "close" is the right success test, not "identical." In the end they matched exactly.

I also answered the draft's open questions: print a clear error when something is missing, take the model name from the response (falling back to `CHAT_MODEL`), and join all command-line arguments into the question. When the agent's build plan left out my engineering-student system message and put `max_tokens` out of scope, I had both added to the intent before approving it.

## One line I can explain

```python
usage = data.get("usage") or {}
```

The API's reply includes a `usage` block with the tokens the provider counted for this call: `prompt_tokens` (what I sent in) and `completion_tokens` (what the model generated). That's what I'm billed for. This line pulls that block out of the reply, and `or {}` means that if a provider leaves it out, the program prints `?` instead of crashing. The next line prints those counts, which is how I compared them against the OpenRouter Logs page.

## Two models, one question

For this one question I observed the following. This is one observation, not a benchmark.

| Model | Answer (short) | Input / output tokens | Observed cost (OpenRouter Logs) |
|---|---|---|---|
| `minimax/minimax-m3` | Maximum amount of text, in tokens, a large language model can consider at one time; "essentially the size of its working memory" | 201 / 142 | $0.000196 |
| `deepseek/deepseek-v4-pro-0813` | Maximum amount of text, in tokens, an AI model can consider at once | 35 / 28 | $0.000112 |

How the answers differed: the two definitions were nearly identical. MiniMax added a "working memory" comparison but used about five times as many output tokens for it, most of them hidden reasoning, so for this question it cost more for a similar answer.

## Local model

Not tried: I don't have a local model installed.
