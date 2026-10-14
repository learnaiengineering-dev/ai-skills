---
name: business-case-builder
description: Build a business case that can win a funding decision for an AI or automation project, with options, an assumptions register, best, base and worst cases, risks and a benefits plan. Use when the user needs to justify, scope or present an AI project to a budget holder.
license: MIT
---

# Business Case Builder

Turn an idea into a short case a decision-maker can approve. Numbers alone rarely get funded; the options, assumptions, risks and the way success will be checked are what build trust.

## Rules

- **Never invent numbers.** If the user has no figure, mark the line `illustrative`, show the formula, and ask for the real value. Never present an illustrative figure as a fact.
- **Never cite a source you have not used.** For an `illustrative` row the Source column reads "Placeholder: get from <where the real figure lives>", not "Helpdesk export" or "Time sample".
- **Ask for a small decision.** A funded pilot with exit criteria is easier to approve than a full rollout.
- **Show the worst case.** A case that admits its downside is trusted more.
- **Separate capacity from cash.** Hours saved only become money if time is redeployed or spend is avoided. Say which one each benefit is.
- **Name an owner** for every benefit and every risk.

## Procedure

1. **Gather inputs** (ask only for what is missing): the problem and who has it, the current process and its cost (volume, time per item, people, error rate), the proposed change, the decision-maker and what they care about, and the budget and time window.
2. **Build the assumptions register.** One row per assumption: statement, value, source, confidence (`measured`, `estimated` or `illustrative`) and owner. Use the format in [references/assumptions-register.md](references/assumptions-register.md).
3. **Define the options.** Always include "do nothing" and a smaller pilot, plus at least one real alternative (buy, build, or a non-AI fix). Score each on cost, value, risk, time to value and effort. Every option's cost is also a row in the register, labelled with its confidence. If a cost still needs a quote, add the row as a placeholder instead of writing "needs a quote" in the table. State whether the pilot cost is inside the one-time cost or on top of it.
4. **Model three cases.** Best, base and worst, changing only the assumptions that are genuinely uncertain. Show costs (build, run, people, change management) and benefits, then payback and net value for each case. Show your arithmetic, and use the same figures in the summary and the tables (recompute after any change). For the three assumptions that move the answer most, show a one-at-a-time sensitivity table, or do not say you tested them.
5. **List risks.** Top five, each with likelihood, impact, mitigation and owner. Include a model-quality risk and an adoption risk.
6. **Write the ask.** One sentence: the decision you need, the amount, the date and the exit criteria that would stop the project.
7. **Plan benefits tracking.** For each benefit: the metric, baseline, target, who measures it, how often, and when the first check happens.

## Output

Produce, in this order:

1. **One-page summary**: decision requested, why now, recommended option, base-case numbers, worst-case numbers, top risk, exit criteria.
2. **Assumptions register** (table).
3. **Options table** (including do nothing and the pilot).
4. **Three-case summary** with arithmetic.
5. **Risks** (table).
6. **Benefits tracking plan** (table).

Finish with "What I could not verify", listing every `illustrative` or `estimated` line the user should firm up before presenting.

For API versus self-hosting model costs and a quick ROI estimate, the free calculator at https://learnaiengineering.dev/business-case can supply the numbers to feed step 2.
