import sys
import time
import tensorflow as tf
import numpy as np
from data_utils import SeqBatcher, Batcher
from cnn import CNN
from bilstm import BiLSTM
from bilstm_char import BiLSTMChar
from cnn_char import CNNChar
import eval_f1 as evaluation
import json
import tf_utils
from os import listdir
import os
import logging
from utils import make_sure_path_exists

FLAGS = tf.app.flags.FLAGS


def main(argv):
    print("CUDA_VISIBLE_DEVICES=", os.environ.get('CUDA_VISIBLE_DEVICES', 0))

    train_dir = FLAGS.train_dir
    dev_dir = FLAGS.dev_dir
    maps_dir = FLAGS.maps_dir

    logger = init_logger()
    logger.info(' '.join(sys.argv) + '\n')

    if FLAGS.evaluate_only:
        if FLAGS.load_dir == '':
            FLAGS.load_dir = FLAGS.model_dir
        if FLAGS.load_dir == '':
            logger.error('Must supply load_dir in evaluation mode')
            sys.exit(1)
    if train_dir == '':
        logger.error('Must supply input data directory generated from tsv_to_tfrecords.py')
        sys.exit(1)

    logger.info('\n'.join(sorted(["%s : %s" % (str(k), str(v)) for k, v in FLAGS.__dict__['__flags'].items()])))

    with open(maps_dir + '/label.txt', 'r') as f:
        labels_str_id_map = {l.split('\t')[0]: int(l.split('\t')[1].strip()) for l in f.readlines()}
        labels_id_str_map = {i: s for s, i in labels_str_id_map.items()}
        labels_size = len(labels_id_str_map)
    with open(maps_dir + '/token.txt', 'r') as f:
        vocab_str_id_map = {l.split('\t')[0]: int(l.split('\t')[1].strip()) for l in f.readlines()}
        vocab_id_str_map = {i: s for s, i in vocab_str_id_map.items()}
        vocab_size = len(vocab_id_str_map)
    with open(maps_dir + '/shape.txt', 'r') as f:
        shape_str_id_map = {l.split('\t')[0]: int(l.split('\t')[1].strip()) for l in f.readlines()}
        shape_id_str_map = {i: s for s, i in shape_str_id_map.items()}
        shape_domain_size = len(shape_id_str_map)
    with open(maps_dir + '/char.txt', 'r') as f:
        char_str_id_map = {l.split('\t')[0]: int(l.split('\t')[1].strip()) for l in f.readlines()}
        char_id_str_map = {i: s for s, i in char_str_id_map.items()}
        char_domain_size = len(char_id_str_map)

    # with open(maps_dir + '/sizes.txt', 'r') as f:
    #     num_train_examples = int(f.readline()[:-1])

    logger.info("num classes: %d" % labels_size)

    size_files = [maps_dir + "/" + fname for fname in listdir(maps_dir) if fname.find("sizes") != -1]
    num_train_examples = 0
    num_tokens = 0
    for size_file in size_files:
        logger.info(size_file)
        with open(size_file, 'r') as f:
            num_train_examples += int(f.readline()[:-1])
            num_tokens += int(f.readline()[:-1])

    logger.info("num train examples: %d" % num_train_examples)
    logger.info("num train tokens: %d" % num_tokens)

    dev_top_dir = '/'.join(dev_dir.split("/")[:-2]) if dev_dir.find("*") != -1 else dev_dir
    logger.info(dev_top_dir)
    dev_size_files = [dev_top_dir + "/" + fname for fname in listdir(dev_top_dir) if fname.find("sizes") != -1]
    num_dev_examples = 0
    num_dev_tokens = 0
    for size_file in dev_size_files:
        logger.info(size_file)
        with open(size_file, 'r') as f:
            num_dev_examples += int(f.readline()[:-1])
            num_dev_tokens += int(f.readline()[:-1])

    logger.info("num dev examples: %d" % num_dev_examples)
    logger.info("num dev tokens: %d" % num_dev_tokens)

    # with open(dev_dir + '/sizes.txt', 'r') as f:
    #     num_dev_examples = int(f.readline()[:-1])

    type_set = {}
    type_int_int_map = {}
    outside_set = ["O", "<PAD>", "<S>", "</S>", "<ZERO>"]
    for label, id in labels_str_id_map.items():
        label_type = label if label in outside_set else label[2:]
        if label_type not in type_set:
            type_set[label_type] = len(type_set)
        type_int_int_map[id] = type_set[label_type]
    logger.info(type_set)  # All NER types

    # load embeddings, if given; initialize in range [-.01, .01]
    embeddings_shape = (vocab_size - 1, FLAGS.embed_dim)
    embeddings = tf_utils.embedding_values(embeddings_shape, old=False)
    used_words = set()
    if FLAGS.embeddings != '':
        with open(FLAGS.embeddings, 'r') as f:
            for line in f.readlines():
                split_line = line.strip().split(" ")
                if len(split_line) != FLAGS.embed_dim + 1:
                    continue
                word = split_line[0]
                embedding = split_line[1:]
                if word in vocab_str_id_map:
                    used_words.add(word)
                    # shift by -1 because we are going to add a 0 constant vector for the padding later
                    embeddings[vocab_str_id_map[word] - 1] = list(map(float, embedding))
    embeddings_used = len(used_words)
    logger.info("Loaded %d/%d embeddings (%2.2f%% coverage)" % (
        embeddings_used, vocab_size, embeddings_used / vocab_size * 100))

    layers_map = sorted(json.loads(FLAGS.layers.replace("'", '"')).items()) if FLAGS.model == 'cnn' else None

    pad_width = int(layers_map[0][1]['width'] / 2) if layers_map is not None else 1

    with tf.Graph().as_default():
        train_batcher = Batcher(train_dir, FLAGS.batch_size) if FLAGS.memmap_train else SeqBatcher(train_dir,
                                                                                                   FLAGS.batch_size)

        dev_batch_size = FLAGS.batch_size  # num_dev_examples
        dev_batcher = SeqBatcher(dev_dir, dev_batch_size, num_buckets=0, num_epochs=1)
        if FLAGS.ontonotes:
            domain_dev_batchers = {domain: SeqBatcher(dev_dir.replace('*', domain),
                                                      dev_batch_size, num_buckets=0, num_epochs=1)
                                   for domain in ['bc', 'nw', 'bn', 'wb', 'mz', 'tc']}

        train_eval_batch_size = FLAGS.batch_size
        train_eval_batcher = SeqBatcher(train_dir, train_eval_batch_size, num_buckets=0, num_epochs=1)

        char_embedding_model = BiLSTMChar(char_domain_size, FLAGS.char_dim, int(FLAGS.char_tok_dim / 2)) \
            if FLAGS.char_dim > 0 and FLAGS.char_model == "lstm" else \
            (CNNChar(char_domain_size, FLAGS.char_dim, FLAGS.char_tok_dim, layers_map[0][1]['width'])
             if FLAGS.char_dim > 0 and FLAGS.char_model == "cnn" else None)
        char_embeddings = char_embedding_model.outputs if char_embedding_model is not None else None

        if FLAGS.model == 'cnn':
            model = CNN(
                num_classes=labels_size,
                vocab_size=vocab_size,
                shape_domain_size=shape_domain_size,
                char_domain_size=char_domain_size,
                char_size=FLAGS.char_tok_dim,
                embedding_size=FLAGS.embed_dim,
                shape_size=FLAGS.shape_dim,
                nonlinearity=FLAGS.nonlinearity,
                layers_map=layers_map,
                viterbi=FLAGS.viterbi,
                projection=FLAGS.projection,
                loss=FLAGS.loss,
                margin=FLAGS.margin,
                repeats=FLAGS.block_repeats,
                share_repeats=FLAGS.share_repeats,
                char_embeddings=char_embeddings,
                embeddings=embeddings)
        elif FLAGS.model == "bilstm":
            model = BiLSTM(
                num_classes=labels_size,
                vocab_size=vocab_size,
                shape_domain_size=shape_domain_size,
                char_domain_size=char_domain_size,
                char_size=FLAGS.char_dim,
                embedding_size=FLAGS.embed_dim,
                shape_size=FLAGS.shape_dim,
                nonlinearity=FLAGS.nonlinearity,
                viterbi=FLAGS.viterbi,
                hidden_dim=FLAGS.lstm_dim,
                char_embeddings=char_embeddings,
                embeddings=embeddings)
        else:
            logger.info(FLAGS.model + ' is not a valid model type')
            sys.exit(1)

        # Define Training procedure
        global_step = tf.Variable(0, name='global_step', trainable=False)

        optimizer = tf.train.AdamOptimizer(learning_rate=model.lr, beta1=FLAGS.beta1, beta2=FLAGS.beta2,
                                           epsilon=FLAGS.epsilon, name="optimizer")

        model_vars = tf.global_variables()

        logger.info("model vars: %d" % len(model_vars))
        logger.info(map(lambda v: v.name, model_vars))

        # todo put in func
        total_parameters = 0
        for variable in tf.trainable_variables():
            # shape is an array of tf.Dimension
            shape = variable.get_shape()
            variable_parametes = 1
            for dim in shape:
                variable_parametes *= dim.value
            total_parameters += variable_parametes
        logger.info("Total trainable parameters: %d" % (total_parameters))

        if FLAGS.clip_norm > 0:
            grads, _ = tf.clip_by_global_norm(tf.gradients(model.loss, model_vars), FLAGS.clip_norm)
            train_op = optimizer.apply_gradients(zip(grads, model_vars), global_step=global_step)
        else:
            train_op = optimizer.minimize(model.loss, global_step=global_step, var_list=model_vars)

        tf.global_variables_initializer()

        opt_vars = [optimizer.get_slot(s, n) for n in optimizer.get_slot_names() for s in model_vars if
                    optimizer.get_slot(s, n) is not None]
        model_vars += opt_vars

        if FLAGS.load_dir:
            reader = tf.train.NewCheckpointReader(FLAGS.load_dir + "/model.tf")
            saved_var_map = reader.get_variable_to_shape_map()
            intersect_vars = [k for k in tf.global_variables() if
                              k.name.split(':')[0] in saved_var_map and k.get_shape() == saved_var_map[
                                  k.name.split(':')[0]]]
            leftovers = [k for k in tf.global_variables() if
                         k.name.split(':')[0] not in saved_var_map or k.get_shape() != saved_var_map[
                             k.name.split(':')[0]]]
            logger.warning("WARNING: Loading pretrained model, but not loading: " + ' '.join(
                list(map(lambda v: v.name, leftovers))))
            loader = tf.train.Saver(var_list=intersect_vars)

        else:
            loader = tf.train.Saver(var_list=model_vars)

        saver = tf.train.Saver(var_list=model_vars)

        sv = tf.train.Supervisor(logdir=FLAGS.model_dir if FLAGS.model_dir != '' else None,
                                 global_step=global_step,
                                 saver=None,
                                 save_model_secs=0,
                                 save_summaries_secs=0)

        training_start_time = time.time()
        with sv.managed_session(FLAGS.master, config=tf.ConfigProto(allow_soft_placement=True)) as sess:
            def run_evaluation(eval_batches, output=None, extra_text=""):
                predictions = []
                for b, (eval_label_batch, eval_token_batch, eval_shape_batch, eval_char_batch, eval_seq_len_batch,
                        eval_tok_len_batch, eval_mask_batch) in enumerate(eval_batches):
                    batch_size, batch_seq_len = eval_token_batch.shape

                    char_lens = np.sum(eval_tok_len_batch, axis=1)
                    max_char_len = np.max(eval_tok_len_batch)
                    eval_padded_char_batch = np.zeros((batch_size, max_char_len * batch_seq_len))
                    for b in range(batch_size):
                        char_indices = [item for sublist in [range(i * max_char_len, i * max_char_len + d) for i, d in
                                                             enumerate(eval_tok_len_batch[b])] for item in sublist]
                        eval_padded_char_batch[b, char_indices] = eval_char_batch[b][:char_lens[b]]

                    char_embedding_feeds = {} if FLAGS.char_dim == 0 else {
                        char_embedding_model.input_chars: eval_padded_char_batch,
                        char_embedding_model.batch_size: batch_size,
                        char_embedding_model.max_seq_len: batch_seq_len,
                        char_embedding_model.token_lengths: eval_tok_len_batch,
                        char_embedding_model.max_tok_len: max_char_len
                    }

                    basic_feeds = {
                        model.input_x1: eval_token_batch,
                        model.input_x2: eval_shape_batch,
                        model.input_y: eval_label_batch,
                        model.input_mask: eval_mask_batch,
                        model.max_seq_len: batch_seq_len,
                        model.batch_size: batch_size,
                        model.sequence_lengths: eval_seq_len_batch
                    }

                    basic_feeds.update(char_embedding_feeds)
                    total_feeds = basic_feeds.copy()

                    if FLAGS.viterbi:
                        preds, transition_params = sess.run([model.predictions, model.transition_params],
                                                            feed_dict=total_feeds)

                        viterbi_repad = np.empty((batch_size, batch_seq_len))
                        for batch_idx, (unary_scores, sequence_lens) in enumerate(zip(preds, eval_seq_len_batch)):
                            viterbi_sequence, _ = tf.contrib.crf.viterbi_decode(unary_scores, transition_params)
                            viterbi_repad[batch_idx] = viterbi_sequence
                        predictions.append(viterbi_repad)
                    else:
                        preds, scores = sess.run([model.predictions, model.unflat_scores], feed_dict=total_feeds)
                        predictions.append(preds)

                if output is not None:
                    evaluation.output_predicted_to_file(
                        (FLAGS.model_dir if FLAGS.model_dir != '' else FLAGS.load_dir) + "/" + output + ".txt",
                        eval_batches,
                        predictions, labels_id_str_map,
                        vocab_id_str_map, pad_width)

                # print evaluation
                precision, recall, f1_micro = evaluation.segment_eval(eval_batches, predictions, labels_id_str_map,
                                                                      vocab_id_str_map,
                                                                      pad_width=pad_width, start_end=FLAGS.start_end,
                                                                      logger=logger,
                                                                      extra_text="Segment evaluation %s:" % extra_text)

                return f1_micro, precision

            threads = tf.train.start_queue_runners(sess=sess)
            log_every = int(max(100, num_train_examples / 5))

            if FLAGS.load_dir != '':
                logger.info("Deserializing model: " + FLAGS.load_dir + "/model.tf")
                loader.restore(sess, FLAGS.load_dir + "/model.tf")

            def get_dev_batches(seq_batcher):
                batches = []
                # load all the dev batches into memory
                done = False
                while not done:
                    try:
                        dev_batch = sess.run(seq_batcher.next_batch_op)
                        dev_label_batch, dev_token_batch, dev_shape_batch, dev_char_batch, dev_seq_len_batch, dev_tok_len_batch = dev_batch
                        mask_batch = np.zeros(dev_token_batch.shape)
                        actual_seq_lens = np.add(np.sum(dev_seq_len_batch, axis=1),
                                                 (2 if FLAGS.start_end else 1) * pad_width * (
                                                     (dev_seq_len_batch != 0).sum(axis=1) + (
                                                         0 if FLAGS.start_end else 1)))
                        for i, seq_len in enumerate(actual_seq_lens):
                            mask_batch[i, :seq_len] = 1
                        batches.append((dev_label_batch, dev_token_batch, dev_shape_batch, dev_char_batch,
                                        dev_seq_len_batch, dev_tok_len_batch, mask_batch))
                    except:
                        done = True
                return batches

            dev_batches = get_dev_batches(dev_batcher)
            train_batches = []
            if FLAGS.train_eval:
                # load all the train batches into memory
                done = False
                while not done:
                    try:
                        train_batch = sess.run(train_eval_batcher.next_batch_op)
                        train_label_batch, train_token_batch, train_shape_batch, train_char_batch, train_seq_len_batch, train_tok_len_batch = train_batch
                        mask_batch = np.zeros(train_token_batch.shape)
                        actual_seq_lens = np.add(np.sum(train_seq_len_batch, axis=1),
                                                 (2 if FLAGS.start_end else 1) * pad_width * (
                                                     (train_seq_len_batch != 0).sum(axis=1) + (
                                                         0 if FLAGS.start_end else 1)))
                        for i, seq_len in enumerate(actual_seq_lens):
                            mask_batch[i, :seq_len] = 1
                        train_batches.append((train_label_batch, train_token_batch, train_shape_batch, train_char_batch,
                                              train_seq_len_batch, train_tok_len_batch, mask_batch))
                    except Exception as e:
                        done = True
            if FLAGS.memmap_train:
                train_batcher.load_and_bucket_data(sess)

            def train(max_epochs, best_score, model_hidden_drop, model_input_drop, until_convergence, max_lower=6,
                      min_iters=20):
                logger.info("Training on %d sentences (%d examples)" % (num_train_examples, num_train_examples))
                start_time = time.time()
                train_batcher._step = 1.0
                converged = False
                examples = 0
                log_every_running = log_every
                epoch_loss = 0.0
                num_lower = 0
                training_iteration = 0
                speed_num = 0.0
                speed_denom = 0.0
                while not sv.should_stop() and training_iteration < max_epochs and not (
                            until_convergence and converged):
                    # evaluate
                    if examples >= num_train_examples:
                        training_iteration += 1
                        FLAGS.lr = FLAGS.lr * FLAGS.lr_decay

                        if FLAGS.train_eval:
                            run_evaluation(train_batches,
                                           'train-out-{}'.format(training_iteration) if FLAGS.print_preds else None,
                                           "TRAIN (iteration %d)" % training_iteration)
                        logger.info('')
                        f1_micro, precision = run_evaluation(dev_batches, 'dev-out-{}'.format(
                            training_iteration) if FLAGS.print_preds else None,
                                                             "DEV (iteration %d)" % training_iteration)
                        logger.info("Avg training speed: %.2f examples/second" % (speed_num / speed_denom))

                        # keep track of running best / convergence heuristic
                        if f1_micro > best_score:
                            best_score = f1_micro
                            num_lower = 0
                            if FLAGS.model_dir != '' and best_score > FLAGS.save_min:
                                save_path = saver.save(sess, FLAGS.model_dir + "/model.tf")
                                logger.info("- best score! Serialized model: %s" % save_path)
                        else:
                            num_lower += 1
                        if num_lower > max_lower and training_iteration > min_iters:
                            converged = True

                        if f1_micro < 90.:
                            logger.info('Score too low, break to save time')
                            # os.system('rm -f ' + FLAGS.model_dir + "/model.tf*")  # remove old model, otherwise conflict
                            break

                        # update per-epoch variables
                        log_every_running = log_every
                        examples = 0
                        epoch_loss = 0.0
                        start_time = time.time()

                    if examples > log_every_running:
                        speed_denom += time.time() - start_time
                        speed_num += examples
                        evaluation.print_training_error(examples, start_time, [epoch_loss], train_batcher._step, logger)
                        log_every_running += log_every

                    # Training iteration

                    label_batch, token_batch, shape_batch, char_batch, seq_len_batch, tok_lengths_batch = \
                        train_batcher.next_batch() if FLAGS.memmap_train else sess.run(train_batcher.next_batch_op)

                    # make mask out of seq lens
                    batch_size, batch_seq_len = token_batch.shape

                    char_lens = np.sum(tok_lengths_batch, axis=1)
                    max_char_len = np.max(tok_lengths_batch)
                    padded_char_batch = np.zeros((batch_size, max_char_len * batch_seq_len))
                    for b in range(batch_size):
                        char_indices = [item for sublist in [range(i * max_char_len, i * max_char_len + d) for i, d in
                                                             enumerate(tok_lengths_batch[b])] for item in sublist]
                        padded_char_batch[b, char_indices] = char_batch[b][:char_lens[b]]

                    max_sentences = max(map(len, seq_len_batch))
                    new_seq_len_batch = np.zeros((batch_size, max_sentences))
                    for i, seq_len_list in enumerate(seq_len_batch):
                        new_seq_len_batch[i, :len(seq_len_list)] = seq_len_list
                    seq_len_batch = new_seq_len_batch
                    num_sentences_batch = np.sum(seq_len_batch != 0, axis=1)

                    mask_batch = np.zeros((batch_size, batch_seq_len)).astype("int")
                    actual_seq_lens = np.add(np.sum(seq_len_batch, axis=1),
                                             (2 if FLAGS.start_end else 1) * pad_width * (
                                                 num_sentences_batch + (0 if FLAGS.start_end else 1))).astype('int')
                    for i, seq_len in enumerate(actual_seq_lens):
                        mask_batch[i, :seq_len] = 1
                    examples += batch_size

                    # apply word dropout
                    # create word dropout mask
                    word_probs = np.random.random(token_batch.shape)
                    drop_indices = np.where(
                        (word_probs > FLAGS.word_dropout) & (token_batch != vocab_str_id_map["<PAD>"]))
                    token_batch[drop_indices[0], drop_indices[1]] = vocab_str_id_map["<OOV>"]

                    char_embedding_feeds = {} if FLAGS.char_dim == 0 else {
                        char_embedding_model.input_chars: padded_char_batch,
                        char_embedding_model.batch_size: batch_size,
                        char_embedding_model.max_seq_len: batch_seq_len,
                        char_embedding_model.token_lengths: tok_lengths_batch,
                        char_embedding_model.max_tok_len: max_char_len,
                        char_embedding_model.input_dropout_keep_prob: FLAGS.char_input_dropout
                    }

                    if FLAGS.model == "cnn":
                        cnn_feeds = {
                            model.input_x1: token_batch,
                            model.input_x2: shape_batch,
                            model.input_y: label_batch,
                            model.input_mask: mask_batch,
                            model.max_seq_len: batch_seq_len,
                            model.sequence_lengths: seq_len_batch,
                            model.batch_size: batch_size,
                            model.hidden_dropout_keep_prob: model_hidden_drop,
                            model.input_dropout_keep_prob: model_input_drop,
                            model.middle_dropout_keep_prob: FLAGS.middle_dropout,
                            model.l2_penalty: FLAGS.l2,
                            model.drop_penalty: FLAGS.regularize_drop_penalty,
                            model.lr: FLAGS.lr
                        }
                        cnn_feeds.update(char_embedding_feeds)
                        _, loss = sess.run([train_op, model.loss], feed_dict=cnn_feeds)
                    elif FLAGS.model == "bilstm":
                        lstm_feed = {
                            model.input_x1: token_batch,
                            model.input_x2: shape_batch,
                            model.input_y: label_batch,
                            model.input_mask: mask_batch,
                            model.sequence_lengths: seq_len_batch,
                            model.max_seq_len: batch_seq_len,
                            model.batch_size: batch_size,
                            model.hidden_dropout_keep_prob: FLAGS.hidden_dropout,
                            model.middle_dropout_keep_prob: FLAGS.middle_dropout,
                            model.input_dropout_keep_prob: FLAGS.input_dropout,
                            model.l2_penalty: FLAGS.l2,
                            model.drop_penalty: FLAGS.regularize_drop_penalty,
                            model.lr: FLAGS.lr
                        }
                        lstm_feed.update(char_embedding_feeds)
                        _, loss = sess.run([train_op, model.loss], feed_dict=lstm_feed)
                    epoch_loss += loss
                    train_batcher._step += 1
                return best_score, training_iteration, speed_num / speed_denom

            if FLAGS.evaluate_only:
                if FLAGS.train_eval:
                    run_evaluation(train_batches, 'train-out' if FLAGS.print_preds else None, "(train)")
                logger.info('')
                training_start_time = time.time()
                run_evaluation(dev_batches, 'test-out' if FLAGS.print_preds else None, "(test)")
            else:
                best_score, training_iteration, train_speed = train(FLAGS.max_epochs, 0.0,
                                                                    FLAGS.hidden_dropout, FLAGS.input_dropout,
                                                                    until_convergence=FLAGS.until_convergence)
                if FLAGS.model_dir:
                    logger.info("Deserializing model: " + FLAGS.model_dir + "/model.tf")
                    saver.restore(sess, FLAGS.model_dir + "/model.tf")

            total_time = time.time() - training_start_time
            sv.coord.request_stop()
            sv.coord.join(threads)
            sess.close()

            if FLAGS.evaluate_only:
                logger.info("Testing time: %d seconds" % (total_time))
            else:
                logger.info("Training time: %d minutes, %d iterations (%3.2f minutes/iteration)" % (
                    total_time / 60, training_iteration, total_time / (60 * training_iteration)))
                logger.info("Avg training speed: %.2f examples/second" % (train_speed))
                logger.info("Best dev F1: %2.2f" % (best_score))


