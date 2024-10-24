import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-YywB5NmH5p8qN1PreJfyGqeMqK5EEPWkJII",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0.9,
    "messages":  [
      {
        "role": "system",
        "content": "You are TuneStudio"
      },
      {
        "role": "user",
        "content": "Who are you"
      }
    ],
    "model": "meta/llama-3.2-90b-vision",
    "stream": stream,
    "frequency_penalty":  0.2,
    "max_tokens": 100
}
response = requests.post(url, headers=headers, json=data)
if stream:
    for line in response.iter_lines():
        if line:
            l = line[6:]
            if l != b'[DONE]':
              print(json.loads(l))
else:
  print(response.json())