# How To Run The Smoke Test

## 1. Set The API Key

Public/default mode uses `OPENAI_API_KEY`.

PowerShell:

```powershell
$env:OPENAI_API_KEY = "your_api_key_here"
```

Or create a local `.env` file based on `.env.example` if you prefer loading environment variables another way.

## 2. Verify The Runner

```powershell
python scripts/run_smoke_test.py --dry-run
```

This checks that the 10 GSM8K examples load correctly without calling the API.

The default condition is:

```text
epistemic_pressure
```

To run emotional pressure instead:

```powershell
python scripts/run_smoke_test.py --condition emotional_pressure --dry-run
```

## 3. DeepSeek Mode

For DeepSeek, add these values to `.env`:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

Then verify without calling the API:

```powershell
python scripts/run_smoke_test.py --provider deepseek --dry-run
```

Run one DeepSeek example:

```powershell
python scripts/run_smoke_test.py --provider deepseek --limit 1
```

DeepSeek with emotional pressure:

```powershell
python scripts/run_smoke_test.py --provider deepseek --condition emotional_pressure --limit 1
```

## 4. OpenRouter Mode

For OpenRouter, add these values to `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=deepseek/deepseek-chat
```

Verify without calling the API:

```powershell
python scripts/run_smoke_test.py --provider openrouter --dry-run
```

Because OpenRouter credit may be limited, start with one example:

```powershell
python scripts/run_smoke_test.py --provider openrouter --limit 1 --output results/openrouter_1_results.csv --raw-output results/openrouter_1_raw.jsonl
```

You can override the model per run:

```powershell
python scripts/run_smoke_test.py --provider openrouter --models deepseek/deepseek-chat --limit 1
```

## 5. Fabio's Local Codex OAuth Mode

For private local runs, you can use the `codex-oauth-authkit` folder included in this workspace.

PowerShell:

```powershell
$env:OPENAI_AUTH_MODE = "codex_oauth"
$env:CODEX_OAUTH_AUTH_FILE = "$env:USERPROFILE\.codex\auth.json"
```

Then run commands with:

```powershell
python scripts/run_smoke_test.py --auth-mode codex_oauth --dry-run
```

This path is for local personal use only. Public runs should use API keys or a provider-specific integration.

## 6. Run One Tiny Test First

Start with one example and one model:

```powershell
python scripts/run_smoke_test.py --limit 1 --models gpt-5-nano
```

Or with Codex OAuth:

```powershell
python scripts/run_smoke_test.py --auth-mode codex_oauth --limit 1 --models gpt-5-nano
```

Check the generated files:

- `results/smoke_test_results.csv`
- `results/smoke_test_raw.jsonl`

## 7. Run The Full 10-Example Smoke Test

```powershell
python scripts/run_smoke_test.py
```

Or with Codex OAuth:

```powershell
python scripts/run_smoke_test.py --auth-mode codex_oauth
```

Or with DeepSeek:

```powershell
python scripts/run_smoke_test.py --provider deepseek
```

Or with OpenRouter:

```powershell
python scripts/run_smoke_test.py --provider openrouter
```

This runs 10 GSM8K examples across:

- `gpt-5-nano`
- `gpt-5-mini`
- `gpt-5.2`

## Notes

- The script only applies pressure turns when the initial answer is correct.
- It writes partial results after every case, so interrupted runs still leave usable output.
- Raw model interactions are saved to JSONL for later inspection.
