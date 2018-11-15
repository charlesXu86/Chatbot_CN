# coding=utf-8
import codecs
import errno
import os
import sys
import time

import numpy as np

UNK_TAG = "<UNK>"
NONE_TAG = "<NONE>"
START_TAG = "<START>"
END_TAG = "<STOP>"
PADDING_CHAR = "<*>"
POS_KEY = "POS"
MORPH_KEY = "MORPH"


class Progbar(object):
    """Progbar class copied from keras (https://github.com/fchollet/keras/)

    Displays a progress bar.
    Small edit : added strict arg to update
    # Arguments
        target: Total number of steps expected.
        interval: Minimum visual progress update interval (in seconds).
    """

    def __init__(self, target, width=30, verbose=1):
        self.width = width
        self.target = target
        self.sum_values = {}
        self.unique_values = []
        self.start = time.time()
        self.total_width = 0
        self.seen_so_far = 0
        self.verbose = verbose

    def update(self, current, values=[], exact=[], strict=[]):
        """
        Updates the progress bar.
        # Arguments
            current: Index of current step.
            values: List of tuples (name, value_for_last_step).
                The progress bar will display averages for these values.
            exact: List of tuples (name, value_for_last_step).
                The progress bar will display these values directly.
        """

        for k, v in values:
            if k not in self.sum_values:
                self.sum_values[k] = [v * (current - self.seen_so_far), current - self.seen_so_far]
                self.unique_values.append(k)
            else:
                self.sum_values[k][0] += v * (current - self.seen_so_far)
                self.sum_values[k][1] += (current - self.seen_so_far)
        for k, v in exact:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = [v, 1]

        for k, v in strict:
            if k not in self.sum_values:
                self.unique_values.append(k)
            self.sum_values[k] = v

        self.seen_so_far = current

        now = time.time()
        if self.verbose == 1:
            prev_total_width = self.total_width
            sys.stdout.write("\b" * prev_total_width)
            sys.stdout.write("\r")

            numdigits = int(np.floor(np.log10(self.target))) + 1
            barstr = '%%%dd/%%%dd [' % (numdigits, numdigits)
            bar = barstr % (current, self.target)
            prog = float(current) / self.target
            prog_width = int(self.width * prog)
            if prog_width > 0:
                bar += ('=' * (prog_width - 1))
                if current < self.target:
                    bar += '>'
                else:
                    bar += '='
            bar += ('.' * (self.width - prog_width))
            bar += ']'
            sys.stdout.write(bar)
            self.total_width = len(bar)

            if current:
                time_per_unit = (now - self.start) / current
            else:
                time_per_unit = 0
            eta = time_per_unit * (self.target - current)
            info = ''
            if current < self.target:
                info += ' - ETA: %ds' % eta
            else:
                info += ' - %ds' % (now - self.start)
            for k in self.unique_values:
                if type(self.sum_values[k]) is list:
                    info += ' - %s: %.4f' % (k, self.sum_values[k][0] / max(1, self.sum_values[k][1]))
                else:
                    info += ' - %s: %s' % (k, self.sum_values[k])

            self.total_width += len(info)
            if prev_total_width > self.total_width:
                info += ((prev_total_width - self.total_width) * " ")

            sys.stdout.write(info)
            sys.stdout.flush()

            if current >= self.target:
                sys.stdout.write("\n")

        if self.verbose == 2:
            if current >= self.target:
                info = '%ds' % (now - self.start)
                for k in self.unique_values:
                    info += ' - %s: %.4f' % (k, self.sum_values[k][0] / max(1, self.sum_values[k][1]))
                sys.stdout.write(info + "\n")

    def add(self, n, values=[]):
        self.update(self.seen_so_far + n, values)


class CSVLogger:
    def __init__(self, filename, columns):
        self.file = open(filename, "w")
        self.columns = columns
        self.file.write(','.join(columns) + "\n")

    def add_column(self, data):
        self.file.write(','.join([str(d) for d in data]) + "\n")
        self.file.flush()

    def close(self):
        self.file.close()


