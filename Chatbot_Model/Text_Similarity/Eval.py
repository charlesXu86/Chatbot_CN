# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     Eval.py
   Description :   模型验证
   Author :       charl
   date：          2018/11/26
-------------------------------------------------
   Change Activity: 2018/11/26:
-------------------------------------------------
"""

import tensorflow as tf
import numpy as np

from Input_helper import InputHelper


# Parameters
# ==================================================

# Eval Parameters
# 批大小
BATCH_SIZE = 64
# 验证集文件
EVAL_FILEPATH = 'validation.txt0'
# 词表（在训练过程中已生成）
VOCAB_FILEPATH = 'runs/1528462228/checkpoints/vocab'
# 模型文件
MODEL = 'runs/1528462228/checkpoints/model-10000'

# 语句最多长度(包含多少个词)
MAX_DOCUMENT_LENGTH = 30

# Misc Parameters
ALLOW_SOFT_PLACEMENT = True
LOG_DEVICE_PLACEMENT = False

inpH = InputHelper()

x1_test, x2_test, y_test = inpH.getTestDataSet(EVAL_FILEPATH, VOCAB_FILEPATH, MAX_DOCUMENT_LENGTH)

# for index ,value in enumerate(x1_test):
#     print (index, x1_test[index], x2_test[index], y_test[index])
# sys.exit(0)

print("\nEvaluating...\n")

# Evaluation
# ==================================================
checkpoint_file = MODEL
print(checkpoint_file)

graph = tf.Graph
with graph.as_default():
    session_conf = tf.ConfigProto(   # 对session进行参数配置
        allow_soft_placement = ALLOW_SOFT_PLACEMENT,
        log_device_placement = LOG_DEVICE_PLACEMENT
    )
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        # Load the saved meta graph and restore variable
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        sess.run(tf.initialize_all_variables())
        saver.restore(sess, checkpoint_file)

        # Get the placeholers from the graph by name
        input_x1 = graph.get_operation_by_name("input_x1").outputs[0]
        input_x2 = graph.get_operation_by_name("input_x2").outputs[0]
        input_y = graph.get_operation_by_name("input_y").outputs[0]

        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        predictions = graph.get_operation_by_name("output/distance").outputs[0]
        accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]
        sim = graph.get_operation_by_name("accuracy/temp_sim").outputs[0]

        # Generate batches for one epoch
        batches = inpH.batch_iter(list(zip(x1_test, x2_test, y_test)), 2 * BATCH_SIZE, 1, shuffle=False)
        # Collect the predictions here
        all_predictions = []
        all_d = []
        for db in batches:
            x1_dev_b, x2_dev_b, y_dev_b = zip(*db)
            batch_predictions, batch_acc, batch_sim = sess.run([predictions, accuracy, sim],
                                                               {input_x1: x1_dev_b, input_x2: x2_dev_b,
                                                                input_y: y_dev_b, dropout_keep_prob: 1.0})
            all_predictions = np.concatenate([all_predictions, batch_predictions])
            print('batch_predictions',batch_predictions)
            all_d = np.concatenate([all_d, batch_sim])
            print('DEV acc {}'.format(batch_acc))
        for ex in all_predictions:
            print('ex', ex)
        correct_predictions = float(np.mean(all_d == y_test))
        print("Accuracy: {:g}".format(correct_predictions))