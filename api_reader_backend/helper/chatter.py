import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

# Initialize the OpenAI client with OpenRouter's base URL and API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTE_API_KEY"),
)

def chat_with_model():
    print("Welcome to the AI Chat! Type 'exit' to end the conversation.")

    # Initialize an empty list to store the conversation history
    conversation_history = []

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")

            # Exit condition
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            # Append user message to conversation history
            conversation_history.append({"role": "user", "content": user_input})

            # Call the OpenRouter API with the conversation history
            completion = client.chat.completions.create(
                model="google/gemini-2.0-flash-thinking-exp:free",
                messages=conversation_history,
            )

            # Extract the model's response
            try:
                model_response = completion.choices[0].message.content
            except:
                model_response = "I'm sorry, Serve is too busy, please try again."

            # Append the model's response to the conversation history
            conversation_history.append({"role": "assistant", "content": model_response})

            # Print the model's response
            print(f"\nAI: {model_response}")

        except OpenAIError as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")
