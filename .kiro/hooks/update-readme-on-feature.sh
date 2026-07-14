#!/bin/bash
# Hook: update-readme-on-feature.sh
# Triggers after shell commands. Detects git push or gh issue close
# and reminds the agent to verify if README needs updating.

# Read hook event from stdin
EVENT=$(cat)

# Extract the shell command that was executed
COMMAND=$(echo "$EVENT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Trigger on git push OR gh issue close
if [[ "$COMMAND" == *"git push"* ]]; then
  LAST_COMMIT=$(cd /Users/pimenta/community/reInventPlanning && git log -1 --pretty=%s 2>/dev/null)
  cat << EOF
📝 README UPDATE REMINDER: Code was just pushed to main.
Commit: "$LAST_COMMIT"

Please verify if the README.md needs updating to reflect this change.
Consider updating:
- Feature descriptions (if new feature)
- Top 10 tips (if new tip added)
- Project structure (if structure changed)
- Links or dates (if updated)

If the README is already up-to-date, no action needed.
EOF
elif [[ "$COMMAND" == *"gh issue close"* ]]; then
  cat << EOF
📝 README UPDATE REMINDER: An issue was just closed.

Please verify if the README.md needs updating to reflect the resolved issue.
Consider updating:
- Feature descriptions (if feature was added)
- Top 10 tips (if relevant)
- Project structure (if changed)

If the README is already up-to-date, no action needed.
EOF
fi

exit 0
