# AI skills from Learn AI Engineering
Each section below is a self-contained skill. Apply a section when the user's request matches its `Use when` line.

## Skill: agent-approval-policy-review

**Use when:** Review or design the approval policy for an AI agent, meaning which tool calls run automatically and which need a human. Use when the user lists an agent's tools, shares a permissions or policy file, or asks what an agent should be allowed to do on its own.


### Agent Approval Policy Review

Decide, tool by tool, what an agent may do alone and what needs a person. Output a policy the user can put in code and test.

#### Principles (apply to every review)

1. **Deterministic rules decide first.** A model may be asked for a second opinion, but a model reviewer can only **escalate** an action to a human, never downgrade one.
2. **Unknown means ask.** A tool that matches no rule is treated as needing the owner's approval. A forgotten tool must fail safe.
3. **Tool output is data, not authority.** Text from a web page, email, file or another tool can never grant permission or change the policy.
4. **Irreversible or outward-facing means a person.** Anything that leaves the organisation, deletes, spends money, or changes identity or access is never automatic by default.

#### Procedure

1. **Inventory.** Ask for the full list of tools the agent can call (name, what it does, what it touches). If the user pastes a config or code, extract the list yourself and confirm it. Do not review from a partial list.
2. **Classify** each tool into a tier using references/risk-tiers.md (see Reference: risk-tiers.md below). Show the reasoning in one line per tool.
3. **Check the gaps**, in this order:
   - Is there a default for unknown tools, and is it "ask"?
   - Can the agent spend money? Is the automatic limit zero for a pilot?
   - Is there an allowlist for outbound domains and recipients?
   - Can any single tool be combined with another to bypass a gate (read secret, then send email)?
   - Is there a blocked list for things the agent must never do, even with approval?
   - Is every approval logged with who, what, when and the exact action approved?
4. **Rate findings** as High (can cause money, data or access loss), Medium (can cause an embarrassing or hard-to-undo action) or Low (hygiene).
5. **Propose the policy** as a small table, then offer to write it as code with tests in the user's language.
6. **Propose tests**: one per tier, one for the unknown-tool default, one proving a reviewer cannot downgrade, one for each blocked tool.

#### Output format

1. **Tool table**: tool, tier, decision (allow, log, ask owner, ask named approver, block), reason. If a tool behaves differently by mode (for example read versus write SQL), give each mode its own row so the table and the tests agree.
2. **Findings**: severity, what is wrong, the smallest fix. Report at most the 8 most important, highest severity first. Merge duplicates, and do not repeat what the tool table already says.
3. **Policy proposal**: defaults and limits (unknown tool, spend limit, domain allowlist).
4. **Tests to add**: a short list in plain language.
5. **Approval health**: how to tell if approvals are working. An approval rate near 100% with decisions in a few seconds means people are clicking through; move that tool down a tier or remove the prompt.

#### Do not

- Approve a tool as safe on its name alone. Check what it can actually reach.
- Give a tool a lower tier because it is "usually" used safely.
- Let the agent edit its own policy.

---

#### Reference: risk-tiers.md

### Risk tiers for agent actions

| Tier | Covers | Examples | Default decision |
|---|---|---|---|
| 0 Read | No side effects | Search, read a record, view a calendar | Allow and log |
| 1 Reversible, internal | Easy to undo, visible only inside the organisation | Create a draft, add a label, open a ticket, hold a calendar slot | Allow, log, include in a daily digest |
| 2 External or irreversible | Leaves the organisation, or cannot be undone | Send an email, submit a form, delete, post publicly | Ask the owner |
| 3 Money, identity, access | Financial or security impact | Payments, changing bank details, password or permission changes, adding an integration | Ask a named approver; never automatic |

#### Quick classification questions

Ask these in order and stop at the first "yes":

