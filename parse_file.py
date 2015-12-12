import json
from replay_parser import ReplayParser


if __name__ == '__main__':
    header = ReplayParser("testfiles/F07B.replay").parse_file()
    with open('parsed.json', 'w', encoding='utf-8') as outfile:
        json.dump(header, outfile, indent=4, ensure_ascii=False)
