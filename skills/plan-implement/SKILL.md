---
name: plan-implement
description: Materialize an implementation plan.
---

Implement the referenced implementation plan. If no implementation plan is given in your context, raise.

1. Split the plan into areas. Areas are independent if they touch different files and do not depend on each other's results.
2. Spawn one `implement-review-revise` agent per area. Run independent areas in parallel and dependent areas in order. Give each lead its part of the plan, the context it needs and acceptance criteria. The leads do not see this chat.
3. If more than one area was implemented, run the /review-diff skill once over the combined diff to catch cross-area issues. Delegate the fixes to one more `implement-review-revise` agent.
4. Report to the user per area: status, deferred issues and open decisions from the lead reports.
