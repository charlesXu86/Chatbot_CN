#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Feature_extraction.py 
@desc: 特征提取
@time: 2019/03/08 
"""

import os
import numpy as np
import datetime

from enum import Enum
from util.General_utils import get_pickle,dump_pickle,get_vocab_dict

NULL = "<null>"
UNK = "<unk>"
ROOT = "<root>"
pos_prefix = "<p>:"
dep_prefix = "<d>:"
punc_pos = ["''", "``", ":", ".", ","]
all_dep_label = ['<d>:\xe6\xa0\xb8\xe5\xbf\x83\xe6\x88\x90\xe5\x88\x86', '<d>:\xe6\x96\xb9\xe4\xbd\x8d\xe8\xaf\x8d\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe9\x83\xa8\xe5\x88\x86', '<d>:\xe2\x80\x9c\xe7\x9a\x84\xe2\x80\x9d\xe5\xad\x97\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe9\xa2\x86\xe6\x9c\x89\xe8\x80\x85', '<d>:\xe7\xbb\x93\xe6\x9e\x9c', '<d>:\xe7\x9b\xae\xe7\x9a\x84', '<d>:\xe5\x85\xb3\xe8\x81\x94\xe8\xaf\x8d\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe7\xbb\x88\xe5\xa4\x84\xe6\x89\x80', '<d>:\xe8\xbf\x9e\xe6\x8e\xa5\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe5\x86\x85\xe5\xae\xb9', '<d>:\xe5\xad\x98\xe7\x8e\xb0\xe4\xbd\x93', '<d>:\xe6\x9d\xa5\xe6\xba\x90', '<d>:\xe7\xa8\x8b\xe5\xba\xa6', '<d>:\xe5\x8a\xa8\xe9\x87\x8f', '<d>:\xe4\xbb\x8b\xe8\xaf\x8d\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe9\x80\x9a\xe8\xbf\x87\xe5\xa4\x84\xe6\x89\x80', '<d>:..\xe6\x98\xaf..\xe7\x9a\x84\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe8\xae\xa9\xe6\xad\xa5', '<d>:\xe5\x8f\x97\xe4\xba\x8b', '<d>:\xe5\x8e\x9f\xe7\x8a\xb6\xe6\x80\x81', '<d>:\xe6\x8f\x8f\xe5\x86\x99\xe4\xbd\x93', '<d>:\xe5\xa4\x84\xe6\x89\x80', '<d>:\xe9\x99\x90\xe5\xae\x9a', '<d>:\xe7\xb1\xbb\xe6\x8c\x87', '<d>:\xe7\x9b\xb8\xe4\xbc\xb4\xe4\xbd\x93', '<d>:\xe8\xaf\xad\xe6\xb0\x94\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe6\xaf\x94\xe8\xbe\x83\xe9\x87\x8f', '<d>:\xe5\x8e\x9f\xe5\xa4\x84\xe6\x89\x80', '<d>:\xe6\x9d\xa1\xe4\xbb\xb6', '<d>:\xe8\xbf\x9b\xe7\xa8\x8b\xe6\x97\xb6\xe6\xae\xb5', '<d>:\xe6\xa0\xb9\xe6\x8d\xae', '<d>:\xe5\x8e\x9f\xe5\x9b\xa0', '<d>:\xe5\xb9\xb6\xe5\x88\x97', '<d>:\xe6\x96\xb9\xe5\x90\x91', '<d>:\xe6\xaf\x94\xe8\xbe\x83\xe5\x86\x85\xe5\xae\xb9', '<d>:<null>', '<d>:\xe6\x97\xb6\xe6\x80\x81\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe7\xbb\x8f\xe9\xaa\x8c\xe8\x80\x85', '<d>:\xe6\x97\xb6\xe9\x97\xb4', '<d>:\xe6\x97\xb6\xe6\x80\x81\xe8\xaf\xad\xe6\x80\x81\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe9\x80\x92\xe8\xbf\x9b', '<d>:\xe6\x96\xb9\xe5\xbc\x8f', '<d>:\xe4\xbb\xa3\xe4\xbb\xb7', '<d>:\xe8\xa7\xa6\xe5\x8f\x8a\xe9\x83\xa8\xe4\xbb\xb6', '<d>:\xe7\xbb\x88\xe6\xad\xa2\xe6\x97\xb6\xe9\x97\xb4', '<d>:\xe6\x89\x8b\xe6\xae\xb5', '<d>:\xe7\xbb\x93\xe6\x9e\x9c\xe4\xba\x8b\xe4\xbb\xb6', '<d>:\xe7\xbb\x88\xe7\x8a\xb6\xe6\x80\x81', '<d>:\xe6\x8e\xa5\xe7\xbb\xad', '<d>:\xe5\xb7\xa5\xe5\x85\xb7', '<d>:\xe7\x9b\xae\xe6\xa0\x87', '<d>:\xe6\x96\xbd\xe4\xba\x8b', '<d>:\xe8\xaf\x84\xe8\xae\xba', '<d>:\xe8\x8c\x83\xe5\x9b\xb4', '<d>:\xe5\x90\x8e\xe5\xbb\xb6\xe6\x97\xb6\xe6\xae\xb5', '<d>:\xe9\xa2\x91\xe7\x8e\x87', '<d>:<unk>', '<d>:\xe8\xb5\xb7\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', '<d>:\xe4\xbc\xb4\xe9\x9a\x8f', '<d>:\xe8\xb6\x8b\xe5\x90\x91\xe5\x8a\xa8\xe8\xaf\x8d\xe4\xbe\x9d\xe5\xad\x98', '<d>:\xe6\x8f\x8f\xe8\xbf\xb0', '<d>:\xe6\x97\xb6\xe8\xb7\x9d', '<d>:\xe5\x90\x8c\xe4\xbd\x8d\xe8\xaf\xad', '<d>:\xe6\x95\xb4\xe4\xbd\x93', '<d>:\xe9\x99\xa4\xe4\xba\x86', '<d>:\xe6\x95\xb0\xe9\x87\x8f', '<d>:\xe5\x85\xb3\xe7\xb3\xbb\xe4\xb8\xbb\xe4\xbd\x93', '<d>:\xe6\x9d\x90\xe6\x96\x99', '<d>:\xe4\xba\x8b\xe4\xbb\xb6\xe8\xbf\x87\xe7\xa8\x8b', '<d>:\xe5\x8f\x82\xe7\x85\xa7\xe4\xbd\x93', '<d>:<root>']


today_date = str(datetime.datetime.now().date())

class DataConfig:  # data, embedding, model path etc.
    # Data Paths
    data_dir_path = "/../data"
    train_path = "train.conll"
    valid_path = "dev.conll"
    test_path = "test.conll"

    # embedding
    embedding_file = "ch_cw.txt"

    # model saver
    model_dir = "params_" + today_date
    model_name = "parser.weights"

    # summary
    summary_dir = "params_" + today_date
    train_summ_dir = "train_summaries"
    test_summ_dir = "valid_summaries"

    # dump - vocab
    dump_dir = "/../data/pkl"
    word_vocab_file = "word2idx.pkl"
    pos_vocab_file = "pos2idx.pkl"
    dep_vocab_file = "dep2idx.pkl"

    # dump - embedding
    word_emb_file = "word_emb.pkl"  # 2d array
    pos_emb_file = "pos_emb.pkl"  # 2d array
    dep_emb_file = "dep_emb.pkl"  # 2d array


class ModelConfig(object):  # Takes care of shape, dimensions used for tf model
    # Input
    word_features_types = None
    pos_features_types = None
    dep_features_types = None
    num_features_types = None
    embedding_dim = 50

    # hidden_size
    l1_hidden_size = 200
    #l2_hidden_size = 15
    l2_hidden_size = 200

    # output
    num_classes = 2 * len(all_dep_label) + 1

    # Vocab
    word_vocab_size = None
    pos_vocab_size = None
    dep_vocab_size = None

    # num_epochs
    n_epochs = 25

    # batch_size
    batch_size = 2048

    # dropout
    keep_prob = 0.5
    reg_val = 1e-8

    # learning_rate
    lr = 0.001

    # load existing vocab
    load_existing_vocab = False

    # summary
    write_summary_after_epochs = 1

    # valid run
    run_valid_after_epochs = 1

class SettingsConfig:  # enabling and disabling features, feature types
    # Features
    use_word = True
    use_pos = True
    use_dep = True
    is_lower = True


class Flags(Enum):
    TRAIN = 1
    VALID = 2
    TEST = 3


class Token(object):
    def __init__(self, token_id, word, pos, dep, head_id):
        self.token_id = token_id  # token index
        self.word = word.lower() if SettingsConfig.is_lower else word
        self.pos = pos_prefix + pos
        self.dep = dep_prefix + dep
        self.head_id = head_id  # head token index
        self.predicted_head_id = None
        #self.left_children = list()
        #self.right_children = list()
        self.left_children = {}
        self.right_children = {}


    def is_root_token(self):
        if self.word == ROOT:
            return True
        return False


    def is_null_token(self):
        if self.word == NULL:
            return True
        return False


    def is_unk_token(self):
        if self.word == UNK:
            return True
        return False


    def reset_predicted_head_id(self):
        self.predicted_head_id = None


NULL_TOKEN = Token(-1, NULL, NULL, NULL, -1)
ROOT_TOKEN = Token(-1, ROOT, ROOT, ROOT, -1)
UNK_TOKEN = Token(-1, UNK, UNK, UNK, -1)


# 解析句子
class Sentence(object):
    def __init__(self, tokens):
        self.Root = Token(-1, ROOT, ROOT, ROOT, -1)
        self.tokens = tokens
        self.buff = [token for token in self.tokens]
        self.stack = [self.Root]
        self.dependencies = []
        self.predicated_dependencies = []

    def load_gold_dependency_mapping(self):
        for token in self.tokens:
            if token.head_id != -1:
                token.parent = self.tokens[token.head_id]
                if token.head_id > token.token_id:
                    token.parent.left_children[token.token_id] = token.dep
                else:
                    token.parent.right_children[token.token_id] = token.dep
            else:
                token.parent = self.Root

        for token in self.tokens:
            token.left_children.keys().sort()
            token.right_children.keys().sort()

    def update_child_dependencies(self, curr_transition):
        if curr_transition > 0 and curr_transition <= len(all_dep_label):
            head = self.stack[-1]
            dependent = self.stack[-2]
        elif curr_transition > len(all_dep_label) and curr_transition <= 2*len(all_dep_label):
            head = self.stack[-2]
            dependent = self.stack[-1]

        if head.token_id > dependent.token_id:
            head.left_children[dependent.token_id] = dependent.dep
            head.left_children.keys().sort()
        else:
            head.right_children[dependent.token_id] = dependent.dep
            head.right_children.keys().sort()
            # dependent.head_id = head.token_id

    def get_child_by_index_and_depth(self, token, index, direction, depth):  # Get child token
        if depth == 0:
            return token

        if direction == "left":
            if len(token.left_children.keys()) > index:
                return self.get_child_by_index_and_depth(
                    self.tokens[token.left_children.keys()[index]], index, direction, depth - 1)
            return NULL_TOKEN
        else:
            if len(token.right_children.keys()) > index:
                return self.get_child_by_index_and_depth(
                    self.tokens[token.right_children.keys()[::-1][index]], index, direction, depth - 1)
            return NULL_TOKEN

    def get_legal_labels(self):
        #labels = ([1] * 70 if len(self.stack) > 2 else [0] * 70)
        #labels += ([1] * 70 if len(self.stack) >= 2 else [0]* 70)
        #labels += [1] * 70 if len(self.buff) > 0 else [0]* 70
        labels = [1] if len(self.buff) > 0 else [0]
        labels += ([1] * len(all_dep_label)  if len(self.stack) > 2 else [0] * len(all_dep_label))
        labels += ([1] * len(all_dep_label) if len(self.stack) >= 2 else [0]* len(all_dep_label) )
        return labels

    def get_transition_from_current_state(self):  # logic to get next transition
        if len(self.stack) < 2:
            return 0  # shift

        stack_token_0 = self.stack[-1]
        stack_token_1 = self.stack[-2]
        if stack_token_1.token_id >= 0 and stack_token_1.head_id == stack_token_0.token_id:  # left arc
            for i in range(len(all_dep_label)):
                if stack_token_1.dep == all_dep_label[i]:
                    return i + 1
        elif stack_token_1.token_id >= -1 and stack_token_0.head_id == stack_token_1.token_id \
                and stack_token_0.token_id not in map(lambda x: x.head_id, self.buff):
            for i in range(len(all_dep_label)):
                if stack_token_0.dep == all_dep_label[i]:
                    return len(all_dep_label) + 1 + i
        else:
            return 0 if len(self.buff) != 0 else None

    def update_state_by_transition(self, transition, gold=True):  # updates stack, buffer and dependencies
        if transition is not None:
            if transition == 0:  # shift
                self.stack.append(self.buff[0])
                self.buff = self.buff[1:] if len(self.buff) > 1 else []
            elif transition >= 1 and transition <= len(all_dep_label):  # left arc
                dep_label = all_dep_label[transition - 1]
                self.dependencies.append(
                    (self.stack[-1], self.stack[-2], dep_label)) if gold else self.predicted_dependencies.append(
                        (self.stack[-1], self.stack[-2], dep_label))
                self.stack = self.stack[:-2] + self.stack[-1:]
            elif transition > len(all_dep_label) and transition <= 2 * len(all_dep_label):  # right arc
                dep_label = all_dep_label[transition - len(all_dep_label) -1]
                self.dependencies.append(
                    (self.stack[-2], self.stack[-1], dep_label)) if gold else self.predicted_dependencies.append(
                    (self.stack[-2], self.stack[-1], dep_label))
                self.stack = self.stack[:-1]

    def reset_to_initial_state(self):
        self.buff = [token for token in self.tokens]
        self.stack = [self.Root]


    def clear_prediction_dependencies(self):
        self.predicted_dependencies = []


    def clear_children_info(self):
        for token in self.tokens:
            token.left_children = {}
            token.right_children = {}


class Dataset(object):
    def __init__(self, model_config, train_data, valid_data, test_data, feature_extractor):
        self.model_config = model_config
        self.train_data = train_data
        self.valid_data = valid_data
        self.test_data = test_data
        self.feature_extractor = feature_extractor

        # Vocab
        self.word2idx = None
        self.idx2word = None
        self.pos2idx = None
        self.idx2pos = None
        self.dep2idx = None
        self.idx2dep = None

        # Embedding Matrix
        self.word_embedding_matrix = None
        self.pos_embedding_matrix = None
        self.dep_embedding_matrix = None

        # input & outputs
        self.train_inputs, self.train_targets = None, None
        self.valid_inputs, self.valid_targets = None, None
        self.test_inputs, self.test_targets = None, None

    def build_vocab(self):

        all_words = set()
        all_pos = set()
        all_dep = set()

        for sentence in self.train_data:
            all_words.update(set(map(lambda x: x.word, sentence.tokens)))
            all_pos.update(set(map(lambda x: x.pos, sentence.tokens)))
            all_dep.update(set(map(lambda x: x.dep, sentence.tokens)))

        all_words.add(ROOT_TOKEN.word)
        all_words.add(NULL_TOKEN.word)
        all_words.add(UNK_TOKEN.word)

        all_pos.add(ROOT_TOKEN.pos)
        all_pos.add(NULL_TOKEN.pos)
        all_pos.add(UNK_TOKEN.pos)

        all_dep.add(ROOT_TOKEN.dep)
        all_dep.add(NULL_TOKEN.dep)
        all_dep.add(UNK_TOKEN.dep)

        word_vocab = list(all_words)
        pos_vocab = list(all_pos)
        dep_vocab = list(all_dep)

        word2idx = get_vocab_dict(word_vocab)  # project item to idx
        idx2word = {idx: word for (word, idx) in word2idx.items()}

        pos2idx = get_vocab_dict(pos_vocab)
        idx2pos = {idx: pos for (pos, idx) in pos2idx.items()}

        dep2idx = get_vocab_dict(dep_vocab)
        idx2dep = {idx: dep for (dep, idx) in dep2idx.items()}

        self.word2idx = word2idx
        self.idx2word = idx2word

        self.pos2idx = pos2idx
        self.idx2pos = idx2pos

        self.dep2idx = dep2idx
        self.idx2dep = idx2dep

    def build_embedding_matrix(self):

        # load word vectors
        word_vectors = {}
        embedding_lines = open(os.path.join(DataConfig.data_dir_path, DataConfig.embedding_file), "r").readlines()
        for line in embedding_lines:
            sp = line.strip().split()
            word_vectors[sp[0]] = [float(x) for x in sp[1:]]

        # word embedding
        self.model_config.word_vocab_size = len(self.word2idx)
        word_embedding_matrix = np.asarray(
            np.random.normal(0, 0.9, size=(self.model_config.word_vocab_size, self.model_config.embedding_dim)),
            dtype=np.float32)
        for (word, idx) in self.word2idx.items():
            if word in word_vectors:
                word_embedding_matrix[idx] = word_vectors[word]
            elif word.lower() in word_vectors:
                word_embedding_matrix[idx] = word_vectors[word.lower()]
        self.word_embedding_matrix = word_embedding_matrix

        # pos embedding
        self.model_config.pos_vocab_size = len(self.pos2idx)
        pos_embedding_matrix = np.asarray(
            np.random.normal(0, 0.9, size=(self.model_config.pos_vocab_size, self.model_config.embedding_dim)),
            dtype=np.float32)
        self.pos_embedding_matrix = pos_embedding_matrix

        # dep embedding
        self.model_config.dep_vocab_size = len(self.dep2idx)
        dep_embedding_matrix = np.asarray(
            np.random.normal(0, 0.9, size=(self.model_config.dep_vocab_size, self.model_config.embedding_dim)),
            dtype=np.float32)
        self.dep_embedding_matrix = dep_embedding_matrix

    def convert_data_to_ids(self):
        self.train_inputs, self.train_targets = self.feature_extractor. \
            create_instances_for_data(self.train_data, self.word2idx, self.pos2idx, self.dep2idx, self.idx2dep)

        # self.valid_inputs, self.valid_targets = self.feature_extractor.\
        #     create_instances_for_data(self.valid_data, self.word2idx)
        # self.test_inputs, self.test_targets = self.feature_extractor.\
        #     create_instances_for_data(self.test_data, self.word2idx)


    def add_to_vocab(self, words, prefix=""):
        idx = len(self.word2idx)
        for token in words:
            if prefix + token not in self.word2idx:
                self.word2idx[prefix + token] = idx
                self.idx2word[idx] = prefix + token
                idx += 1

class FeatureExtractor(object):
    def __init__(self, model_config):
        self.model_config = model_config

    def extract_from_stack_and_buffer(self, sentence, num_words=3):
        tokens = []

        tokens.extend([NULL_TOKEN for _ in range(num_words - len(sentence.stack))])
        tokens.extend(sentence.stack[-num_words:])

        tokens.extend(sentence.buff[:num_words])
        tokens.extend([NULL_TOKEN for _ in range(num_words - len(sentence.buff))])
        return tokens  # 6 features

    def extract_children_from_stack(self, sentence, num_stack_words=2):
        children_tokens = []

        for i in range(num_stack_words):
            if len(sentence.stack) > i:
                lc0 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 0, "left", 1)
                rc0 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 0, "right", 1)

                lc1 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 1, "left",
                                                            1) if lc0 != NULL_TOKEN else NULL_TOKEN
                rc1 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 1, "right",
                                                            1) if rc0 != NULL_TOKEN else NULL_TOKEN

                llc0 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 0, "left",
                                                             2) if lc0 != NULL_TOKEN else NULL_TOKEN
                rrc0 = sentence.get_child_by_index_and_depth(sentence.stack[-i - 1], 0, "right",
                                                             2) if rc0 != NULL_TOKEN else NULL_TOKEN

                children_tokens.extend([lc0, rc0, lc1, rc1, llc0, rrc0])
            else:
                [children_tokens.append(NULL_TOKEN) for _ in range(6)]

        return children_tokens  # 12 features

    def extract_for_current_state(self, sentence, word2idx, pos2idx, dep2idx, idx2dep):
        direct_tokens = self.extract_from_stack_and_buffer(sentence, num_words=3)
        children_tokens = self.extract_children_from_stack(sentence, num_stack_words=2)

        word_features = []
        pos_features = []
        dep_features = []

        # Word features -> 18
        word_features.extend(map(lambda x: x.word, direct_tokens))
        word_features.extend(map(lambda x: x.word, children_tokens))

        # pos features -> 18
        pos_features.extend(map(lambda x: x.pos, direct_tokens))
        pos_features.extend(map(lambda x: x.pos, children_tokens))

        # dep features -> 12 (only children)
        dep_features.extend(map(lambda x: x.dep, children_tokens))

        word_input_ids = [word2idx[word] if word in word2idx else word2idx[UNK_TOKEN.word] for word in word_features]
        pos_input_ids = [pos2idx[pos] if pos in pos2idx else pos2idx[UNK_TOKEN.pos] for pos in pos_features]
        dep_input_ids = [dep2idx[dep] if dep in dep2idx else dep2idx[UNK_TOKEN.dep] for dep in dep_features]

        return [word_input_ids, pos_input_ids, dep_input_ids]  # 48 features

    def create_instances_for_data(self, data, word2idx, pos2idx, dep2idx, idx2dep):
        lables = []
        word_inputs = []
        pos_inputs = []
        dep_inputs = []
        for i, sentence in enumerate(data):
            num_words = len(sentence.tokens)

            for _ in range(num_words * 2):
                word_input, pos_input, dep_input = self.extract_for_current_state(sentence, word2idx, pos2idx, dep2idx,
                                                                                  idx2dep)
                legal_labels = sentence.get_legal_labels()
                curr_transition = sentence.get_transition_from_current_state()
                if curr_transition is None:
                    break
                assert legal_labels[curr_transition] == 1

                # Update left/right children
                if curr_transition != 0:
                    sentence.update_child_dependencies(curr_transition)

                sentence.update_state_by_transition(curr_transition)
                lables.append(curr_transition)
                word_inputs.append(word_input)
                pos_inputs.append(pos_input)
                dep_inputs.append(dep_input)

            else:
                sentence.reset_to_initial_state()

            # reset stack and buffer to default state
            sentence.reset_to_initial_state()

        targets = np.zeros((len(lables), self.model_config.num_classes), dtype=np.int32)
        targets[np.arange(len(targets)), lables] = 1  # targets should be 1 when use that action

        return [word_inputs, pos_inputs, dep_inputs], targets


class DataReader(object):
    def __init__(self):
        print('Initial data reader....')

    def read_conll(self, token_lines):
        tokens = []
        for each in token_lines:
            fields = each.strip().split('\t')
            token_index = int(fields[0]) - 1
            word = fields[0]
            pos = fields[4]
            dep = fields[7]
            head_index = int(fields[6]) - 1
            token = Token(token_index, word, pos, dep, head_index)
            tokens.append(token)
        sentence = Sentence(tokens)

        # sentence.load_gold_dependency_mapping()
        return sentence

    def read_conll_test(self, list_word, list_pos):
        tokens = []
        if len(list_word) != len(list_pos):
            print("Please check your input dim for word or pos!!!")
        for i in range(len(list_pos)):
            token_index = i
            word = list_word[i]
            pos = list_pos[i]
            dep = u""
            head_index = 0
            token = Token(token_index, word, pos, dep, head_index)
            tokens.append(token)
        sentence = Sentence(tokens)

        # sentence.load_gold_dependency_mapping()
        return sentence

    def read_data(self, data_lines):
        data_objects = []
        token_lines = []
        for token_conll in data_lines:
            token_conll = token_conll.strip()
            if len(token_conll) > 0:
                token_lines.append(token_conll)
            else:
                data_objects.append(self.read_conll(token_lines))
                token_lines = []
        if len(token_lines) > 0:
            data_objects.append(self.read_conll(token_lines))
        return data_objects

    def read_data_test(self, list_word, list_pos):
        data_objects = []
        token_lines = []
        if len(list_pos) > 0 and len(list_word) > 0:
            data_objects.append(self.read_conll_test(list_word, list_pos))
        return data_objects

def load_datasets(list_word, list_pos, load_file=True, load_existing_dump=False):
    model_config = ModelConfig()

    data_reader = DataReader()
    train_lines = open(os.path.join(DataConfig.data_dir_path, DataConfig.train_path), "r").readlines()
    valid_lines = open(os.path.join(DataConfig.data_dir_path, DataConfig.valid_path), "r").readlines()
    test_lines = open(os.path.join(DataConfig.data_dir_path, DataConfig.test_path), "r").readlines()

    # Load data
    train_data = data_reader.read_data(train_lines)
    print("Loaded Train data")
    valid_data = data_reader.read_data(valid_lines)
    print("Loaded Dev data")
    test_data = data_reader.read_data(test_lines)
    print("Loaded Test data")

    if not load_file:
        test_data = data_reader.read_data_test(list_word, list_pos)
        print("Loading the input sentence...")

    feature_extractor = FeatureExtractor(model_config)
    dataset = Dataset(model_config, train_data, valid_data, test_data, feature_extractor)

    # Vocab processing
    if load_existing_dump:
        dataset.word2idx = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.word_vocab_file))
        dataset.idx2word = {idx: word for (word, idx) in dataset.word2idx.items()}
        dataset.pos2idx = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.pos_vocab_file))
        dataset.idx2pos = {idx: pos for (pos, idx) in dataset.pos2idx.items()}
        dataset.dep2idx = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.dep_vocab_file))
        dataset.idx2dep = {idx: dep for (dep, idx) in dataset.dep2idx.items()}

        dataset.model_config.load_existing_vocab = True
        print("loaded existing Vocab!")
        dataset.word_embedding_matrix = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.word_emb_file))
        dataset.pos_embedding_matrix = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.pos_emb_file))
        dataset.dep_embedding_matrix = get_pickle(os.path.join(DataConfig.dump_dir, DataConfig.dep_emb_file))
        print("loaded existing embedding matrix!")

    else:
        dataset.build_vocab()
        dump_pickle(dataset.word2idx, os.path.join(DataConfig.dump_dir, DataConfig.word_vocab_file))
        dump_pickle(dataset.pos2idx, os.path.join(DataConfig.dump_dir, DataConfig.pos_vocab_file))
        dump_pickle(dataset.dep2idx, os.path.join(DataConfig.dump_dir, DataConfig.dep_vocab_file))
        dataset.model_config.load_existing_vocab = True
        print("Vocab Build Done!")
        dataset.build_embedding_matrix()
        print("embedding matrix Build Done")
        dump_pickle(dataset.word_embedding_matrix, os.path.join(DataConfig.dump_dir, DataConfig.word_emb_file))
        dump_pickle(dataset.pos_embedding_matrix, os.path.join(DataConfig.dump_dir, DataConfig.pos_emb_file))
        dump_pickle(dataset.dep_embedding_matrix, os.path.join(DataConfig.dump_dir, DataConfig.dep_emb_file))

    print("converting data into ids..")
    dataset.convert_data_to_ids()
    print("Done!")
    dataset.model_config.word_features_types = len(dataset.train_inputs[0][0])
    dataset.model_config.pos_features_types = len(dataset.train_inputs[1][0])
    dataset.model_config.dep_features_types = len(dataset.train_inputs[2][0])
    dataset.model_config.num_features_types = dataset.model_config.word_features_types + \
                                              dataset.model_config.pos_features_types + dataset.model_config.dep_features_types
    # dataset.model_config.num_classes = len(dataset.train_targets[0])

    return dataset