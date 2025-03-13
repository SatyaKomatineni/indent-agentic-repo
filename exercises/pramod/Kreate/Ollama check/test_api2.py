# How do I encapsulate this connecction to Llama so it can be used in crewAI framework
import requests

# Ollama API details
BASE_URL = "https://api-mac.kreatetechnologies.com/ollama"
API_KEY = "fcc1b39e-9548-4ee4-81dc-415a5d80da87"

# Define headers with API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

prompt_post = [{'role': 'system', 'content': 'You are Comedian. A hilarious AI comedian who loves making people laugh.\nYour personal goal is: Tell funny jokes\nTo give my best complete final answer to the task respond using the exact following format:\n\nThought: I now can give a great answer\nFinal Answer: Your final answer must be the great and the most complete as possible, it must be outcome described.\n\nI MUST use these formats, my job depends on it!'}, {'role': 'user', 'content': '\nCurrent Task: Generate a funny joke.\n\nThis is the expected criteria for your final answer: Print the joke\nyou MUST return the actual complete content as the final answer, not a summary.\n\nBegin! This is VERY important to you, use the tools available and give your best Final Answer, your job depends on it!\n\nThought:'}]
# Define request payload (modify as needed)
data = {
    "model": "llama3",  # Change model name if needed
    "prompt": prompt_post,
    "stream": True  # Set to True for streaming responses
}

# Make the request
response = requests.post(f"{BASE_URL}", json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Response:", response.text)
else:
    print("Error:", response.status_code, response.text)
