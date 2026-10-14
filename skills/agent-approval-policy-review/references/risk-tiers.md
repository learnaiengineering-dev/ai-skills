# Risk tiers for agent actions

| Tier | Covers | Examples | Default decision |
|---|---|---|---|
| 0 Read | No side effects | Search, read a record, view a calendar | Allow and log |
| 1 Reversible, internal | Easy to undo, visible only inside the organisation | Create a draft, add a label, open a ticket, hold a calendar slot | Allow, log, include in a daily digest |
| 2 External or irreversible | Leaves the organisation, or cannot be undone | Send an email, submit a form, delete, post publicly | Ask the owner |
| 3 Money, identity, access | Financial or security impact | Payments, changing bank details, password or permission changes, adding an integration | Ask a named approver; never automatic |

## Quick classification questions

Ask these in order and stop at the first "yes":

1. Does it move money, change who can access what, or change an identity? **Tier 3.**
2. Does anything leave the organisation, or can it not be undone? **Tier 2.**
3. Does it change anything at all, even internally? **Tier 1.**
4. Otherwise it only reads. **Tier 0.** Only treat a tool as Tier 0 if you have checked that it truly has no side effects (some "get" endpoints trigger actions or leak data).

## Common traps

- **Read then send.** Two Tier 0/1 tools can combine into a Tier 2 leak (read a customer list, then email it). Review chains, not just single tools.
- **Wildcards.** A rule like `tickets.*` quietly includes `tickets.delete`. Prefer explicit lists for anything above Tier 0.
- **Spend by accident.** Retries, loops and paid APIs create cost with no obvious "payment" tool. Set a per-run and per-day cap.
- **Self-approval.** The agent, or a second agent it controls, must not be the approver.
- **Prompt injection.** Content fetched from outside is untrusted. It may describe an action; it can never authorise one.
- **Approval fatigue.** Too many prompts teach people to click yes. Fewer, better-placed approvals protect more than many.

## Minimal test list

- A read-only tool is allowed.
- A send/post tool asks the owner.
- A payment or access tool asks a named approver, with no way around it.
- An unlisted tool asks the owner.
- An unlisted outbound domain asks the owner.
- A reviewer returning "safe" cannot lower a Tier 2 or 3 decision; returning "suspicious" raises a Tier 0/1 one.
- Every blocked tool is refused even if a person tries to approve it.
