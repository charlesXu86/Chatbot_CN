import re
import jieba
import random
from tensorflow.contrib import learn


class Data_Prepare(object):

    def readfile(self, filename):
        texta = []
        textb = []
        tag = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip().split("\t")
                texta.append(self.pre_processing(line[0]))
                textb.append(self.pre_processing(line[1]))
                tag.append(line[2])
        # shuffle
        index = [x for x in range(len(texta))]
        random.shuffle(index)
        texta_new = [texta[x] for x in index]
        textb_new = [textb[x] for x in index]
        tag_new = [tag[x] for x in index]

        type = list(set(tag_new))
        dicts = {}
        tags_vec = []
        for x in tag_new:
            if x not in dicts.keys():
                dicts[x] = 1
            else:
                dicts[x] += 1
            temp = [0] * len(type)
            temp[int(x)] = 1
            tags_vec.append(temp)
        print(dicts)
        return texta_new, textb_new, tags_vec

    def pre_processing(self, text):
        # 删除（）里的内容
        text = re.sub('（[^（.]*）', '', text)
        # 只保留中文部分
        text = ''.join([x for x in text if '\u4e00' <= x <= '\u9fa5'])
        # 利用jieba进行分词
        words = ' '.join(jieba.cut(text)).split(" ")
        # 不分词
        words = [x for x in ''.join(words)]
        return ' '.join(words)

    def build_vocab(self, sentences, path):
        lens = [len(sentence.split(" ")) for sentence in sentences]
        max_length = max(lens)
        vocab_processor = learn.preprocessing.VocabularyProcessor(max_length)
        vocab_processor.fit(sentences)
        vocab_processor.save(path)


if __name__ == '__main__':
    data_pre = Data_Prepare()
    data_pre.readfile('data/train.txt')
