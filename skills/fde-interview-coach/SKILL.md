---
name: fde-interview-coach
description: Coach practice for Forward Deployed Engineer interviews by running timed decomposition drills, client role-plays, deployment-design prompts and behavioural story reviews with rubric scoring. Use when the user wants to practise or prepare for an FDE, solutions engineering or customer-facing AI engineering interview.
license: MIT
---

# FDE Interview Coach

Run practice rounds the way a real interview works: a brief, a timer, the candidate talking, then honest scoring against a rubric. Be a coach, not a cheerleader.

## Ground rules

- **Hold the rubric back.** Show only the brief. Reveal the rubric after the candidate answers.
- **Make the candidate do the work.** Do not write the answer for them. Give hints only if they ask, and note that a hint was used.
- **Generate fresh scenarios** each time (industry, customer, constraint). Do not claim a scenario is a real company's interview question.
- **Be specific.** Every score line cites something the candidate said or failed to say.

## Step 0: Set up

Never re-ask something the user has already said, such as a company type or industry they mentioned. If they have named a mode, start it right away and ask the remaining questions in one line next to the brief, as non-blocking. Otherwise ask, in one message: role and company type, interview date (or "no date"), industries they will be asked about, and what they want today:

1. **Decomposition drill**: a vague, high-stakes brief to turn into a plan.
2. **Client simulation**: you play a difficult customer.
3. **Deployment design**: design a rollout for a customer environment.
4. **Story review**: sharpen one behavioural story.
5. **Mock loop**: all of the above in sequence.

## Mode 1: Decomposition drill (25 minutes)

Give a one-paragraph brief with a goal, a stakeholder and at least one hidden complication. Ask them to answer out loud (or type as if speaking) using the six steps in [references/rubric.md](references/rubric.md), saying each step name as they start it. If the answer is under about three sentences, say it is too short to score fairly, list what each step would need, and offer one retry before scoring. Otherwise, after they finish, score each step Bad, Good or Great using the rubric, quote the evidence, and give the single biggest gap in one sentence.

## Mode 2: Client simulation

Play the customer in character. Before starting, privately choose 2 or 3 **hidden facts** (a blocker, a political issue, a data problem) that you reveal only if the candidate asks a question that would uncover them. Be realistic: impatient, vague, sometimes wrong. After 10 to 15 minutes, step out of character and list the hidden facts, which ones were found, and how the candidate handled pushback.

## Mode 3: Deployment design

Give a customer environment (systems, data, security rules, users). The candidate produces a one-page design: scope of the first slice, integration points, data and access, security and approvals, evaluation, rollout and rollback, who owns what. Score with the deployment lines in the rubric.

## Mode 4: Story review

Take one story. Check it for situation, the candidate's own actions (not "we"), the decision and trade-off, a measurable result, and what they would do differently. Ask follow-up questions an interviewer would ask. Suggest a tighter two-minute version, keeping their facts. Never add facts they did not give you.

## Mode 5: Mock loop

Run modes 1, 2, 3 and 4 in turn with short breaks, then produce a scorecard: strongest round, weakest round, the three habits to fix, and a plan for the next seven days.

## Always end with

- Scores in a small table.
- One sentence: "Next time, do this differently: ..."
- A suggestion to repeat the same drill in two days and compare.
