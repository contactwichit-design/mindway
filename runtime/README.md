# Mindway Swarm Runtime — Local Runner

This directory contains the provider-agnostic reference implementation for real multi-process Mindway swarm execution.

## What it does

`swarm_runner.py` can:

1. load one mission and bounded `/myN` cycle budget;
2. fan out independent worker workstreams concurrently;
3. persist each result and a shared `board.json`;
4. run critic, synthesizer, fixer, and independent verifier stages;
5. write `FINAL.md` only when the verifier returns a PASS verdict;
6. stop safely on cycle limits, failed stages, or missing results;
7. resume an existing run directory without repeating completed workers/stages.

## Requirements

- Python 3.11+ recommended.
- One or more AI command-line clients or local model commands that:
  - run non-interactively;
  - accept the prompt on standard input;
  - write the answer to standard output;
  - return exit code 0 on success.

The runner itself contains no AI API key and is not tied to one provider.

## Configure

Copy:

```text
runtime/swarm.example.json
```

to an untracked local config, then replace each placeholder command array:

```json
["YOUR_AI_CLI", "YOUR_NONINTERACTIVE_ARGS"]
```

with the argv for the AI CLI installed on the machine.

Do not commit credentials, tokens, API keys, or secret-bearing arguments.

## Run

```bash
python runtime/swarm_runner.py path/to/swarm.local.json
```

Outputs are stored under the configured `runs_dir`:

```text
runs/RUN-.../
  board.json
  results/
    worker-A1.json
    worker-A2.json
    ...
    critic.json
    synthesizer.json
    fixer.json
    verifier.json
  FINAL.md
```

`FINAL.md` is created only after a verifier PASS/PASS_WITH_WARNINGS leading verdict.

## Resume

Use the same mission/config and point to an existing run directory:

```bash
python runtime/swarm_runner.py path/to/swarm.local.json --resume runs/RUN-...
```

Completed worker/stage outputs are reused instead of regenerated.

## Current v1 boundary

The runner performs one default critique -> synthesis -> repair -> verification pass. If the verifier does not pass, the run ends in `REVIEW_NEEDED`; the next version should support bounded automatic repair/verify loops under remaining `/myN` budget.

Normal ChatGPT conversations cannot autonomously create new assistant turns after final output. This external runner is the mechanism that makes real multi-process continuation possible when installed and executed on an owner-controlled machine or server.

## Security

- Agent commands are argv arrays executed with `create_subprocess_exec`; no shell interpolation is used.
- Secrets must stay in environment variables or each provider's credential store.
- Treat all worker outputs as untrusted until synthesis/verification.
- Mindway approval gates still apply to destructive, publishing, account/credential, clinical, legal, business-policy, or other high-impact actions.
