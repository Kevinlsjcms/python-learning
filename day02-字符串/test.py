def char_count(s):
    count_dict = {}
    for char in s:
        if char == " ":
            continue
        lower_char = char.lower()
        if lower_char in count_dict:
            count_dict[lower_char] += 1
        else:
            count_dict[lower_char] = 1
        return count_dict