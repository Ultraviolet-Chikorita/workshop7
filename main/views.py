import os
from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
import dotenv

dotenv.load_dotenv()

# Create your views here.
def home(request):
    return render(request, 'home.html')

def processName(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY', '')}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "alibaba/tongyi-deepresearch-30b-a3b:free",
            "messages": [
                {
                "role": "user",
                "content": "Summarise the following content in 5 words or less: " + name
                }
            ],
            "reasoning": {"enabled": True}
        })
        )

        # Extract the assistant message with reasoning_details
        response = response.json()
        response = response['choices'][0]['message']
        return JsonResponse({'greeting': response['content']})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def farcaster_manifest_view(request):
    """Serve the Farcaster/Base mini-app manifest at /.well-known/farcaster.json"""
    # Look for the manifest in the static folder
    data = json.loads("""{
  "accountAssociation": {
    "header": "eyJmaWQiOjE0NDcxNTcsInR5cGUiOiJhdXRoIiwia2V5IjoiMHhhMDkzMWREOTI1MTJEZjAzMzAyY0U0YTZmZjExNWI1ZEVEZDczNDA5In0",
    "payload": "eyJkb21haW4iOiJ0aGVncmVhdGVzdG1pbmlhcHBvZmFsbHRpbWUub25yZW5kZXIuY29tIn0",
    "signature": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUTrx9knvEo-ZhKQHu_TXaIipvXQPh09V79mhh2t1T6hWJJBAOjw2xnl9ZR-KEXBVUyCc-cbUSqXqLmA7miFKQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAl8ZgIay2xclZzG8RWZzuWvO8j9R0fus3XxDee9lRlVy8dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD3eyJ0eXBlIjoid2ViYXV0aG4uZ2V0IiwiY2hhbGxlbmdlIjoiMUhxaC1zeHFzdXF6QjZpbWtBbEVid1dZcklxd08wbjA0aS1DLVRjZF9jWSIsIm9yaWdpbiI6Imh0dHBzOi8va2V5cy5jb2luYmFzZS5jb20iLCJjcm9zc09yaWdpbiI6ZmFsc2UsIm90aGVyX2tleXNfY2FuX2JlX2FkZGVkX2hlcmUiOiJkbyBub3QgY29tcGFyZSBjbGllbnREYXRhSlNPTiBhZ2FpbnN0IGEgdGVtcGxhdGUuIFNlZSBodHRwczovL2dvby5nbC95YWJQZXgifQAAAAAAAAAAAA"
  },
  "miniapp": {
    "version": "1",
    "name": "The greatest Summariser mini app of all time",
    "homeUrl": "https://thegreatestminiappofalltime.onrender.com/",
    "iconUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWBuB632p-BzikvlVaPUTEubUuieUuoFM2TQ&s",
    "splashImageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWBuB632p-BzikvlVaPUTEubUuieUuoFM2TQ&s",
    "splashBackgroundColor": "#020617",
    "webhookUrl": "https://thegreatestminiappofalltime.onrender.com/api/webhook",
    "subtitle": "summarise anything",
    "description": "A mini app that can summarise any text you give it.",
    "screenshotUrls": [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWBuB632p-BzikvlVaPUTEubUuieUuoFM2TQ&s"
    ],
    "primaryCategory": "games",
    "tags": ["game", "miniapp", "base"],
    "heroImageUrl": "https://thegreatestminiappofalltime.onrender.com/api/webhook",
    "tagline": "Summarise anything, anywhere!",
    "ogTitle": "The Greatest Summariser Mini App of All Time",
    "ogDescription": "This is the greatest summariser mini app of all time. It can summarise anything you give it, in 5 words or less.",
    "ogImageUrl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWBuB632p-BzikvlVaPUTEubUuieUuoFM2TQ&s",
    "noindex": true
  }
}
""")
    return JsonResponse(data)


def webhook_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = {}
    return JsonResponse({"ok": True, "received": payload})


