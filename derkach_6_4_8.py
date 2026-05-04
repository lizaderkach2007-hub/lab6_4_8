import re
import copy


class SentenceIterator:

    def __init__(self, words):

        self._sorted_words = sorted(words)
        self._index = 0

    def __next__(self):
        if self._index < len(self._sorted_words):
            word = self._sorted_words[self._index]
            self._index += 1
            return word
        else:
            raise StopIteration


class Sentence:
    def __init__(self, words=None):
        if isinstance(words, Sentence):
            self.words = copy.deepcopy(words.words)
        elif isinstance(words, list):
            self.words = copy.deepcopy(words)
        else:
            self.words = []

    def __str__(self):
        return f"Sentence(words_count={len(self.words)})"

    def __iter__(self):
        return SentenceIterator(self.words)


def main():
    input_file = "input.txt"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        all_words = re.findall(r'\w+', content)

        full_sentence_obj = Sentence(all_words)


        print("Всі слова тексту за алфавітом:")

        for word in full_sentence_obj:
            print(f"• {word}")

    except FileNotFoundError:
        print(f"Помилка: Файл {input_file} не знайдено.")


if __name__ == "__main__":
    main()