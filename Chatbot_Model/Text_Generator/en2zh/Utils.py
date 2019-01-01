import datetime
import random
import re
import time
import unicodedata

import jieba
from torch import nn

from Config import *


def encode_text(word_map, c):
    return [word_map.get(word, word_map['<unk>']) for word in c] + [word_map['<end>']]


# Since we are dealing with batches of padded sequences, we cannot simply consider all elements of
# the tensor when calculating loss. We define maskNLLLoss to calculate our loss based on our
# decoder’s output tensor, the target tensor, and a binary mask tensor describing the padding of the
# target tensor. This loss function calculates the average negative log likelihood of the elements that
# correspond to a 1 in the mask tensor.
def maskNLLLoss(inp, target, mask):
    nTotal = mask.sum()
    crossEntropy = -torch.log(torch.gather(input=inp, dim=1, index=target.view(-1, 1)))
    loss = crossEntropy.masked_select(mask).mean()
    loss = loss.to(device)
    return loss, nTotal.item()


class AverageMeter(object):
    """
    Keeps track of most recent, average, sum, and count of a metric.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


# Exponentially weighted averages
class ExpoAverageMeter(object):
    # Exponential Weighted Average Meter
    def __init__(self, beta=0.9):
        self.reset()

    def reset(self):
        self.beta = 0.9
        self.val = 0
        self.avg = 0
        self.count = 0

    def update(self, val):
        self.val = val
        self.avg = self.beta * self.avg + (1 - self.beta) * self.val


def accuracy(scores, targets, k):
    """
    Computes top-k accuracy, from predicted and true labels.
    :param scores: scores from the model
    :param targets: true labels
    :param k: k in top-k accuracy
    :return: top-k accuracy
    """

    batch_size = targets.size(0)
    _, ind = scores.topk(k, 1, True, True)
    correct = ind.eq(targets.view(-1, 1).expand_as(ind))
    correct_total = correct.view(-1).float().sum()  # 0D tensor
    return correct_total.item() * (100.0 / batch_size)


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# Turn a Unicode string to plain ASCII, thanks to
# http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# Lowercase, trim, and remove non-letter characters

def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = s.strip()
    return s


def indexesFromSentence(voc, sentence):
    sentence_zh = sentence.strip()
    seg_list = jieba.cut(sentence_zh)
    return encode_text(voc.word2index, list(seg_list))


class GreedySearchDecoder(nn.Module):
    def __init__(self, encoder, decoder):
        super(GreedySearchDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, input_seq, input_length, max_length):
        # Forward input through encoder model
        encoder_outputs, encoder_hidden = self.encoder(input_seq, input_length)
        # Prepare encoder's final hidden layer to be first hidden input to the decoder
        decoder_hidden = encoder_hidden[:self.decoder.n_layers]
        # Initialize decoder input with SOS_token
        decoder_input = torch.ones(1, 1, device=device, dtype=torch.long) * SOS_token
        # Initialize tensors to append decoded words to
        all_tokens = torch.zeros([0], device=device, dtype=torch.long)
        all_scores = torch.zeros([0], device=device)
        # Iteratively decode one word token at a time
        for _ in range(max_length):
            # Forward pass through decoder
            decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs)
            # Obtain most likely word token and its softmax score
            decoder_scores, decoder_input = torch.max(decoder_output, dim=1)
            # Record token and score
            all_tokens = torch.cat((all_tokens, decoder_input), dim=0)
            all_scores = torch.cat((all_scores, decoder_scores), dim=0)
            # Prepare current token to be next decoder input (add a dimension)
            decoder_input = torch.unsqueeze(decoder_input, 0)
        # Return collections of word tokens and scores
        return all_tokens, all_scores


def evaluate(searcher, sentence, input_lang, output_lang, max_length=max_len):
    with torch.no_grad():
        ### Format input sentence as a batch
        # words -> indexes
        indexes_batch = [indexesFromSentence(input_lang, sentence)]
        # Create lengths tensor
        lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
        # Transpose dimensions of batch to match models' expectations
        input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
        # Use appropriate device
        input_batch = input_batch.to(device)
        lengths = lengths.to(device)
        # Decode sentence with searcher
        tokens, scores = searcher(input_batch, lengths, max_length)
        # indexes -> words
        decoded_words = [output_lang.index2word[token.item()] for token in tokens
                         if token != EOS_token and token != PAD_token]
    return decoded_words


def pick_n_valid_sentences(input_lang, output_lang, n):
    samples_path = 'data/samples_train.json'
    samples = json.load(open(samples_path, 'r'))
    train_count = int(len(samples) * train_split)
    samples = samples[train_count:]
    # samples = samples[:train_count]
    samples = random.sample(samples, n)
    result = []
    for sample in samples:
        input_sentence = ''.join([input_lang.index2word[token] for token in sample['input'] if token != EOS_token])
        target_sentence = ' '.join([output_lang.index2word[token] for token in sample['output'] if token != EOS_token])
        result.append((input_sentence, target_sentence))
    return result


def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def save_checkpoint(epoch, encoder, decoder, encoder_optimizer, decoder_optimizer, input_lang, output_lang, val_loss,
                    is_best):
    # Save checkpoint
    state = {
        'en': encoder.state_dict(),
        'de': decoder.state_dict(),
        'en_opt': encoder_optimizer.state_dict(),
        'de_opt': decoder_optimizer.state_dict(),
        'input_lang_dict': input_lang.__dict__,
        'output_lang_dict': output_lang.__dict__,
    }

    if is_best:
        ensure_folder(save_dir)
        filename = '{0}/checkpoint_{1}_{2:.3f}.tar'.format(save_dir, epoch, val_loss)
        torch.save(state, filename)

        # If this checkpoint is the best so far, store a copy so it doesn't get overwritten by a worse checkpoint
        torch.save(state, '{0}/BEST_checkpoint.tar'.format(save_dir))


def adjust_learning_rate(optimizer, shrink_factor):
    """
    Shrinks learning rate by a specified factor.
    :param optimizer: optimizer whose learning rate must be shrunk.
    :param shrink_factor: factor in interval (0, 1) to multiply learning rate with.
    """

    print("\nDECAYING learning rate.")
    for param_group in optimizer.param_groups:
        param_group['lr'] = param_group['lr'] * shrink_factor
    print("The new learning rate is %f\n" % (optimizer.param_groups[0]['lr'],))
