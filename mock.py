# # Problem 1
# import datetime
#
# def date(day, month, year, hour, minute):
#     if not (isinstance(day, int) and isinstance(month, int) and isinstance(year, int) and isinstance(hour,
#                                                                                                     int) and isinstance(
#             minute, int)):
#         return False
#
#     try:
#         datetime.datetime(year, month, day, hour, minute)
#         return True
#     except ValueError:
#         return False
#
# print(date(12, 12, 2023, 15, 58))
# print(date(78, 12, 1, 25, 68))
# print(date(7, "Yanvar", "2023-yil", 10, 0))

# # Problem 2
# morse = {
#     ".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e", "..-.": "f",
#     "--.": "g", "....": "h", "..": "i", ".---": "j", "-.-": "k", ".-..": "l",
#     "--": "m", "-.": "n", "---": "o", ".--.": "p", "--.-": "q", ".-.": "r",
#     "...": "s", "-": "t", "..-": "u", "...-": "v", ".--": "w", "-..-": "x",
#     "-.--": "y", "--..": "z"
# }
#
# reserve_morse ={v: k for k, v in morse.items()}
#
# def encode_to_morse(text):
#     morse_code =[]
#     for word in text.lower().split():
#         encode_word = ' '.join(reserve_morse.get(char, '') for char in word if char in reserve_morse)
#         morse_code.append(encode_word)
#     return ' '.join(morse_code)
#
# def decode_morse(code):
#     words = code.strip().split("   ")
#     decode_txt =[]
#     for word in words:
#         decode_word = ' '.join(morse.get(char, ' ')for char in word.split())
#         decode_txt.append(decode_word)
#     return ' '.join(decode_txt)
#
# text = input("Matn kiriting: ")
# morse_code = encode_to_morse(text)
#
# with open("input.txt", "w") as file:
#     file.write(morse_code)
#
# with open("input.txt", "r") as file:
#     morse_code_lines = file.readlines()
#
# decode_lines = [decode_morse(line) for line in morse_code_lines]
#
# with open("output.txt", "w") as file:
#     for line in decode_lines:
#         file.write(line + "\n")