def init_logger():
    log_formatter = logging.Formatter("%(message)s")
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    root_dir = FLAGS.model_dir if FLAGS.model_dir != '' else FLAGS.load_dir
    make_sure_path_exists(root_dir)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    file_handler = logging.FileHandler("{0}/info.log".format(root_dir), mode='a')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    return logger


if __name__ == '__main__':
    tf.app.flags.DEFINE_string('train_dir', '', 'directory containing preprocessed training data')
    tf.app.flags.DEFINE_string('dev_dir', '',
                               'directory containing preprocessed dev data or test data(when perform testing)')
    tf.app.flags.DEFINE_string('maps_dir', '', 'directory containing data intmaps')

    tf.app.flags.DEFINE_string('model_dir', '', 'save model to this dir (if empty do not save)')
    tf.app.flags.DEFINE_string('load_dir', '', 'load model from this dir (if empty do not load)')

    tf.app.flags.DEFINE_string('optimizer', 'adam', 'optimizer to use')
    tf.app.flags.DEFINE_string('master', '', 'use for Supervisor')
    tf.app.flags.DEFINE_string('model', 'cnn', 'which model to use [cnn, bilstm]')
    tf.app.flags.DEFINE_integer('filter_size', 3, "filter size")

    tf.app.flags.DEFINE_float('lr', 0.001, 'learning rate')
    tf.app.flags.DEFINE_float('lr_decay', 1.0, 'learning rate decay')
    tf.app.flags.DEFINE_float('l2', 0.0, 'l2 penalty')
    tf.app.flags.DEFINE_float('beta1', 0.9, 'beta1')
    tf.app.flags.DEFINE_float('beta2', 0.999, 'beta2')
    tf.app.flags.DEFINE_float('epsilon', 1e-8, 'epsilon')

    tf.app.flags.DEFINE_float('hidden_dropout', .75, 'hidden layer dropout rate')
    tf.app.flags.DEFINE_float('input_dropout', 1.0, 'input layer (word embedding) dropout rate')
    tf.app.flags.DEFINE_float('middle_dropout', 1.0, 'middle layer dropout rate')
    tf.app.flags.DEFINE_float('word_dropout', 1.0, 'whole-word (-> oov) dropout rate')

    tf.app.flags.DEFINE_float('clip_norm', 0, 'clip gradients to have norm <= this')
    tf.app.flags.DEFINE_integer('batch_size', 128, 'batch size')
    tf.app.flags.DEFINE_integer('lstm_dim', 2048, 'lstm internal dimension')
    tf.app.flags.DEFINE_integer('embed_dim', 50, 'word embedding dimension')
    tf.app.flags.DEFINE_integer('shape_dim', 5, 'shape embedding dimension')
    tf.app.flags.DEFINE_integer('char_dim', 0, 'character embedding dimension')
    tf.app.flags.DEFINE_integer('char_tok_dim', 0, 'character token embedding dimension')
    tf.app.flags.DEFINE_string('char_model', 'lstm', 'character embedding model (lstm, cnn)')

    tf.app.flags.DEFINE_integer('max_finetune_epochs', 100, 'train for this many epochs')
    tf.app.flags.DEFINE_integer('max_context_epochs', 100, 'train for this many epochs')

    tf.app.flags.DEFINE_integer('max_epochs', 100, 'train for this many epochs')

    tf.app.flags.DEFINE_integer('log_every', 2, 'log status every k steps')
    tf.app.flags.DEFINE_string('embeddings', '', 'file of pretrained embeddings to use')
    tf.app.flags.DEFINE_string('nonlinearity', 'relu', 'nonlinearity function to use (tanh, sigmoid, relu, swish)')
    tf.app.flags.DEFINE_boolean('until_convergence', False, 'whether to run until convergence')
    tf.app.flags.DEFINE_boolean('evaluate_only', False, 'whether to only run evaluation')
    tf.app.flags.DEFINE_string('layers', '', 'json definition of layers (dilation, filters, width)')
    tf.app.flags.DEFINE_string('print_preds', False,
                               'print out predictions (for eval script) to given file (or do not if False)')
    tf.app.flags.DEFINE_boolean('viterbi', False, 'whether to use viberbi inference')
    tf.app.flags.DEFINE_boolean('train_eval', False, 'whether to report train accuracy')
    tf.app.flags.DEFINE_boolean('memmap_train', True, 'whether to load all training examples into memory')
    tf.app.flags.DEFINE_boolean('projection', False, 'whether to do final halving projection (front end)')

    tf.app.flags.DEFINE_integer('block_repeats', 1, 'number of times to repeat the stacked dilations block')
    tf.app.flags.DEFINE_boolean('share_repeats', True, 'whether to share parameters between blocks')

    tf.app.flags.DEFINE_string('loss', 'mean', '')
    tf.app.flags.DEFINE_float('margin', 1.0, 'margin')

    tf.app.flags.DEFINE_float('char_input_dropout', 1.0, 'dropout for character embeddings')

    tf.app.flags.DEFINE_float('save_min', 0.0, 'min accuracy before saving')

    tf.app.flags.DEFINE_boolean('start_end', False, 'whether using start/end or just pad between sentences')
    tf.app.flags.DEFINE_float('regularize_drop_penalty', 0.0, 'penalty for dropout regularization')

    tf.app.flags.DEFINE_boolean('documents', False, 'whether each example is a document (default: sentence)')
    tf.app.flags.DEFINE_boolean('ontonotes', False, 'evaluate each domain of ontonotes seperately')

    tf.app.run()
