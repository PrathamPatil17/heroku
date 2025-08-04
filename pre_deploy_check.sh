#!/bin/bash

# Pre-deployment checklist for Heroku
echo "🔍 Pre-deployment checklist for Heroku..."

# Check if .env exists (shouldn't be committed)
if [ -f ".env" ]; then
    echo "⚠️  .env file found - make sure it's in .gitignore"
    if grep -q "^.env$" .gitignore; then
        echo "✅ .env is properly ignored in .gitignore"
    else
        echo "❌ .env is NOT in .gitignore - this is a security risk!"
        exit 1
    fi
else
    echo "✅ No .env file found in project root"
fi

# Check required files
echo ""
echo "📋 Checking required files..."

required_files=("Procfile" "requirements.txt" "runtime.txt" "app.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Check if git is initialized
if [ -d ".git" ]; then
    echo "✅ Git repository initialized"
else
    echo "❌ Git repository not initialized"
    echo "   Run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Check for uncommitted changes
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No uncommitted changes"
else
    echo "⚠️  Uncommitted changes found:"
    git status --porcelain
    echo "   Consider committing changes before deployment"
fi

# Check Python version
echo ""
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "   Local Python version: $python_version"

runtime_version=$(cat runtime.txt | cut -d'-' -f2)
echo "   Heroku runtime version: $runtime_version"

# Test local server
echo ""
echo "🚀 Testing local server startup..."
timeout 10s python3 -c "
import sys
sys.path.append('.')
from app import app
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get('/health')
if response.status_code == 200:
    print('✅ Local server health check passed')
else:
    print('❌ Local server health check failed')
    sys.exit(1)
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ App can start successfully"
else
    echo "⚠️  Could not test local startup (missing dependencies?)"
fi

# Check environment variables
echo ""
echo "🔧 Environment variable checklist:"
echo "   Make sure you have these ready for Heroku config:"
echo "   - OPENAI_API_KEY"
echo "   - PINECONE_API_KEY"
echo "   - PINECONE_INDEX"
echo "   - PINECONE_ENV"

echo ""
echo "🎉 Pre-deployment check complete!"
echo ""
echo "📋 Next steps for Heroku deployment:"
echo "   1. heroku login"
echo "   2. heroku create your-app-name"
echo "   3. heroku addons:create heroku-postgresql:essential-0"
echo "   4. heroku config:set OPENAI_API_KEY='your_key'"
echo "   5. heroku config:set PINECONE_API_KEY='your_key'"
echo "   6. heroku config:set PINECONE_INDEX='hackathon-doc-index'"
echo "   7. heroku config:set PINECONE_ENV='us-east-1'"
echo "   8. git push heroku main"
echo ""
echo "📚 Full guide: See HEROKU_DEPLOYMENT.md"
