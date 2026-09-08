---
name: ci-monitor
description: Watch the CI on GitHub for a pull request (PR) with a background Monitor that emits each check result as an event. Fix the PR until all checks pass.
---

# CI Monitor

Arm a background `Monitor` to watch the CI status of the PR and report failures and successes to you as events. The Monitor only reports; you do the fixes. Fix the PR until the CI turns green or leaves no way to improve without PR-unrelated changes.

Run the Monitor with a poll loop over `gh pr checks` that emits one line per terminal check result and exits when the run completes. Cover every terminal state, not just success, so a crash or cancel is not silent. Use a poll interval of 30s or more for the GitHub API.

```bash
prev=""
while true; do
  s=$(gh pr checks <PR> --json name,bucket 2>/dev/null || echo "[]")
  cur=$(jq -r '.[] | select(.bucket!="pending") | "\(.name): \(.bucket)"' <<<"$s" | sort)
  comm -13 <(echo "$prev") <(echo "$cur")
  prev=$cur
  jq -e 'length>0 and all(.[]; .bucket!="pending")' <<<"$s" >/dev/null && break
  sleep 30
done
```

Set `persistent: true` so the watch survives across your fix iterations. Re-arm the Monitor after you push a fix to watch the next run. Stop it with `TaskStop` once the CI is green.
