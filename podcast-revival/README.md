# Podcast Video Maker — Turn Source Material into a Directed Conversation

## What it does

Give your agent a video, notes, a script, or mixed source material. Tell it how long the conversation should be, how it should sound, and which questions or viewpoints matter. Podcast Revival helps the agent prepare a source-grounded script and make its voiced video with a local, recoverable media runtime.

## Who it's for

Use it when you want a voiced video conversation from source material, with a specific length, attitude or editorial question. An existing recording can become a carefully attributed continuation; notes can become a new scripted discussion. For a transcript or summary alone, use a simpler transcription or writing tool.

## Install

```bash
npx skills add m1nga/podcast-revival
```

Then ask naturally:

> Use $podcast-revival to turn these notes into a three-minute discussion. Keep a curious, skeptical tone, compare both explanations, and end with what the evidence cannot tell us.

The skill works with a capable local agent, Python 3.10+ on macOS/Linux, internet access for setup/provider calls, and your own fal account/key. Installing the skill does not include hosted generation credits. The agent handles setup; you do not need to write JSON or operate a command line after installation.

## What you receive

A finished run produces the actual video, its matching audio track, the script and source references, and an honest status/cost report. Existing-video work keeps source timestamps and speaker attribution. New text or mixed-material work starts from the requested editorial direction and an explicit speaker/voice plan.

The host agent performs material analysis, research, writing and review. The bundled runtime handles supported media steps, current prices, budget reservations and recovery. It does not independently turn arbitrary material into a complete episode without an agent, and it does not impersonate a person's endorsement.

## Limits and spending

Use material and voices you have permission to process. Explicitly authorize a total budget before paid media. The runtime keeps uncertain submissions reserved until the original request is reconciled; a timeout is not a reason to pay for a duplicate. Keys stay in a supported local store or process environment, never in the browser or production brief.

Private generation does not authorize public publication. Text and mixed-material jobs use the single-language production route after the agent prepares and reviews the script. Stock voices are synthetic presenters, not a recreation of the original author; existing custom voices require permission evidence.

## Design notes

Source preservation, editorial direction and media generation have different responsibilities. Keeping a brief, evidence, exact script review and frozen audio separate makes a revision traceable and lets a failed step resume without discarding completed work. A versioned wheel supplies the media runtime; the skill does not carry a second editable fork.

## Validation

Release 0.2.0 bundles a 68,807-byte runtime wheel with SHA-256 `9eee8ffc328497dbe3d3faedd7f5072b7fef3509d70c91f73b4dd18b4847bbe7`. It was installed with its dependencies into a clean temporary environment outside both source repositories. The installed CLI preserved a 90-second skeptical brief, refused an existing destination, passed an offline stock-voice production check, and rejected a changed script signature. Those release checks made no generation calls.

Four isolated bootstrap mechanism tests cover installation/reuse, a missing wheel, a modified wheel and preservation of an unowned directory. The frozen core is accompanied by 109 passing tests. These are setup, safety and pipeline checks; they do not establish universal voice resemblance, visible lip-sync quality or human preference.

## Author

Built by [Ming](https://github.com/m1nga). Runtime and skill behavior are maintained together; user materials, private scripts and provider receipts remain outside this public package.
