# Heroku Deployment Guide for HackRX 6.0 Document Processing API

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure git is installed and configured

## Required API Keys

Before deployment, make sure you have:

- **OpenAI API Key**: From [platform.openai.com](https://platform.openai.com)
- **Pinecone API Key**: From [pinecone.io](https://pinecone.io)
- **Pinecone Index**: Create an index named `hackathon-doc-index` in Pinecone

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create Heroku Application

```bash
heroku create your-app-name
```

Replace `your-app-name` with your desired app name (must be unique).

### 3. Add Heroku PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:essential-0 --app your-app-name
```

### 4. Set Environment Variables

```bash
# Required API Keys
heroku config:set OPENAI_API_KEY="your_openai_api_key" --app your-app-name
heroku config:set PINECONE_API_KEY="your_pinecone_api_key" --app your-app-name
heroku config:set PINECONE_INDEX="hackathon-doc-index" --app your-app-name
heroku config:set PINECONE_ENV="us-east-1" --app your-app-name

# PostgreSQL will be automatically configured by Heroku
```

### 5. Deploy to Heroku

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 6. Scale the Application

```bash
heroku ps:scale web=1 --app your-app-name
```

### 7. Open Your Application

```bash
heroku open --app your-app-name
```

## Post-Deployment

### API Documentation

Your FastAPI documentation will be available at:

- **Swagger UI**: `https://your-app-name.herokuapp.com/docs`
- **ReDoc**: `https://your-app-name.herokuapp.com/redoc`

### Health Check

Test your deployment:

```bash
curl https://your-app-name.herokuapp.com/health
```

## Environment Variables

The following environment variables are supported:

| Variable           | Required | Description                                       |
| ------------------ | -------- | ------------------------------------------------- |
| `OPENAI_API_KEY`   | Yes      | OpenAI API key for GPT-4o                         |
| `PINECONE_API_KEY` | Yes      | Pinecone API key                                  |
| `PINECONE_INDEX`   | Yes      | Pinecone index name                               |
| `PINECONE_ENV`     | Yes      | Pinecone environment                              |
| `DATABASE_URL`     | No       | PostgreSQL connection (auto-configured by Heroku) |

## Monitoring and Logs

### View Logs

```bash
heroku logs --tail --app your-app-name
```

### Monitor Performance

```bash
heroku ps --app your-app-name
```

## Scaling

### Scale Web Dynos

```bash
heroku ps:scale web=2 --app your-app-name
```

### Upgrade Database

```bash
heroku addons:upgrade heroku-postgresql:standard-0 --app your-app-name
```

## Troubleshooting

### Common Issues

1. **Build Failures**: Check `heroku logs` for dependency issues
2. **Memory Issues**: Upgrade to a larger dyno type
3. **Timeout Issues**: Ensure your requests complete within 30 seconds

### Debug Commands

```bash
# Check environment variables
heroku config --app your-app-name

# Restart application
heroku restart --app your-app-name

# Run one-off commands
heroku run python --app your-app-name
```

## Cost Optimization

- **Free Tier**: Use `hobby` dynos for development
- **Production**: Use `standard` or `performance` dynos
- **Database**: Start with `essential-0` plan, upgrade as needed

## Security Notes

- Never commit `.env` files to git
- Use Heroku Config Vars for sensitive data
- Regularly rotate API keys
- Monitor usage and costs

## API Usage

### Authentication

All API requests require a Bearer token:

```
Authorization: Bearer 880b4911f53f0dc33bb443bfc2c5831f87db7bc9d8bf084d6f42acb6918b02f7
```

### Main Endpoint

```bash
curl -X POST "https://your-app-name.herokuapp.com/hackrx/run" \
  -H "Authorization: Bearer 880b4911f53f0dc33bb443bfc2c5831f87db7bc9d8bf084d6f42acb6918b02f7" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is the main topic of this document?"]
  }'
```

## Support

For issues and questions:

- Check logs: `heroku logs --tail`
- Review documentation at `/docs`
- Monitor health at `/health`