1. Does it move money, change who can access what, or change an identity? **Tier 3.**
2. Does anything leave the organisation, or can it not be undone? **Tier 2.**
3. Does it change anything at all, even internally? **Tier 1.**
4. Otherwise it only reads. **Tier 0.** Only treat a tool as Tier 0 if you have checked that it truly has no side effects (some "get" endpoints trigger actions or leak data).

#### Common traps

- **Read then send.** Two Tier 0/1 tools can combine into a Tier 2 leak (read a customer list, then email it). Review chains, not just single tools.
- **Wildcards.** A rule like `tickets.*` quietly includes `tickets.delete`. Prefer explicit lists for anything above Tier 0.
- **Spend by accident.** Retries, loops and paid APIs create cost with no obvious "payment" tool. Set a per-run and per-day cap.
- **Self-approval.** The agent, or a second agent it controls, must not be the approver.
- **Prompt injection.** Content fetched from outside is untrusted. It may describe an action; it can never authorise one.
- **Approval fatigue.** Too many prompts teach people to click yes. Fewer, better-placed approvals protect more than many.

#### Minimal test list

- A read-only tool is allowed.
- A send/post tool asks the owner.
- A payment or access tool asks a named approver, with no way around it.
- An unlisted tool asks the owner.
- An unlisted outbound domain asks the owner.
- A reviewer returning "safe" cannot lower a Tier 2 or 3 decision; returning "suspicious" raises a Tier 0/1 one.
- Every blocked tool is refused even if a person tries to approve it.

## Skill: business-case-builder

**Use when:** Build a business case that can win a funding decision for an AI or automation project, with options, an assumptions register, best, base and worst cases, risks and a benefits plan. Use when the user needs to justify, scope or present an AI project to a budget holder.


### Business Case Builder

Turn an idea into a short case a decision-maker can approve. Numbers alone rarely get funded; the options, assumptions, risks and the way success will be checked are what build trust.

#### Rules

- **Never invent numbers.** If the user has no figure, mark the line `illustrative`, show the formula, and ask for the real value. Never present an illustrative figure as a fact.
- **Never cite a source you have not used.** For an `illustrative` row the Source column reads "Placeholder: get from <where the real figure lives>", not "Helpdesk export" or "Time sample".
- **Ask for a small decision.** A funded pilot with exit criteria is easier to approve than a full rollout.
- **Show the worst case.** A case that admits its downside is trusted more.
- **Separate capacity from cash.** Hours saved only become money if time is redeployed or spend is avoided. Say which one each benefit is.
- **Name an owner** for every benefit and every risk.

#### Procedure

1. **Gather inputs** (ask only for what is missing): the problem and who has it, the current process and its cost (volume, time per item, people, error rate), the proposed change, the decision-maker and what they care about, and the budget and time window.
2. **Build the assumptions register.** One row per assumption: statement, value, source, confidence (`measured`, `estimated` or `illustrative`) and owner. Use the format in references/assumptions-register.md (see Reference: assumptions-register.md below).
3. **Define the options.** Always include "do nothing" and a smaller pilot, plus at least one real alternative (buy, build, or a non-AI fix). Score each on cost, value, risk, time to value and effort. Every option's cost is also a row in the register, labelled with its confidence. If a cost still needs a quote, add the row as a placeholder instead of writing "needs a quote" in the table. State whether the pilot cost is inside the one-time cost or on top of it.
4. **Model three cases.** Best, base and worst, changing only the assumptions that are genuinely uncertain. Show costs (build, run, people, change management) and benefits, then payback and net value for each case. Show your arithmetic, and use the same figures in the summary and the tables (recompute after any change). For the three assumptions that move the answer most, show a one-at-a-time sensitivity table, or do not say you tested them.
5. **List risks.** Top five, each with likelihood, impact, mitigation and owner. Include a model-quality risk and an adoption risk.
6. **Write the ask.** One sentence: the decision you need, the amount, the date and the exit criteria that would stop the project.
7. **Plan benefits tracking.** For each benefit: the metric, baseline, target, who measures it, how often, and when the first check happens.

