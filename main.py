import requests
import bs4


def job_parser(url: str) -> list:
    """Download html from url and parse out unordered list
    and paragraph elements from job description CSS."""
    res = requests.get(url)
    res.raise_for_status()

    job_descript = bs4.BeautifulSoup(res.text, "html.parser")
    all_lines = job_descript.select("#jobDescriptionText li, #jobDescriptionText p")
    line_list = [line.getText() for line in all_lines]
    return line_list


def clean_word(word: str) -> list:
    """Remove any special characters from word
    and splits '/' words."""
    if "/" in word:
        cleaned_words = []
        split_slash_words = word.split("/")
        for word in split_slash_words:
            cleaned_words.extend(clean_word(word))
        return cleaned_words
    lowercase_word = ""
    for char in word:
        if char.isupper():
            char = char.lower()
            lowercase_word += char
        elif char.islower():
            lowercase_word += char
    return [lowercase_word]


def word_frequency(line_list: list) -> dict:
    """Create a dictionary of word:frequency"""
    word_freq = {}
    for line in line_list:
        words_in_line = line.split()
        for word in words_in_line:
            lowercase_word_list = clean_word(word)
            for lowercase_word in lowercase_word_list:
                if lowercase_word not in word_freq:
                    word_freq[lowercase_word] = 1
                else:
                    word_freq[lowercase_word] += 1
    # Order word freq by greatest -> smallest
    word_freq = {
        word: val
        for word, val in sorted(
            word_freq.items(), key=lambda item: item[1], reverse=True
        )
    }
    return word_freq


if __name__ == "__main__":
    word_list = job_parser(
        "https://www.indeed.com/viewjob?cmp=AAA-AIR-SUPPORT,"
        "-INC&from=iaBackPress&jk=3896b9504d7af1b0"
    )
    word_freq = word_frequency(word_list)
    for word in word_freq:
        print((word, word_freq[word]))
