# -*- coding: UTF-8 -*-
import json
import os
import psutil
import sys
import time
from collections import Counter

sprite_data_url = "SpriteData.json"
answer_url = "answer.txt"


def loads_sprite():
    with open(sprite_data_url, mode='r', encoding='UTF-8') as load_file:
        data = load_file.read()
        if data.startswith(u'\ufeff'):
            data = data.encode('utf8')[3:].decode('utf8')
        sprite_data = json.loads(data)

    sprite_list = sprite_data['spriteData']
    sprite_names, sprite_names_counter = [], []
    for sprite in sprite_list:
        sprite_names.append(sprite['name'])
        sprite_names_counter.append(Counter(sprite['name']))

    return sprite_names


def create_inverted_index(sprite_names):
    inverted_index = {}
    for name in sprite_names:
        for word in set(name):
            inverted_index.setdefault(word, set()).add(name)

    return inverted_index


def find_candidate_names(puzzle, inverted_index):
    candidate_names = set()
    puzzle = puzzle.replace("\t", "")
    for word in puzzle:
        candidate_names |= inverted_index.get(word, set())

    return list(candidate_names)


def solve_puzzle(puzzle, candidate_names):
    puzzle = puzzle.replace("\t", "")
    puzzle = puzzle.replace(" ", "")

    puzzle_counter = Counter(list(puzzle))
    for name in candidate_names:
        name_counter = Counter(name)
        if all(v <= puzzle_counter[k] for k, v in name_counter.items()):
            return name
    return "不存在"


def test_inverted_index():
    sprite_names, sprite_names_counter = loads_sprite()
    inverted_index = create_inverted_index(sprite_names)
    print(inverted_index['兔'])
    print(find_candidate_names("郎	喜	奴	乌	货	孙	娃	雨	知", inverted_index))


def main():
    sprite_names, sprite_names_counter = loads_sprite()
    print(solve_puzzle("郎	喜	奴	乌	货	孙	娃	雨	知", sprite_names))
    while True:
        try:
            puzzle = input("输入字谜: ")
            answer = solve_puzzle(puzzle, sprite_names)
            print(answer)
        except Exception as e:
            print(e)
            break


def main_v2():
    sprite_names, sprite_names_counter = loads_sprite()
    inverted_index = create_inverted_index(sprite_names)
    while True:
        try:
            puzzle = input("输入字谜: ")
            candidate_name = find_candidate_names(puzzle, inverted_index)
            answer = solve_puzzle(puzzle, candidate_name)
            print(answer)
        except Exception as e:
            print(e)
            break


def loads_test_puzzles():
    puzzles = []
    with open(answer_url, mode='r') as load_file:
        lines = load_file.readlines()
        for i in range(0, len(lines), 6):
            # print(lines[i])
            puzzles.append(lines[i].replace("\t", "").replace("\n", "").replace(" ", ""))
    return puzzles


def testcase_v1():
    test_puzzles = loads_test_puzzles()

    # 1
    v1_start = time.time()
    v1_start_mem = psutil.Process(os.getpid()).memory_info().rss
    sprite_names, _ = loads_sprite()
    for puzzle in test_puzzles:
        solve_puzzle(puzzle, sprite_names)
    v1_end = time.time()
    v1_end_mem = psutil.Process(os.getpid()).memory_info().rss
    print(sys.getsizeof(sprite_names))
    print("v1 cost: %f" % (v1_end - v1_start))
    print((v1_end_mem - v1_start_mem) / 1024)


def testcase_v2():
    test_puzzles = loads_test_puzzles()

    # 2
    v2_start = time.time()
    v2_start_mem = psutil.Process(os.getpid()).memory_info().rss
    sprite_names, sprite_names_counter = loads_sprite()
    inverted_index = create_inverted_index(sprite_names)
    for puzzle in test_puzzles:
        candidate_name = find_candidate_names(puzzle, inverted_index)
        solve_puzzle(puzzle, candidate_name)
    v2_end = time.time()
    v2_end_mem = psutil.Process(os.getpid()).memory_info().rss
    print(sys.getsizeof(inverted_index) / 1024)
    print("v2 cost: %f" % (v2_end - v2_start))
    print((v2_end_mem - v2_start_mem) / 1024)


if __name__ == '__main__':
    # main()
    # test_inverted_index()
    # main_v2()
    # print(loads_test_puzzles())
    testcase_v2()