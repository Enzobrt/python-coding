def my_split(text, split_character):
    text_split = []
    for letter in text:
        if letter == split_character:
            letter_index = text.index(letter)
            text_split.append(text[:letter_index])
            text = text[letter_index + 1:]
    if text != "":
        text_split.append(text)
        text = ""
    return text_split


def my_len(text):
    len = 0
    for word in text:
        len += 1
    return len


def count_characters(text):
    characters_count = 0
    for word in text:
        characters_count += 1
    return characters_count


text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed condimentum, eros convallis ullamcorper efficitur, dolor nisl convallis mi, at placerat nulla sapien vel leo. Cras ut sem pretium, sagittis sem non, tincidunt lectus. Fusce tristique tellus nisi, sed ultricies velit mattis eu. Pellentesque id lacus non felis porta tempus. Cras nisi diam, laoreet cursus dui iaculis, convallis sodales lorem. Fusce eleifend dignissim augue. Etiam non quam sed arcu hendrerit scelerisque sed et orci. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ut dolor dolor. Ut sit amet diam erat."

# print(text.split(" "))
print(my_split(text, " "))
if text.split(" ") == my_split(text, " "):
    print("yeah")
else:
    print("nah")

print("\n")
# print(len(text.split(" ")))
print(my_len(my_split(text, " ")))
if len(text.split(" ")) == my_len(my_split(text, " ")):
    print("yeah")
else:
    print("nah")
