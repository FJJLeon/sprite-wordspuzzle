import json
from collections import Counter

sprite_data_url = "./SpriteData.json"


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

    return sprite_names, sprite_names_counter


def solve_puzzle(puzzle, candidate_names):
    puzzle = puzzle.replace("\t", "")
    puzzle = puzzle.replace(" ", "")

    puzzle_counter = Counter(list(puzzle))
    for name in candidate_names:
        name_counter = Counter(name)
        if all(v <= puzzle_counter[k] for k, v in name_counter.items()):
            return name
    return "不存在"


def main():
    sprite_names, sprite_names_counter = loads_sprite()
    print(solve_puzzle("郎	喜	奴	乌	货	孙	娃	雨	知", sprite_names))
    while True:
        try:
            puzzle = input("输入字谜: ")
            print(solve_puzzle(puzzle, sprite_names))
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    main()