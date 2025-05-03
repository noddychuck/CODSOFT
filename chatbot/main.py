import datetime
import wikipedia
import webbrowser
import pywhatkit

def greet_user():
    print("👋 Hello! I am Noddy, your chatbot assistant.")
    print("I can help you with various tasks like telling the time, answering questions, or opening websites.")
    print("Type 'exit' to end the conversation.")

def get_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    return f"The current time is {time}"

def get_wikipedia_info(query):
    try:
        info = wikipedia.summary(query, sentences=1)
        return info
    except wikipedia.exceptions.DisambiguationError as e:
        return f"There are multiple results for '{query}'. Can you be more specific?"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, I couldn't reach Wikipedia. Please check your internet connection."

def open_website(website):
    webbrowser.open(website)
    return f"Opening {website}..."

def play_on_youtube(song):
    pywhatkit.playonyt(song)
    return f"Playing '{song}' on YouTube."

def chatbot_response(user_input):
    user_input = user_input.lower()

    if 'time' in user_input:
        return get_time()

    elif 'who is' in user_input:
        person = user_input.replace('who is', '').strip()
        return get_wikipedia_info(person)

    elif 'open' in user_input:
        website = user_input.replace('open', '').strip()
        return open_website(website)

    elif 'play' in user_input:
        song = user_input.replace('play', '').strip()
        return play_on_youtube(song)

    elif 'hello' in user_input or 'hi' in user_input:
        return "Hello! How can I assist you today?"

    elif 'exit' in user_input or 'quit' in user_input:
        return "Goodbye! Have a great day!"

    else:
        return "Sorry, I didn't understand that. Can you try again?"

# === MAIN ===
if __name__ == "__main__":
    greet_user()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            print("Noddy: Goodbye! Take care.")
            break

        response = chatbot_response(user_input)
        print("Noddy:", response)
