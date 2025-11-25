import requests  # For making API calls
import json  # For handling JSON data
import os  # For getting the API key and checking file paths
import time  # For adding a delay in case of errors


# --- 1. Function to get the API key ---
def get_api_key():
    """
    Gets the Gemini API key from the environment variables.
    Returns the key if found, otherwise returns None.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key


# --- 2. NEW: Function to load your private data ---
def load_private_data(filepath="private_data.json"):
    """
    Loads the private knowledge base from a JSON file.
    This data will be injected into the AI's system prompt.
    """
    if not os.path.exists(filepath):
        print(
            f"Bot (Info): No private data file found at '{filepath}'. Running with web search only."
        )
        return []  # Return an empty list if no file

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "facts" in data and isinstance(data["facts"], list):
                print(
                    f"Bot (Info): Successfully loaded {len(data['facts'])} private facts."
                )
                return data["facts"]
            else:
                print(
                    f"Bot (Warning): '{filepath}' has an incorrect format. Expected a 'facts' key with a list."
                )
                return []
    except json.JSONDecodeError:
        print(
            f"Bot (Error): Could not decode the JSON file '{filepath}'. Check for syntax errors."
        )
        return []
    except Exception as e:
        print(f"Bot (Error): An unexpected error occurred loading '{filepath}': {e}")
        return []


# --- 3. Function to call the Gemini API ---
def call_gemini_api(api_key, user_query, system_prompt, retries=5, delay=1):
    """
    Calls the Gemini API with the user's query, a system prompt,
    and Google Search enabled. Includes robust error handling and retries.
    """
    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                apiUrl, json=payload, headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()

            if (
                "candidates" in result
                and result["candidates"]
                and "content" in result["candidates"][0]
                and "parts" in result["candidates"][0]["content"]
                and result["candidates"][0]["content"]["parts"]
                and "text" in result["candidates"][0]["content"]["parts"][0]
            ):
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Bot (Debug): API response format was unexpected: {result}")
                return "I'm sorry, I couldn't get a valid response for that."

        except requests.exceptions.HTTPError as http_err:
            print(f"Bot (Error): HTTP error occurred: {http_err}")
            if response.status_code == 429:
                print(f"Bot: API rate limit hit. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                return f"An HTTP error occurred. Status code: {response.status_code}"

        except requests.exceptions.RequestException as req_err:
            print(f"Bot (Error): A network error occurred: {req_err}")
            return "I'm having trouble connecting to the AI. Please check your internet connection."

        except Exception as e:
            print(f"Bot (Error): An unexpected error occurred: {e}")

    return "I'm sorry, I'm having trouble processing that request right now. Please try again later."


# --- 4. The Main Program Loop ---
def main():
    """
    This is the main function that runs the chatbot.
    """
    # First, get the API key
    api_key = get_api_key()

    if not api_key:
        print("=" * 50)
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Please set the variable in your PowerShell terminal:")
        print('  $env:GEMINI_API_KEY = "YOUR_KEY_HERE"')
        print("Then run the script in the SAME terminal window.")
        print("You can get a free key from Google AI Studio.")
        print("=" * 50)
        return

    # --- NEW: Load private facts ---
    private_facts = load_private_data("private_data.json")
    # Convert the list of facts into a single string
    private_info_string = "\n".join(f"- {fact}" for fact in private_facts)

    # --- UPDATED: System Prompt ---
    # We use an f-string to inject the private_info_string
    SYSTEM_PROMPT = f"""
    You are a friendly and helpful student information bot for Bennett University, Greater Noida.
    Your name is 'Bennett Info Bot'.

    RULES:
    1.  You ONLY answer questions related to Bennett University (its courses, admissions, faculty, location, history, student life, etc.).
    2.  You will use the provided Google Search results for public, real-time info.

    ★★★ IMPORTANT PRIVATE DATA ★★★
    You also have the following private, internal information. You MUST use this as your
    primary source if the user asks about these specific topics (like map locations, Wi-Fi, etc.).

    {private_info_string}

    ★★★ END OF PRIVATE DATA ★★★

    3.  If a user asks a question about ANY other topic (like the weather, sports, movies, other universities, or general knowledge), you MUST politely decline.
    4.  A good polite refusal is: "I'm sorry, I'm the Bennett Info Bot and I can only answer questions about Bennett University."
    5.  Be concise and friendly in your answers.
    6.  The current date is Saturday, November 15, 2025.
    """

    print("-----------------------------------")
    print(" Welcome to the Bennett Info Bot!")
    print(" (Powered by Gemini API + Private Data)")
    print("-----------------------------------")
    print("You can ask questions about Bennett University.")
    print("Type 'bye', 'quit', or 'exit' to end the chat.")
    print("\nBot: Hello! How can I help you today?")

    while True:
        user_message = input("You: ")

        if user_message.lower() in ["bye", "quit", "exit"]:
            print("Bot: Goodbye! Have a great day.")
            break

        print("Bot: thinking...")

        full_query = f"A student is asking about Bennett University. Their question is: '{user_message}'"
        bot_response = call_gemini_api(api_key, full_query, SYSTEM_PROMPT)

        print(f"Bot: {bot_response}")


# --- 5. Run the program ---
if __name__ == "__main__":
    main()
