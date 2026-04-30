# Stripe Auth Checker API

A simple and fast REST API to check the validity of credit cards using the Stripe Gateway. It automatically formats output, verifies if a card is expired before processing, and returns a pretty-printed JSON response.

## Features
- **Stripe Auth Verification**: Validates whether a card is Approved, Declined, CCN Live, or CVV Live.
- **Auto-Expiry Check**: Instantly declines cards where the month and year have already expired without making an API call.
- **Multiple Formats Supported**: Easily accepts card formats like `cc|mm|yy|cvv` or space-separated variations.
- **Ready for Railway**: Pre-configured `requirements.txt` and `Procfile` make it easy to host for free on Railway.
- **Pretty JSON Responses**: Outputs clean, indented JSON for easy readability.

## Usage

Send a GET request to the `/st` endpoint passing your card details in the `cc` parameter.

**Endpoint:**
```
GET /st?cc=card|mm|yy|cvv
```

**Example Request:**
```
GET https://your-app-domain.up.railway.app/st?cc=4242424242424242|12|2026|123
```

**Example Response:**
```json
{
  "card": "4242424242424242|12|2026|123",
  "credit": "@xoxhunterxd",
  "gateway": "Stripe Auth",
  "response": "Card Declined by Issuer (Generic)",
  "status": "DECLINED",
  "time": "4.32s"
}
```

## How to Deploy to Railway

1. Push this folder to a GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
2. Log in to [Railway.app](https://railway.app/).
3. Click **New Project** -> **Deploy from GitHub repo**.
4. Select your repository. Railway will automatically detect the `Procfile` and `requirements.txt` to install and start your Flask API.
5. Once deployed, Railway will provide you with a public URL!

## Credits
Built and maintained by **@xoxhunterxd**