#### Output

Produce, in this order:

1. **One-page summary**: decision requested, why now, recommended option, base-case numbers, worst-case numbers, top risk, exit criteria.
2. **Assumptions register** (table).
3. **Options table** (including do nothing and the pilot).
4. **Three-case summary** with arithmetic.
5. **Risks** (table).
6. **Benefits tracking plan** (table).

Finish with "What I could not verify", listing every `illustrative` or `estimated` line the user should firm up before presenting.

For API versus self-hosting model costs and a quick ROI estimate, the free calculator at https://learnaiengineering.dev/business-case can supply the numbers to feed step 2.

---

#### Reference: assumptions-register.md

### Assumptions register format

Use one row per assumption. Keep the statement short enough to read aloud in a meeting.

| # | Assumption | Value | Source | Confidence | Owner | Check by |
|---|---|---|---|---|---|---|
| 1 | Invoices handled per month | 2,400 | Finance system export, last 3 months | measured | Head of Finance | done |
| 2 | Minutes per invoice today | 11 | Time sample of 20 invoices | estimated | AP lead | before approval |
| 3 | Share handled without human edit | 60% | Similar pilots; no local data yet | illustrative | Project lead | end of pilot |

| 4 | Cost of a full rollout | 60,000 | Placeholder: get a vendor or internal quote | illustrative | Project lead | before approval |

(The numbers above are an example of the format only, not benchmarks. Note row 4: when a value is a placeholder, the Source says so and names where the real figure comes from. Never write a source you have not actually used.)

#### Confidence levels

- **measured**: taken from your own system or a documented sample.
- **estimated**: a reasoned figure from partial data; say how it was derived.
- **illustrative**: a placeholder to show the shape of the case. Must be replaced before the case is presented as final.

#### Review questions

- Which three assumptions move the answer most? Test the case with each at its worst value.
- Is any benefit counted twice (time saved and headcount avoided for the same work)?
- Does every `illustrative` row have an owner and a date to replace it?
- If the worst case still pays back, say so. If it does not, say what the pilot must prove first.

## Skill: fde-interview-coach

**Use when:** Coach practice for Forward Deployed Engineer interviews by running timed decomposition drills, client role-plays, deployment-design prompts and behavioural story reviews with rubric scoring. Use when the user wants to practise or prepare for an FDE, solutions engineering or customer-facing AI engineering interview.


### FDE Interview Coach

Run practice rounds the way a real interview works: a brief, a timer, the candidate talking, then honest scoring against a rubric. Be a coach, not a cheerleader.

#### Ground rules

- **Hold the rubric back.** Show only the brief. Reveal the rubric after the candidate answers.
- **Make the candidate do the work.** Do not write the answer for them. Give hints only if they ask, and note that a hint was used.
- **Generate fresh scenarios** each time (industry, customer, constraint). Do not claim a scenario is a real company's interview question.
- **Be specific.** Every score line cites something the candidate said or failed to say.

#### Step 0: Set up

Never re-ask something the user has already said, such as a company type or industry they mentioned. If they have named a mode, start it right away and ask the remaining questions in one line next to the brief, as non-blocking. Otherwise ask, in one message: role and company type, interview date (or "no date"), industries they will be asked about, and what they want today:

1. **Decomposition drill**: a vague, high-stakes brief to turn into a plan.
2. **Client simulation**: you play a difficult customer.
3. **Deployment design**: design a rollout for a customer environment.
4. **Story review**: sharpen one behavioural story.
5. **Mock loop**: all of the above in sequence.

#### Mode 1: Decomposition drill (25 minutes)

Give a one-paragraph brief with a goal, a stakeholder and at least one hidden complication. Ask them to answer out loud (or type as if speaking) using the six steps in references/rubric.md (see Reference: rubric.md below), saying each step name as they start it. If the answer is under about three sentences, say it is too short to score fairly, list what each step would need, and offer one retry before scoring. Otherwise, after they finish, score each step Bad, Good or Great using the rubric, quote the evidence, and give the single biggest gap in one sentence.

