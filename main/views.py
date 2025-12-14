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