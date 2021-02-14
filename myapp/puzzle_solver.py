# -*- coding: UTF-8 -*-

import json
import os
from collections import Counter

SPRITE_DATA_URL = "SpriteData.json"


class PuzzleSolver:
    def __init__(self, sprite_data_url):
        self.url = sprite_data_url
        assert os.path.isfile(self.url)
        self.sprite_names = []
        self.__load_data()

        self.inverted_index = {}
        self.__create_inverted_index()

    def __load_data(self):
        with open(self.url, mode='r', encoding='UTF-8') as load_file:
            data = load_file.read()
            if data.startswith(u'\ufeff'):
                data = data.encode('utf8')[3:].decode('utf8')
            sprite_data = json.loads(data)

        sprite_list = sprite_data['spriteData']
        for sprite in sprite_list:
            self.sprite_names.append(sprite['name'])

    def __create_inverted_index(self):
        for name in self.sprite_names:
            for word in set(name):
                self.inverted_index.setdefault(word, set()).add(name)

    def __find_candidate_names(self, puzzle):
        candidate_names = set()
        puzzle = puzzle.replace("\t", "")
        for word in puzzle:
            candidate_names |= self.inverted_index.get(word, set())

        return list(candidate_names)

    def solve(self, puzzle):
        puzzle = puzzle.replace("\t", "")
        puzzle = puzzle.replace(" ", "")

        candidate_names = self.__find_candidate_names(puzzle)
        puzzle_counter = Counter(list(puzzle))
        for name in candidate_names:
            name_counter = Counter(name)
            if all(v <= puzzle_counter[k] for k, v in name_counter.items()):
                return name
        return "不存在"


if __name__ == '__main__':
    test_solver = PuzzleSolver(SPRITE_DATA_URL)
    print(test_solver.solve("帝	明	刀	风	蝶	不	鸟	喵	招  "))