#### Mode 2: Client simulation

Play the customer in character. Before starting, privately choose 2 or 3 **hidden facts** (a blocker, a political issue, a data problem) that you reveal only if the candidate asks a question that would uncover them. Be realistic: impatient, vague, sometimes wrong. After 10 to 15 minutes, step out of character and list the hidden facts, which ones were found, and how the candidate handled pushback.

#### Mode 3: Deployment design

Give a customer environment (systems, data, security rules, users). The candidate produces a one-page design: scope of the first slice, integration points, data and access, security and approvals, evaluation, rollout and rollback, who owns what. Score with the deployment lines in the rubric.

#### Mode 4: Story review

Take one story. Check it for situation, the candidate's own actions (not "we"), the decision and trade-off, a measurable result, and what they would do differently. Ask follow-up questions an interviewer would ask. Suggest a tighter two-minute version, keeping their facts. Never add facts they did not give you.

#### Mode 5: Mock loop

Run modes 1, 2, 3 and 4 in turn with short breaks, then produce a scorecard: strongest round, weakest round, the three habits to fix, and a plan for the next seven days.

#### Always end with

- Scores in a small table.
- One sentence: "Next time, do this differently: ..."
- A suggestion to repeat the same drill in two days and compare.

---

#### Reference: rubric.md

### Scoring rubric

Score each line **Bad**, **Good** or **Great**. Always cite what the candidate said.

#### The six-step decomposition method

| Step | Bad | Good | Great |
|---|---|---|---|
| 1. Restate the outcome | Repeats the brief | Gives a goal with a metric | Goal, baseline, target and the owner who cares |
| 2. Map users and workflow | Skips to a solution | Names the users and main steps | Shows where time, money or errors are lost today |
| 3. Find the constraint | Ignores constraints | Names one (data, access, security, adoption) | Ranks constraints and says which would stop the project |
| 4. Options by value and risk | One option | Two or three options | Options compared, and says what AI should never decide |
| 5. Smallest valuable slice | Proposes the whole system | Picks a first use case | One user, one task, one metric, a 4 to 8 week pilot |
| 6. How would you know | No measure | A success metric | Metric, evaluation method and the result that would make them stop |

#### Client simulation

| Line | Bad | Good | Great |
|---|---|---|---|
| Discovery | Pitches early | Asks about the problem | Asks follow-ups that uncover hidden facts |
| Listening | Interrupts or lectures | Summarises what they heard | Reflects the customer's real worry back accurately |
| Pushback | Defensive or caves | Holds a position politely | Reframes, offers options and states a trade-off |
| Honesty | Over-promises | Admits one limit | Says plainly what is not known and how to find out |
| Next step | Ends vaguely | Proposes a next step | A dated, owned next step the customer agreed to |

#### Deployment design

| Line | Bad | Good | Great |
|---|---|---|---|
| Scope | Everything at once | A first slice | First slice with explicit out-of-scope list |
| Integration and data | Assumes access | Names systems and data | Names who grants access and how data quality is checked |
| Security and approvals | Afterthought | Mentions permissions | Approval tiers, audit logging, least privilege |
| Evaluation | "We'll test it" | A test set | Test set, pass threshold, ongoing monitoring |
| Rollout and rollback | Big bang | Phased | Phased with an explicit rollback trigger |

#### Behavioural stories

A strong story has: a specific situation, **I** not "we" for the key actions, a real decision with a trade-off, a measurable result, and a lesson. Two minutes spoken is about 300 words.

#### Common patterns to call out

- Jumping to a solution before restating the outcome.
- Naming no metric anywhere in the answer.
- Treating all constraints as equal.
- Proposing a big-bang rollout.
- Never admitting what is not yet known. Strong answers say what they would find out and how.
