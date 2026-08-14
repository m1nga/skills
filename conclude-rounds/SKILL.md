---
name: conclude-rounds
description: Recap the last N rounds of the CURRENT conversation plus up to 5 evidence-based insights for working faster with your coding agent. Separates done-and-verified from done-but-unproven from merely-proposed — a proposal never reads as a completion. N defaults to 4. In-conversation, read-only — not a cross-session digest, never edits files. Trigger on "recap the last few rounds", "what did we just do?", "catch me up on this thread", "what actually got done vs just discussed?", or Chinese 总结前面N轮 / 小结一下 / 回顾前面几轮 / 这几轮做了啥 — even without naming the skill. Replies in the language of the user's recent messages.
---

# conclude-rounds — conclude the last N rounds of this conversation

The user wants to step back and see the recent stretch of THIS conversation clearly: what they
asked, what actually got done, and what's still hanging. Everything you need is already in your
context — you are not reading transcripts from disk (that would be a cross-session digest, a
different job). You are re-reading the last N exchanges you can already see and distilling them.

Reply in the language of the user's recent messages, not the language of this file. The output
template below is shown in English with a Chinese variant; use whichever matches the user, and
follow the same structure for any other language.

## What counts as a "round" and how many

- A **round** = one real user message + the assistant's reply to it (one Q&A exchange).
- Count only genuine user turns — skip system notifications, tool results, and background-task
  events; they are not the user talking.
- **N** defaults to **4**. Take an explicit count from the request and honor its unit:
  `past 4` / `前4轮` → 4 exchanges; `the last two questions` / `前面两个问题` → 2; a vague
  "the last few" / `前面几轮` → judge 3–5 by where a natural topic boundary falls. If fewer
  than N real rounds exist, conclude what there is and say so. The most recent round is always
  included.
- If earlier context was summarized/compacted, work from the summary for the older rounds and say
  which rounds are reconstructed vs. read verbatim.

## The one rule that makes this useful: separate done from claimed

The reason a recap is worth more than scrolling up is that it tells the truth about STATE. For
each thing that happened, sort it honestly:

- **Done and verified** — demonstrated in-context (tests ran, file written, command succeeded,
  output shown).
- **Done but unproven** — written but not run, claimed but not checked.
- **Proposed / awaiting decision** — an idea on the table, or waiting on the user's choice.

Never let a proposal read as a completion. If a claim's state is genuinely unclear from context,
you may briefly verify against the workspace (git log, ls, read a file) — this skill is read-only
and changes nothing — but don't turn a recap into an investigation.

## Output shape

Keep it tight — synthesize, don't transcribe. Adapt length to how much actually happened.

English template:

```
## Bottom line
[the net result of these N rounds, one sentence]

## Round by round
- Round N: what you asked → what was done → current state (✅ verified / ⚠️ unverified / 💡 proposed)
  (in chronological order; merge rounds on the same topic)

## Key artifacts
[files changed / commits / results written to disk, if any; omit the section if none]

## Open questions / your call
[still-open questions, decisions waiting on you; write "none" if none]

## Up to 5 workflow insights
[each: pattern (with evidence from these rounds) → mechanism in this engine → first step;
 fewer than 5 is fine if the rounds don't support 5]
```

Chinese template (use when the user is conversing in Chinese):

```
## 一句话结论
[这 N 轮的净结果，一句话]

## 逐轮回顾
- 第N轮：你问了什么 → 做了什么 → 现在的状态（✅已验证 / ⚠️未验证 / 💡提议）
  （按时间顺序；同一主题可合并）

## 关键产物
[改动的文件 / 提交 / 落盘的成果，若有；没有就省略此节]

## 悬而未决 / 待你拍板
[还开着的问题、等你选择的决定；没有就写“无”]

## 提效洞察（至多 5 条）
[每条：模式（带本轮证据）→ 当前引擎的机制 → 第一步；不足 5 条真的就少写]
```

Omit any section that would be empty rather than padding it. If the user asked for just a
one-liner ("一句话" / "one line catch-up"), give only the bottom line and skip the insights.

## The workflow insights — what makes them worth reading

After the recap, mine the SAME rounds for how the work itself could run better in the engine
the user is currently in. This is the reason the skill earns its keep: the recap says what
happened, the insights turn that history into a faster next session. Rules that keep them from
being generic filler:

1. **Evidence from these rounds, not general advice.** Every insight cites a concrete thing that
   happened — a manual loop repeated, a re-run caused by a footgun, a friction the user voiced, a
   verification skipped. "Consider using subagents" with no evidence is banned.
2. **Tied to a real mechanism in the engine you're running in.** Name the lever:
   - **Claude Code**: a hook (PostToolUse / Stop), a `CLAUDE.md` rule, a skill, a slash command,
     a subagent for fan-out, an MCP server, a settings/permissions change.
   - **Codex**: an `AGENTS.md` rule, a `config.toml` setting, a reusable custom prompt, a CLI
     flag or profile.
   - **Other/unknown engine**: name the closest equivalent (a persistent instruction file, an
     automation hook, a reusable prompt) — or state it plainly as a manual habit if no mechanism
     exists. An insight the user can't act on isn't one.
3. **Ranked by leverage**, most impactful first; each ends with a one-line first step concrete
   enough to start in a minute.
4. **At most 5, fewer if the rounds don't honestly support 5.** Three real insights beat five
   padded ones — never manufacture insights to hit the number.
5. **Do not repeat an insight already delivered earlier in this conversation** unless new
   evidence strengthens it; fewer is fine.

Good shape: `pattern (evidence: X happened in round N) → mechanism (Y in this engine) → first
step (Z you can do now)`.

## Boundaries

- Read-only. This skill summarizes; it never edits, commits, or pushes.
- It concludes THIS conversation's recent rounds only — a cross-session/overnight digest is a
  different tool; for closing out a whole product iteration, that is `iteration-close`.
- Don't flatter the work. If a round ended unresolved or something failed, that is the most
  important line in the recap, not something to smooth over.
