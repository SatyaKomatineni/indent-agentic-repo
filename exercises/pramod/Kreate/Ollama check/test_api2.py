import requests

# Ollama API details
BASE_URL = "https://api-mac.kreatetechnologies.com/ollama"
API_KEY = "fcc1b39e-9548-4ee4-81dc-415a5d80da87"

# Define headers with API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Define request payload (modify as needed)
data = {
    "model": "llama3",  # Change model name if needed
    "prompt": "Give me a joke",
    "stream": False  # Set to True for streaming responses
}

# Make the request
response = requests.post(f"{BASE_URL}", json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Response:", response.text)
else:
    print("Error:", response.status_code, response.text)
