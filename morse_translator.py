from morse_code import code


def translate(user_text):
    try:
        morse_chars = [code[ch] for ch in user_text.upper()]
        morse_text = " ".join(morse_chars)
        return morse_text
    except KeyError:
        return "Please only input letters, numbers and/or spaces"
