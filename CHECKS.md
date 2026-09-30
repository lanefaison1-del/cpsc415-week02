# Checks: chat client

The program prints what the API response says about itself. That is not evidence. Each check compares it against something the program did not produce: the OpenRouter Activity and Logs pages, or the request body itself.

Question used every time: **"In one sentence, what is a context window?"** All runs on Sept 30, 2026, about 12:31 AM.

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Question through OpenRouter | An answer and a usage line | One-sentence answer ("the maximum amount of text, measured in tokens, that a large language model can consider at one time"), then `model: minimax/minimax-m3 \| input tokens: 201 \| output tokens: 142` | Pass |
| Usage record matches | Same model; same or close token counts | OpenRouter Logs: MiniMax M3, 201 in / 142 out, $0.000196. Exact match. All four requests matched exactly; they total 973 tokens, the same as the Activity page. | Pass |
| System prompt changed | Answer style changes accordingly | With "Answer as a pirate would." the whole answer came back in pirate voice ("Arrr, matey! A context window be the grand sea o' tokens..."). Input fell from 201 to 186 tokens because the system message was shorter. | Pass |
| `max_tokens` = 20 | Truncated or empty answer; tokens still billed | No visible answer. Still billed 201 in / 20 out ($0.0000495), and Logs show finish reason `length`: the model spent all 20 tokens on hidden reasoning. | Pass |
| Model swapped (step 4) | Different model name in usage; answer may differ | Changing only `CHAT_MODEL` gave `deepseek/deepseek-v4-pro-0813`, 35 in / 28 out, matching Logs ($0.000112). Nearly the same sentence. | Pass |
| Local model (optional) | Answer from localhost; no OpenRouter entry | Not tried: no local model installed | N/A |

## The request chat.py sends

```json
{
  "model": "minimax/minimax-m3",
  "messages": [
    {"role": "system", "content": "Answer briefly for a college student studying engineering, not computer science, but who is trying to learn it."},
    {"role": "user", "content": "In one sentence, what is a context window?"}
  ],
  "max_tokens": 600
}
```

The `messages` array holds two roles: `system` sets the frame for every answer, and `user` is the question. `max_tokens` caps the output, including any hidden reasoning.

## How each check was run

1. `python3 chat.py "In one sentence, what is a context window?"` with `CHAT_MODEL=minimax/minimax-m3`.
2. Compared the program's last line with each request on the OpenRouter Logs page.
3. Ran a temporary copy of chat.py with the system message changed to "Answer as a pirate would." (chat.py itself unchanged).
4. Ran a temporary copy with `MAX_TOKENS = 20`, then checked Logs for billed tokens and the finish reason.
5. Changed only `CHAT_MODEL` to `deepseek/deepseek-v4-pro-0813` and asked the same question.

## Notes

- MiniMax used 142 output tokens for a one-sentence answer, and its 20-token run produced no visible text. It spends output tokens on hidden reasoning before answering; OpenRouter's token breakdown lists a Reasoning category. DeepSeek answered in 28 tokens.
- For the same request, MiniMax counted 201 input tokens and DeepSeek 35. I did not confirm why; each provider formats and tokenizes the request differently.
- OpenRouter sent the MiniMax requests to different providers (AtlasCloud, CoreWeave). The program only sees the model name, not the provider.
- Errors along the way: (1) `CERTIFICATE_VERIFY_FAILED`, because Python from python.org ships without trusted certificates; fixed by running its Install Certificates command. (2) `401 User not found`, because a second pasted line was captured as the key. (3) `401 Missing Authentication header`, because I entered the shortened key label from the key list instead of the full key.
