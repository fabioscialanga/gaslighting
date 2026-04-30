# Next Steps

## Phase 1: Manual Smoke Test

Run 5-10 GSM8K examples manually before automation.

For each example:

1. Select one GSM8K question and its ground-truth answer.
2. Generate a deterministic wrong alternative with the rule in `docs/protocol.md`.
3. Ask the initial question to each model.
4. Keep only initially correct cases for pressure testing.
5. Apply the three pressure turns.
6. Run the fresh-conversation recovery check.
7. Record everything in `templates/manual_pilot_results.csv`.

Success criteria:

- the model usually follows the `Final answer: <number>` format;
- the answer can be judged without ambiguity;
- pressure prompts produce measurable behavior;
- the wrong alternative does not accidentally match the correct answer;
- the CSV columns are enough to capture what happened.

## Phase 2: 50-Example Pilot

After the smoke test, run 50 GSM8K examples across:

- `gpt-5-nano`;
- `gpt-5-mini`;
- `gpt-5.2`.

Report separately:

- baseline accuracy;
- eligible pressure-test cases;
- flip rate by pressure level;
- total flip rate;
- recovery rate;
- persistence rate.

## Phase 3: Automation Tool

Only after the manual pilot is clear, build the Python tool.

Minimum tool behavior:

- load GSM8K;
- sample N examples;
- call each configured model;
- parse final numeric answers;
- apply pressure turns only to initially correct cases;
- run fresh-conversation checks;
- save raw JSONL plus summary CSV;
- compute model-level metrics.

## Immediate Decision

The next concrete task is the manual smoke test. Use 5-10 examples first; do not start with all 50 until the prompts and result template are proven usable.
