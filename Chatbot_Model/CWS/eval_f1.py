from __future__ import division
from __future__ import print_function
import time
import numpy as np
import sys

from utils import CWSEvaluator, bmes_to_words


def is_start(curr):
    return curr[0] == "B" or curr[0] == "S"


def is_continue(curr):
    return curr[0] == "M"


def is_background(curr):
    return not is_start(curr) and not is_continue(curr)


def is_seg_start(curr, prev):
    return (is_start(curr) and not is_continue(curr)) or (
        is_continue(curr) and (prev is None or is_background(prev) or prev[1:] != curr[1:]))


def segment_eval(batches, predictions, labels_id_str_map, vocab_id_str_map, pad_width, start_end, logger,
                 extra_text=""):
    if extra_text != "":
        logger.info(extra_text)

    def print_context(width, start, tok_list, pred_list, gold_list):
        for offset in range(-width, width + 1):
            idx = offset + start
            if 0 <= idx < len(tok_list):
                logger.info("%s\t%s\t%s" % (
                    vocab_id_str_map[tok_list[idx]], labels_id_str_map[pred_list[idx]],
                    labels_id_str_map[gold_list[idx]]))
        logger.info()

    prf = CWSEvaluator(labels_id_str_map)
    # iterate over batches
    for predictions, (dev_label_batch, dev_token_batch, _, _, dev_seq_len_batch, _, _) in zip(predictions, batches):
        # iterate over examples in batch
        for preds, labels, tokens, seq_lens in zip(predictions, dev_label_batch, dev_token_batch, dev_seq_len_batch):
            start = pad_width
            for seq_len in seq_lens:
                predicted = preds[start:seq_len + start]
                golds = labels[start:seq_len + start]
                toks = tokens[start:seq_len + start]
                prf.add_instance(predicted, golds)
                start += seq_len + (2 if start_end else 1) * pad_width

    prf = prf.result()
    logger.info('{}\t{:04.2f}\t{:04.2f}\t{:04.2f}'.format('AVG', prf[0], prf[1], prf[2]))
    return prf


def print_training_error(num_examples, start_time, epoch_losses, step, logger):
    losses_str = ' '.join(["%5.5f"] * len(epoch_losses)) % tuple(map(lambda l: l / step, epoch_losses))
    logger.info("%20d examples at %5.2f examples/sec. Error: %s" %
                (num_examples, num_examples / (time.time() - start_time), losses_str))
    sys.stdout.flush()


def output_predicted_to_file(out_filename, eval_batches, predictions, labels_id_str_map, vocab_id_str_map, pad_width):
    with open(out_filename, 'w') as preds_file:
        sentence_count = 0
        for prediction, (
                label_batch, token_batch, shape_batch, char_batch, seq_len_batch, tok_len_batch,
                eval_mask_batch) in zip(
            predictions, eval_batches):
            for preds, labels, tokens, seq_lens in zip(prediction, label_batch, token_batch, seq_len_batch):
                start = pad_width
                for seq_len in seq_lens:
                    if seq_len != 0:
                        preds_nopad = list(map(lambda t: labels_id_str_map[t], preds[start:seq_len + start]))
                        tokens_nopad = list(map(lambda t: vocab_id_str_map[t], tokens[start:seq_len + start]))
                        start += pad_width + seq_len
                        words = bmes_to_words(tokens_nopad, preds_nopad)
                        print(" ".join(words), file=preds_file)
                        sentence_count += 1
