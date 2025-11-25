# ui.py
import tkinter as tk
from tkinter import scrolledtext

from api_client import call_gemini_api
from config import API_KEY, SYSTEM_PROMPT


class BennettTkBot:
    def __init__(self, master):
        self.master = master
        master.title("Bennett Info Bot")
        master.geometry("900x600")

        self.dark_mode = True
        self.typing = False
        self.typing_dots = 0

        # Top bar
        top_bar = tk.Frame(master)
        top_bar.pack(fill=tk.X, pady=5)

        self.clear_btn = tk.Button(top_bar, text="Clear Chat", command=self.clear_chat)
        self.clear_btn.pack(side=tk.LEFT, padx=10)

        self.toggle_btn = tk.Button(
            top_bar, text="Light Mode", command=self.toggle_theme
        )
        self.toggle_btn.pack(side=tk.LEFT)

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, state=tk.DISABLED
        )
        self.chat_area.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

        # Input area
        input_frame = tk.Frame(master)
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        self.user_entry = tk.Entry(input_frame)
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.user_entry.bind("<Return>", self.send_message_event)

        self.send_button = tk.Button(
            input_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.LEFT, padx=10)

        self.apply_theme()
        self.append_bot_text("👋 Hello! I am Bennett Info Bot.")

    # ========== THEMING ==========

    def apply_theme(self):
        if self.dark_mode:
            bg, chat_bg, fg = "#1e1e1e", "#252526", "#e0e0e0"
            entry_bg, btn_bg = "#333333", "#007acc"
        else:
            bg, chat_bg, fg = "#f5f5f5", "#ffffff", "#000000"
            entry_bg, btn_bg = "#ffffff", "#1976d2"

        self.master.configure(bg=bg)
        self.chat_area.configure(bg=chat_bg, fg=fg, insertbackground=fg)
        self.user_entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)

        for btn in [self.send_button, self.clear_btn, self.toggle_btn]:
            btn.configure(bg=btn_bg, fg="white", relief=tk.FLAT)

        self.toggle_btn.config(text="Light Mode" if self.dark_mode else "Dark Mode")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    # ========== CHAT DISPLAY ==========

    def append_text(self, prefix, text):
        self.chat_area.config(state=tk.NORMAL)

        tag = "user" if prefix == "You:" else "bot"
        self.chat_area.insert(tk.END, f"{prefix} {text}\n\n", tag)

        self.chat_area.tag_configure(
            "user", foreground="#03a9f4", font=("Segoe UI", 11, "bold")
        )
        self.chat_area.tag_configure("bot", foreground="#66bb6a", font=("Segoe UI", 11))

        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def append_user_text(self, text):
        self.append_text("You:", text)

    def append_bot_text(self, text):
        self.append_text("Bot:", text)

    def clear_chat(self):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)

    # ========== SAFE TYPING ANIMATION ==========

    def start_typing(self):
        self.typing = True
        self.typing_dots = 0
        self.animate_typing()

    def animate_typing(self):
        if not self.typing:
            return

        dots = "." * (self.typing_dots % 4)
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Bot: Thinking{dots}\n\n", "bot")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

        self.typing_dots += 1
        self.master.after(400, self.animate_typing)

    def stop_typing(self):
        self.typing = False

    # ========== MESSAGE HANDLING ==========

    def send_message_event(self, event):
        self.send_message()

    def send_message(self):
        user_message = self.user_entry.get().strip()
        if not user_message:
            return

        self.user_entry.delete(0, tk.END)
        self.append_user_text(user_message)

        if user_message.lower() in ["bye", "quit", "exit"]:
            self.append_bot_text("Goodbye 👋")
            return

        self.start_typing()

        def get_response():
            bot_response = call_gemini_api(
                API_KEY,
                f"Answer using Bennett campus data: {user_message}",
                SYSTEM_PROMPT,
            )
            self.stop_typing()
            self.append_bot_text(bot_response)

        self.master.after(600, get_response)
