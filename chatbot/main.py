import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Canvas

def R_ADVICE():
    return "Sure! Always aim to be the best version of yourself."

def R_EATING():
    return "I don't eat, but I love hearing about your favorite foods!"

def unknown():
    return "I'm not sure I understand. Can you rephrase that?"

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response("I'm doing fine, and you?", ['how', 'are', 'you', 'doing'], required_words=['how'])
    response("You're welcome!", ['thank', 'thanks'], single_response=True)
    response("Thank you!", ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response(R_ADVICE(), ['give', 'advice'], required_words=['advice'])
    response(R_EATING(), ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

def send_message(event=None):
    user_input = entry_box.get("1.0", 'end-1c').strip()
    if user_input:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n")
        bot_response = get_response(user_input)
        chat_window.insert(tk.END, "Bot: " + bot_response + "\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)
        entry_box.delete("1.0", tk.END)

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def create_gradient(canvas, width, height, color1, color2):
    limit = 100
    (r1, g1, b1) = canvas.winfo_rgb(color1)
    (r2, g2, b2) = canvas.winfo_rgb(color2)
    r_ratio = float(r2-r1) / limit
    g_ratio = float(g2-g1) / limit
    b_ratio = float(b2-b1) / limit

    for i in range(limit):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%04x%04x%04x" % (nr, ng, nb)
        canvas.create_rectangle(0, i * height / limit, width, (i + 1) * height / limit, outline="", fill=color)

root = tk.Tk()
root.title("Chatbot")

# Set window size to 18:9 aspect ratio (e.g., 360x720)
root.geometry("363x720")

gradient_canvas = Canvas(root, width=360, height=720)
gradient_canvas.pack(fill=tk.BOTH, expand=True)
create_gradient(gradient_canvas, 360, 720, "#FFFFFF", "#CDEDFF")

chat_window = scrolledtext.ScrolledText(gradient_canvas, wrap=tk.WORD, state=tk.DISABLED, bg="#FFFFFF", fg="#666666", font=("Inter", 14))
chat_window.place(relwidth=0.95, relheight=0.75, rely=0.05, relx=0.025)
chat_window.yview(tk.END)

entry_frame = tk.Frame(gradient_canvas, bg="#FFFFFF")
entry_frame.place(relwidth=0.95, relheight=0.1, rely=0.85, relx=0.025)

canvas = tk.Canvas(entry_frame, bg="#CDEDFF", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

round_rectangle(canvas, 10, 10, 340, 60, radius=50, fill="white")

entry_box = tk.Text(canvas, height=2, bg="white", fg="#666666", font=("Roboto", 12), bd=1, relief="flat")
entry_box.place(x=20, y=15, width=300, height=30)
entry_box.bind("<Return>", send_message)

send_button = tk.Button(entry_frame, text="Send", command=send_message, bg="white", fg="#CDEDFF", font=("Arial", 12), bd=0, relief="flat")
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()
