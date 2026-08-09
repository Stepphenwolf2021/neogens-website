#!/bin/bash
set -e
R="$(cd "$(dirname "$0")/.." && pwd)"
cd "$R"
clear
echo "Neo Gens — publish to neogens.co"
echo "================================"
echo "repo: $R"
echo

echo "1/5  Syncing with GitHub..."
git fetch --quiet origin
LOCAL=$(git rev-parse HEAD); REMOTE=$(git rev-parse origin/HEAD 2>/dev/null || git rev-parse origin/main)
if [ "$LOCAL" != "$REMOTE" ] && git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
  echo "     Remote is ahead. Pulling..."
  git pull --quiet --ff-only
fi

echo "2/5  Running checks..."
( cd "$R" && python3 .tools/check.py ) || { echo; echo "✗ Checks failed. Nothing was published."; read -n 1 -s -r -p "Press any key to close..."; exit 1; }

if [ -z "$(git status --porcelain)" ]; then
  echo; echo "Nothing has changed since the last publish."; echo
  read -n 1 -s -r -p "Press any key to close..."; exit 0
fi

echo
echo "3/5  What will change on the live site:"
echo "--------------------------------------"
git add -A
git -c color.ui=always diff --cached --stat | sed 's/^/    /'
echo "--------------------------------------"
echo
echo "Read the list above. If you see a file you did not mean to touch, answer N."
read -r -p "Publish these changes to neogens.co? [y/N] " ans
case "$ans" in
  y|Y) ;;
  *) git reset --quiet; echo; echo "Cancelled. Nothing was published."; read -n 1 -s -r -p "Press any key to close..."; exit 0;;
esac

echo
read -r -p "4/5  One line describing this change: " msg
[ -z "$msg" ] && msg="Update site"

echo
echo "5/5  Publishing..."
git commit --quiet -m "$msg"
git push --quiet origin HEAD
echo
echo "✓ Pushed as $(git rev-parse --short HEAD). GitHub Pages usually takes 1–2 minutes."
echo
echo "  Then check:  https://www.neogens.co/"
echo "               https://www.neogens.co/th-index.html"
echo "               https://www.neogens.co/km-for-museums-and-libraries.html"
echo "               https://www.neogens.co/km-for-museums.html   (should redirect)"
echo "               https://www.neogens.co/nonsense               (should 404 properly)"
echo
read -n 1 -s -r -p "Press any key to close..."
