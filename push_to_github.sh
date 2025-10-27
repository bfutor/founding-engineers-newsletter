#!/bin/bash

# This script helps you push to GitHub and set up Actions

echo "🚀 Push to GitHub Helper"
echo "========================"
echo ""

read -p "Enter your GitHub username: " USERNAME
read -p "Enter your repository name (default: founding-engineers-newsletter): " REPO

REPO=${REPO:-founding-engineers-newsletter}

echo ""
echo "📦 Setting up remote repository..."
git remote add origin https://github.com/$USERNAME/$REPO.git

echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Done! Your code is now on GitHub."
echo ""
echo "🤖 Next Steps:"
echo "1. Go to: https://github.com/$USERNAME/$REPO/settings/secrets/actions"
echo "2. Add ANTHROPIC_API_KEY secret with your Claude API key"
echo "3. GitHub Actions will run automatically every Monday at 9 AM UTC"
echo ""
echo "📊 View Actions: https://github.com/$USERNAME/$REPO/actions"
