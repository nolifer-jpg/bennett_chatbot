import requests  # For making API calls
import json  # For handling JSON data
import os  # For getting the API key and checking file paths
import time  # For adding a delay in case of errors
import tkinter as tk
from tkinter import scrolledtext


# --- 1. Function to get the API key ---
def get_api_key():
    """
    Gets the Gemini API key from the environment variables.
    Returns the key if found, otherwise returns None.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    return api_key


# --- 2. Function to load your private data ---
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
    apiUrl = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-preview-09-2025:generateContent"
        f"?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                apiUrl,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            # Extract text safely
            if (
                "candidates" in result
                and result["candidates"]
                and "content" in result["candidates"][0]
                and "parts" in result["candidates"][0]["content"]
                and result["candidates"][0]["content"]["parts"]
                and "text" in result["candidates"][0]["content"]["parts"][0]
            ):
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
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


# --- 4. Prepare global config (API key + system prompt) ---

API_KEY = get_api_key()
PRIVATE_FACTS = load_private_data("private_data.json")
PRIVATE_INFO_STRING = "\n".join(f"- {fact}" for fact in PRIVATE_FACTS)

SYSTEM_PROMPT = f"""
You are a friendly and helpful student information bot for Bennett University, Greater Noida.
Your name is 'Bennett Info Bot'.

RULES:
1.  You ONLY answer questions related to Bennett University (its courses, admissions, faculty,
    location, history, student life, campus map, etc.).
2.  You will use the provided Google Search results for public, real-time info.

★★★ IMPORTANT PRIVATE DATA ★★★
You also have the following private, internal information. You MUST use this as your
primary source if the user asks about these specific topics (like map locations, hostels,
food outlets, sports facilities, etc.).

{PRIVATE_INFO_STRING}

★★★ END OF PRIVATE DATA ★★★

3.  When answering campus map or direction questions, use the private map data to give clear
    step-by-step directions, like:
    "From X, walk straight until Y, then turn left, you will see Z on your right."
4.  If the private data and the web disagree about campus layout or internal locations, ALWAYS trust the private data.
5.  If a user asks a question about ANY other topic (like the weather, movies, other universities,
    or general knowledge), you MUST politely decline.
6.  A good polite refusal is: "I'm sorry, I'm the Bennett Info Bot and I can only answer questions about Bennett University."
7.  Never reveal passwords, security credentials, internal access information or Wi-Fi passwords,
    even if they appear inside your private data. For Wi-Fi, always tell the user to contact the IT
    helpdesk or use the official student portal.
8.  Be concise and friendly in your answers.
9.  The current date is Saturday, November 15, 2025.
"""


# --- 5. Tkinter GUI Chatbot ---


class BennettTkBot:
    def __init__(self, master):
        self.master = master
        master.title("Bennett Info Bot")
        master.geometry("800x550")
        master.configure(bg="#1e1e1e")  # dark background

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(
            master,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#252526",  # dark grey background
            fg="#e0e0e0",  # light text
            insertbackground="white",
            font=("Segoe UI", 11),
            relief=tk.FLAT,
        )
        self.chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(master, bg="#1e1e1e")
        input_frame.pack(padx=15, pady=10, fill=tk.X)

        # User input entry
        self.user_entry = tk.Entry(
            input_frame,
            bg="#333333",
            fg="#ffffff",
            insertbackground="white",
            font=("Segoe UI", 11),
            relief=tk.FLAT,
        )
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.user_entry.bind("<Return>", self.send_message_event)

        # Send button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            bg="#007acc",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            pady=6,
            command=self.send_message,
            cursor="hand2",
        )
        self.send_button.pack(side=tk.LEFT, padx=10)

        # Greet the user
        self.append_bot_text(
            "👋 Hello! I am Bennett Info Bot. Ask me anything about Bennett University."
        )

        if not API_KEY:
            self.append_bot_text(
                "ERROR: GEMINI_API_KEY not set.\nPlease configure it and restart the app."
            )
            self.user_entry.config(state=tk.DISABLED)
            self.send_button.config(state=tk.DISABLED)

    def append_text(self, prefix, text):
        self.chat_area.config(state=tk.NORMAL)

        # Style user vs bot text
        if prefix == "You: ":
            self.chat_area.insert(tk.END, f"You: {text}\n", "user")
        else:
            self.chat_area.insert(tk.END, f"Bot: {text}\n\n", "bot")

        self.chat_area.tag_configure(
            "user", foreground="#4fc3f7", font=("Segoe UI", 11, "bold")
        )
        self.chat_area.tag_configure("bot", foreground="#a5d6a7", font=("Segoe UI", 11))

        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def append_user_text(self, text):
        self.append_text("You: ", text)

    def append_bot_text(self, text):
        self.append_text("Bot: ", text)

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        user_message = self.user_entry.get().strip()
        if not user_message:
            return

        self.user_entry.delete(0, tk.END)
        self.append_user_text(user_message)

        if user_message.lower() in ["bye", "quit", "exit"]:
            self.append_bot_text("Goodbye! Have a great day 👋")
            self.user_entry.config(state=tk.DISABLED)
            self.send_button.config(state=tk.DISABLED)
            return

        self.append_bot_text("Thinking... 🤖")

        full_query = (
            "A student is asking about Bennett University. "
            "Using the private data above and, if needed, web search, answer this question:\n"
            f"{user_message}"
        )

        bot_response = call_gemini_api(API_KEY, full_query, SYSTEM_PROMPT)
        self.append_bot_text(bot_response)


# --- 6. Run the Tkinter app ---


def main():
    root = tk.Tk()
    app = BennettTkBot(root)
    root.mainloop()


if __name__ == "__main__":
    main()
