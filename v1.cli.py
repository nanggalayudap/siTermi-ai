import os
import time
import threading
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

os.system('')

ASCII_IDLE = r'''
      _........_
   .d888888888888b.
  d888+"""""+888888.
   8b' o  o  `88888b
 _.8P (_)    .888888
d88P .____, .d88888P
888b.       :88888P'
`"""""`-----`""""' 
'''

ASCII_THINKING = r'''
      _........_
   .d888888888888b.
  d888+"""""+888888.
   8b' -  -  `88888b
 _.8P (_)    .888888
d88P  ...   .d88888P
888b.       :88888P'
`"""""`-----`""""' 
'''

ASCII_HAPPY = r'''
      _........_
   .d888888888888b.
  d888+"""""+888888.
   8b' *  *  `88888b
 _.8P (_)    .888888
d88P \____/  .d88888P
888b.       :88888P'
`"""""`-----`""""' 
'''


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def redraw(frame_text):
    print("\033[H\033[J" + frame_text, flush=True)


def chat_with_gemini(prompt):
    if gemini_client is None:
        return "Error Gemini: GEMINI_API_KEY belum diatur di file .env"
    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text or "(Gemini tidak mengembalikan teks, mungkin diblokir filter keamanan)"
    except Exception as e:
        return f"Error Gemini: {e}"


def run_with_animation(func, *args):
    """Jalankan func di thread lain sambil melooping animasi sampai selesai."""
    result = {}

    def worker():
        result["value"] = func(*args)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    frames = [ASCII_THINKING, ASCII_IDLE]
    i = 0
    while thread.is_alive():
        art = frames[i % len(frames)]
        dots = "." * (i % 4)
        redraw(f"{art}\nsiTermi sedang meracik jawaban yang okehhh :> {dots:<3}")
        time.sleep(0.4)
        i += 1

    thread.join()
    return result["value"]


def say_goodbye():
    print("\nDadah! Sampai jumpa lagi dari siTermi!")


def main():
    clear_screen()
    print(ASCII_IDLE)
    print(" HALO! Aku siTermi ")
    print(f"Model aktif: {GEMINI_MODEL}")

    while True:
        prompt = input("\nTulis pesanmu untuk siTermi (atau ketik 'exit' untuk keluar): ").strip()

        if prompt.lower() == 'exit':
            say_goodbye()
            break

        if not prompt:
            continue


        result = run_with_animation(chat_with_gemini, prompt)

        clear_screen()
        print(ASCII_HAPPY)
        if result.startswith("Error"):
            print("\n[siTermi Gagal Menjawab]:\n")
        else:
            print("\n[siTermi Berhasil Menjawab!]:\n")
        print(result)
        print("\n" + "=" * 50)
        input("\nTekan Enter untuk lanjut bertanya...")
        clear_screen()
        print(ASCII_IDLE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        say_goodbye()