def convert_instance(instance, i2w, i2t):
    sent = [i2w[w] for w in instance.sentence]
    tags = [i2t[t] for t in instance.tags]
    return sent, tags


def read_pretrained_embeddings(filename, w2i):
    word_to_embed = {}
    with codecs.open(filename, "r", "utf-8") as f:
        for line in f:
            split = line.split()
            if len(split) > 2:
                word = split[0]
                if word in w2i:
                    vec = split[1:]
                    word_to_embed[word] = vec
    embedding_dim = len(next(iter(word_to_embed.values())))
    out = np.random.uniform(-0.8, 0.8, (len(w2i), embedding_dim))
    for word, embed in word_to_embed.items():
        out[w2i[word]] = np.array(embed)
    return out


def split_tagstring(s, uni_key=False, has_pos=False):
    '''
    Returns attribute-value mapping from UD-type CONLL field
    @param uni_key: if toggled, returns attribute-value pairs as joined strings (with the '=')
    '''
    if has_pos:
        s = s.split("\t")[1]
    ret = [] if uni_key else {}
    if "=" not in s:  # incorrect format
        return ret
    for attval in s.split('|'):
        attval = attval.strip()
        if not uni_key:
            a, v = attval.split('=')
            ret[a] = v
        else:
            ret.append(attval)
    return ret


def to_tag_strings(i2ts, tag_mapping, pos_separate_col=True):
    senlen = len(tag_mapping)
    key_value_strs = []

    # j iterates along sentence, as we're building the string representations
    # in the opposite orientation as the mapping
    for j in range(senlen):
        val = i2ts[tag_mapping[j]]
        pos_str = val
        key_value_strs.append(pos_str)
    return key_value_strs


def bmes_to_words(chars, tags):
    result = []
    if len(chars) == 0:
        return result
    word = chars[0]

    for c, t in zip(chars[1:], tags[1:]):
        if t == 'B' or t == 'S':
            result.append(word)
            word = ''
        word += c
    if len(word) != 0:
        result.append(word)

    return result


def sortvals(dct):
    return [v for (k, v) in sorted(dct.items())]


def get_processing_word(vocab_words=None, vocab_chars=None,
                        lowercase=False, chars=False):
    """
    Args:
        vocab: dict[word] = idx
    Returns:
        f("cat") = ([12, 4, 32], 12345)
                 = (list of char ids, word id)
    """

    def f(word):
        # 0. get chars of words
        if vocab_chars is not None and chars == True:
            char_ids = []
            for char in word:
                # ignore chars out of vocabulary
                if char in vocab_chars:
                    char_ids += [vocab_chars[char]]

        # 1. preprocess word
        if lowercase:
            word = word.lower()
        if word.isdigit():
            word = '0'

        # 2. get id of word
        if vocab_words is not None:
            if word in vocab_words:
                word = vocab_words[word]
            else:
                word = vocab_words[UNK_TAG]

        # 3. return tuple char ids, word id
        if vocab_chars is not None and chars == True:
            return char_ids, word
        else:
            return word

    return f


def get_chunk_type(tok, idx_to_tag):
    """
    Args:
        tok: id of token, ex 4
        idx_to_tag: dictionary {4: "B-PER", ...}
    Returns:
        tuple: "B", "PER"
    """
    tag_name = idx_to_tag[tok]
    tag_class = tag_name.split('-')[0]
    tag_type = tag_name.split('-')[-1]
    return tag_class, tag_type


