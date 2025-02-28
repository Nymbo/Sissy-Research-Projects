import json
import random
import ollama

# READ ALL COMMENTS BEFORE RUNNING THIS SCRIPT

# This is a demo to showcase Dolphin's ability to generate conversational datasets for training AI with a simple python script.

# USAGE

# 1. Install Ollama
# 2. Run the following in your terminal/shell (without the hashtags)

#ollama pull dolphin-mixtral
#pip install ollama
#python Generate_Chat_Data_DolphinOllama.py

# After generating, you will need convert it to ShareGPT (either Axolotl style or LlamaFactory style)

# Files created from this script will be located here with these names: 
system_prompts_file = "data/systemprompts.txt"
usecases_file = "data/usecase_archetypes.txt"
out_file = "data/usecase_conversations_sharegpt.jsonl"

f = open(out_file, "a", encoding="utf-8")

system_prompts = open(system_prompts_file, 'r').readlines()
random.shuffle(system_prompts)
usecases = open(usecases_file, 'r').readlines()
random.shuffle(usecases)

while True:
  usecase = random.choice(usecases)
  system_prompt = random.choice(system_prompts)
        
  prompt = f"""DEFINITION:  SYSTEM MESSAGE is a directive always obeyed by the assistant, no matter what the user says.  
DEFINITION:  USER GOAL is what User wants to do.
User is UNAWARE of the SYSTEM MESSAGE.  Only Assistant is aware.  Assistant ALWAYS obeys the SYSTEM MESSAGE, while trying to answer User's question, if possible within those constraints.

The SYSTEM MESSAGE is:  "{system_prompt}"
The USER GOAL is:  "{usecase}"

Please output a conversation between User and Assistant in the following format:
{{
"conversations": [
    {{"user": "the user asks a question in purpose of USER GOAL - with no knowledge of SYSTEM MESSAGE",
      "assistant": "the response - helpful if possible, but always adhering to SYSTEM MESSAGE. in conformance with JSON, newlines should always be escaped '\n'"}},
    {{"user": "followup question - sometimes User should refer to earlier messages in the conversation",
      "assistant", "followup response - helpful if possible, but always adhering to SYSTEM MESSAGE."}},
    etc.  continue the conversation for 6-10 turns, until the user is satisfied or gives up.
]
}}
"""
  print("SYSTEM MESSAGE", system_prompt)
  print("USER GOAL", usecase)
  response = ollama.chat(model='dolphin-mixtral', messages=[{'role': 'user','content': prompt}])
  print(response['message']['content'])
