#!/usr/bin/env python
# coding=utf-8


with open("./articles.csv") as f:
    with open("./articles_new.csv", "w+") as o:
        lines = f.readlines()
        for line in lines:
            words = line.strip().split(",")
            id = words[0]
            content = words[1:]
            text = '，'.join(content)
            text = text.replace(",", "，")
            o.write(id + "," + text + "\n")

