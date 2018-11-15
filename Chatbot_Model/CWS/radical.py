# -*- coding:utf-8 -*-
# Filename: radical.py
# Author：hankcs
# Date: 2017-07-19 PM11:41


class Radical:
    _radical = {}
    _char = {}
    _char.setdefault('null')

    @staticmethod
    def _init():
        with open('data/radical/radical.txt', encoding="utf-8") as f:
            for line in f:
                cells = line.rstrip('\n').split('\t')
                c, r = cells[0], cells[3]
                Radical._radical[c] = r
                Radical._char[r] = c

    @staticmethod
    def to_radical(char):
        r = Radical._radical.get(char)
        if r is None:
            return char
        return r

    @staticmethod
    def to_char(radical):
        c = Radical._char.get(radical)
        if c is None:
            return radical
        return c

    @staticmethod
    def to_radical_sentence(sent):
        line = ''
        for c in sent:
            line += Radical.to_radical(c)
            line += ' '
        return line[:-1]

    @staticmethod
    def to_radical_list(sent):
        l = []
        for c in sent:
            l.append(Radical.to_radical(c))
        return l


# noinspection PyProtectedMember
Radical._init()

if __name__ == "__main__":
    print(Radical.to_radical('胖'))
