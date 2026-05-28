from collections.abc import Iterable, Iterator
import re
import os
import copy


class SentenceIterator(Iterator):
    def __init__(self, words: list[str]):
        self._sorted_words = sorted(words)
        self._index = 0

    def __copy__(self):
        new_instance = SentenceIterator([])
        new_instance._sorted_words = copy.copy(self._sorted_words)
        new_instance._index = self._index
        return new_instance

    def __str__(self) -> str:
        return f"SentenceIterator(index={self._index}, total={len(self._sorted_words)})"

    def __next__(self) -> str:
        if self._index < len(self._sorted_words):
            word = self._sorted_words[self._index]
            self._index += 1
            return word
        raise StopIteration


class Sentence(Iterable):
    def __init__(self, text_or_words=None):
        if text_or_words is None:
            self.words = []
        elif isinstance(text_or_words, Sentence):
            self.words = list(text_or_words.words)
        elif isinstance(text_or_words, list):
            self.words = [str(w) for w in text_or_words]
        elif isinstance(text_or_words, str):
            self.words = re.findall(r'\w+', text_or_words)
        else:
            raise TypeError("Недопустимий тип даних для створення Sentence")

    def __len__(self) -> int:
        return len(self.words)

    def __getitem__(self, index: int) -> str:
        return self.words[index]

    def __setitem__(self, index: int, value: str):
        self.words[index] = str(value)

    def __contains__(self, word: str) -> bool:
        return str(word) in self.words

    def __str__(self) -> str:
        return f"Sentence(words_count={len(self.words)})"

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self) -> SentenceIterator:
        return SentenceIterator(self.words)


def main():
    input_file = "input.txt"
    output_file = "output.txt"

    if not os.path.exists(input_file):
        print(f"Помилка: Вхідний файл '{input_file}' не знайдено в поточній папці.")
        return

    words_accumulator = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    words_in_line = re.findall(r'\w+', line)
                    words_accumulator.extend(words_in_line)
                except Exception as e:
                    print(f"Помилка обробки рядка {line_num}: {e}")
                    
    except (IOError, OSError) as e:
        print(f"Критична помилка доступу до файлу: {e}")
        return

    sentence_obj = Sentence(words_accumulator)

    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write("Всі слова тексту за алфавітом:\n")
            for word in sentence_obj:
                out_f.write(f"• {word}\n")
        print(f"Успішно! Результат обробки {len(sentence_obj)} слів збережено в '{output_file}'.")
    except (IOError, OSError) as e:
        print(f"Не вдалося записати результат у файл '{output_file}': {e}")


if __name__ == "__main__":
    main()
