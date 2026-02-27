#!/bin/bash
# Quick setup script to initialize and push to GitHub
# Usage: chmod +x setup_github.sh && ./setup_github.sh <your-github-username>

USERNAME=$1
REPO="multi-agent-marketing-system"

if [ -z "$USERNAME" ]; then
  echo "Usage: ./setup_github.sh <github-username>"
  exit 1
fi

echo "🔧 Initializing git repository..."
git init
git add .
git commit -m "Initial commit: Multi-Agent Marketing System (LangChain + Angular)

- Research Agent: Gathers market intelligence and synthesizes briefs
- Sentiment Agent: Analyzes audience psychology and emotional landscape  
- Content Agent: Generates complete campaign packages (tagline, email, social)
- Critic Agent: Reviews content with scoring + revision feedback loop
- FastAPI backend with SSE streaming for real-time agent events
- Angular 17 frontend with live agent activity feed
"

echo ""
echo "📦 Next steps:"
echo "1. Create repo on GitHub: https://github.com/new"
echo "   Name it: $REPO"
echo ""
echo "2. Push to GitHub:"
echo "   git remote add origin https://github.com/$USERNAME/$REPO.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "✅ Done! Share the link: https://github.com/$USERNAME/$REPO"