def get_chunks(seq, tags):
    """
    Args:
        seq: [4, 4, 0, 0, ...] sequence of labels
        tags: dict["O"] = 4
    Returns:
        list of (chunk_type, chunk_start, chunk_end)

    Example:
        seq = [4, 5, 0, 3]
        tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
        result = [("PER", 0, 2), ("LOC", 3, 4)]
    """
    default = tags["O"]
    idx_to_tag = {idx: tag for tag, idx in tags.items()}
    chunks = []
    chunk_type, chunk_start = None, None
    for i, tok in enumerate(seq):
        # End of a chunk 1
        if tok == default and chunk_type is not None:
            # Add a chunk.
            chunk = (chunk_type, chunk_start, i)
            chunks.append(chunk)
            chunk_type, chunk_start = None, None

        # End of a chunk + start of a chunk!
        elif tok != default:
            tok_chunk_class, tok_chunk_type = get_chunk_type(tok, idx_to_tag)
            if chunk_type is None:
                chunk_type, chunk_start = tok_chunk_type, i
            elif tok_chunk_type != chunk_type or tok_chunk_class == "B":
                chunk = (chunk_type, chunk_start, i)
                chunks.append(chunk)
                chunk_type, chunk_start = tok_chunk_type, i
        else:
            pass
    # end condition
    if chunk_type is not None:
        chunk = (chunk_type, chunk_start, len(seq))
        chunks.append(chunk)

    return chunks


class NEREvaluator:
    def __init__(self, t2i):
        self.correct_preds = 0.
        self.total_preds = 0.
        self.total_correct = 0.
        self.t2i = t2i

    def add_instance(self, gold_tags, out_tags):
        # Evaluate PRF
        lab_chunks = set(get_chunks(gold_tags, self.t2i))
        lab_pred_chunks = set(get_chunks(out_tags, self.t2i))
        self.correct_preds += len(lab_chunks & lab_pred_chunks)
        self.total_preds += len(lab_pred_chunks)
        self.total_correct += len(lab_chunks)

    def result(self):
        p = self.correct_preds / self.total_preds if self.correct_preds > 0 else 0
        r = self.correct_preds / self.total_correct if self.correct_preds > 0 else 0
        f1 = 2 * p * r / (p + r) if p + r > 0 else 0
        return p, r, f1


def bmes_tag(input_file, output_file):
    with open(input_file) as input_data, open(output_file, 'w') as output_data:
        for line in input_data:
            word_list = line.strip().split()
            for word in word_list:
                if len(word) == 1:
                    output_data.write(word + "\tS\n")
                else:
                    output_data.write(word[0] + "\tB\n")
                    for w in word[1:len(word) - 1]:
                        output_data.write(w + "\tM\n")
                    output_data.write(word[len(word) - 1] + "\tE\n")
            output_data.write("\n")


def bmes_to_words(chars, tags):
    result = []
    if len(chars) == 0:
        return result
    word = chars[0]

    for c, t in zip(chars[1:], tags[1:]):
        if t == 'B' or t == 'S':
            result.append(word)
            word = ''
        word += c
    if len(word) != 0:
        result.append(word)

    return result


def bmes_to_index(tags):
    """
    Args:
        tags: [4, 4, 0, 0, ...] sequence of labels
    Returns:
        list of (chunk_type, chunk_start, chunk_end)

    Example:
        seq = [4, 5, 0, 3]
        tags = {"B-PER": 4, "I-PER": 5, "B-LOC": 3}
        result = [("PER", 0, 2), ("LOC", 3, 4)]
    """
    result = []
    if len(tags) == 0:
        return result
    word = (0, 0)

    for i, t in enumerate(tags):
        if i == 0:
            word = (0, 0)
        elif t == 'B' or t == 'S':
            result.append(word)
            word = (i, 0)
        word = (word[0], word[1] + 1)
    if word[1] != 0:
        result.append(word)
    return result


def combine_bmes_to_raw(bmes, raw):
    with open(bmes) as input_data, open(raw, 'w') as output_data:
        words = []
        tags = []
        for line in input_data:
            cells = line.strip().split()
            if len(cells) < 2:
                sent = bmes_to_words(words, tags)
                output_data.write(" ".join(sent))
                output_data.write("\n")
                words = []
                tags = []
                continue
            words.append(cells[0])
            tags.append(cells[2])


