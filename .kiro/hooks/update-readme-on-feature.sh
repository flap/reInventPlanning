#!/bin/bash
# Hook: update-readme-on-feature.sh
# Triggers after shell commands. Detects git push on main and reminds
# the agent to update the README if the commit message indicates a new
# feature or issue resolution.

# Read hook event from stdin
EVENT=$(cat)

# Extract the shell command that was executed
COMMAND=$(echo "$EVENT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

# Only act on git push commands
if [[ "$COMMAND" != *"git push"* ]]; then
  exit 0
fi

# Get the last commit message
LAST_COMMIT=$(cd /Users/pimenta/community/reInventPlanning && git log -1 --pretty=%s 2>/dev/null)

# Check if it's a feature or fix commit
if [[ "$LAST_COMMIT" == feat:* ]] || [[ "$LAST_COMMIT" == fix:* ]] || [[ "$LAST_COMMIT" == *"Closes #"* ]]; then
  # Output reminder to the agent's context
  cat << EOF
📝 README UPDATE REMINDER: A feature/fix was just pushed to main.
Commit: "$LAST_COMMIT"

Please verify if the README.md needs updating to reflect this change.
Consider updating:
- Feature descriptions (if new feature)
- Top 10 tips (if new tip added)
- Project structure (if structure changed)
- Links or dates (if updated)

If the README is already up-to-date, no action needed.
EOF
fi

exit 0
