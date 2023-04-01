#!/usr/bin/env python
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import random
import sys
import os
from cedict_utils.cedict import CedictParser
import pypinyin

NUM_WORDS = 20

def get_random_entries(entries, seed):
    random.seed(seed)
    return [random.choice(entries) for _ in range(0, NUM_WORDS)]

def run_one_round(random_entries, seed):
    random.seed(seed)
    shuffled_indexes = list(range(0, NUM_WORDS))
    random.shuffle(shuffled_indexes)
    num_correct = 0
    for i, entry in enumerate(map(lambda index: random_entries[index], shuffled_indexes)):
        os.system('clear')
        word = entry.simplified
        pinyin_string = " ".join(map(pypinyin.contrib.tone_convert.to_tone, entry.pinyin.split()))
        list_of_meanings = entry.meanings
        print(f"{i}/{NUM_WORDS}")
        user_in = input(f"{word}\n")
        if user_in == word:
            print("correct")
            num_correct += 1
        else:
            print(f"{word} ({pinyin_string}): {list_of_meanings}\n")
            while True:
                user_in = input(f"{word}\n")
                if(user_in == word):
                    break;
    return num_correct

def run_one_set(random_entries, seed):
    random.seed(seed)
    seed = random.randbytes(32)
    while True:
        num_correct = run_one_round(random_entries, seed)
        print(f"{num_correct} correct")
        print("=========================")
        if num_correct == NUM_WORDS:
            break

def main(argv):
    round_num = 0
    if len(argv) > 1:
        seed = int(sys.argv[1])
        if len(argv) > 2:
            round_num = int(argv[2])
    else:
        seed = None
    random.seed(seed)
    parser = CedictParser()
    parser.read_file("cedict_1_0_ts_utf-8_mdbg.txt")
    entries = parser.parse()
    for _ in range(0, round_num):
        _ = random.randbytes(32)
    while True:
        seed = random.randbytes(32)
        rng_state = random.getstate()
        random_entries = get_random_entries(entries, seed)
        run_one_set(random_entries, seed)
        random.setstate(rng_state)

main(sys.argv)