class CWSEvaluator:
    def __init__(self, i2t):
        self.correct_preds = 0.
        self.total_preds = 0.
        self.total_correct = 0.
        self.i2t = i2t

    def add_instance(self, pred_tags, gold_tags):
        pred_tags = [self.i2t[i] for i in pred_tags]
        gold_tags = [self.i2t[i] for i in gold_tags]
        # Evaluate PRF
        lab_gold_chunks = set(bmes_to_index(gold_tags))
        lab_pred_chunks = set(bmes_to_index(pred_tags))
        self.correct_preds += len(lab_gold_chunks & lab_pred_chunks)
        self.total_preds += len(lab_pred_chunks)
        self.total_correct += len(lab_gold_chunks)

    def result(self, percentage=True):
        p = self.correct_preds / self.total_preds if self.correct_preds > 0 else 0
        r = self.correct_preds / self.total_correct if self.correct_preds > 0 else 0
        f1 = 2 * p * r / (p + r) if p + r > 0 else 0
        if percentage:
            p *= 100
            r *= 100
            f1 *= 100
        return p, r, f1


def evaluate_bmes(pred, gold):
    performance = CWSEvaluator()
    with open(pred) as pred_file, open(gold) as gold_file:
        pred = []
        gold = []
        for pred_line, gold_line in zip(pred_file, gold_file):
            if len(pred_line.strip()) == 0:
                performance.add_instance(gold, pred)
            pred_line.strip().split()

    return performance.result()


def minibatches(data, minibatch_size):
    """
    Args:
        data: generator of instance
        minibatch_size: (int)
    Returns:
        list of instance
    """
    batch = []
    for instance in data:
        if len(batch) == minibatch_size:
            yield batch
            batch = []

        if type(instance[0]) == tuple:
            instance = zip(*instance)
        batch += [instance]

    if len(batch) != 0:
        yield batch


def evaluate_file(file_name, t2i):
    e = NEREvaluator(t2i)
    with codecs.open(file_name, "r", "utf-8") as f:
        pred_tags, gold_tags = [], []
        for line in f:
            line = line.strip()
            if len(line) == 0 or line.startswith("-DOCSTART-"):
                if len(pred_tags) != 0:
                    e.add_instance(gold_tags, pred_tags)
                    pred_tags, gold_tags = [], []
            else:
                cells = line.split("\t")
                if len(cells) < 2:
                    print(line)
                    continue
                pt = cells[1]
                gt = cells[3]
                if pt not in t2i or gt not in t2i:
                    print(line)
                    continue
                pred_tags.append(t2i[pt])
                gold_tags.append(t2i[gt])
    print(e.result())


def append_tags(src, des, part):
    with open('data/{}/raw/{}.txt'.format(src, part)) as input, open('data/{}/raw/{}.txt'.format(des, part),
                                                                     'a') as output:
        for line in input:
            line = line.strip()
            if len(line) > 0:
                output.write('<{}> {} </{}>'.format(src, line, src))
            output.write('\n')


def is_dataset_tag(word):
    return len(word) > 2 and word[0] == '<' and word[-1] == '>'


def to_id_list(w2i):
    i2w = [None] * len(w2i)
    for w, i in w2i.items():
        i2w[i] = w
    return i2w


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def restore_sentence(sentence):
    if len(sentence) == 0 or type(sentence[0]) != tuple:
        return sentence

    return [w[1] for w in sentence]

# if __name__ == '__main__':
#     make_joint_corpus(['pku', 'msr', 'as', 'cityu'], 'joint')
# processing_word = get_processing_word(lowercase=True)
# print processing_word('Hello你好')
# import collections
# Instance = collections.namedtuple("Instance", ["sentence", "tags"])
# dataset = cPickle.load(open("data/conll2003/build/dataset.pkl", "r"))
# w2i = dataset["w2i"]
# t2i = dataset["t2is"]["POS"]
# c2i = dataset["c2i"]
# evaluate_file("data/conll2003/build/log/testout.txt", t2i)
