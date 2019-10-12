import argparse
import sys
import tempfile
from time import time
import random
from os import listdir
from os.path import isfile, join


import pandas
import numpy as np
import tensorflow as tf
from sklearn import metrics


# model settings
# Static seed to allow for reproducability between training runs
tf.set_random_seed(12345)
trainingCycles = 500000  # Number of training steps before ending
batchSize = 1000  # Number of examples per training batch
summarySteps = 1000  # Number of training steps between each summary
dropout = 0.5  # Node dropout for training
nodeLayout = [40, 30, 20, 10]  # Layout of nodes in each layer


mainDirectory = str("./model_1/")

trainFiles = [f for f in listdir("./train/") if isfile(join("./train/", f))]
evalFiles = [f for f in listdir("./eval/") if isfile(join("./eval/", f))]


# Initialises data arrays
trainDataX = np.empty([0, 4])
trainDataY = np.empty([0, 2])
evalDataX = np.empty([0, 4])
evalDataY = np.empty([0, 2])


# Reads training data into memory
readPos = 0
for fileName in trainFiles:
    importedData = pandas.read_csv("./train/" + fileName, sep=',')

    xValuesDF = importedData[["RSI14", "RSI50", "STOCH14K", "STOCH14D"]]
    yValuesDF = importedData[["longOutput", "shortOutput"]]

    xValues = np.array(xValuesDF.values.tolist())
    yValues = np.array(yValuesDF.values.tolist())

    trainDataX = np.concatenate([trainDataX, xValues], axis=0)
    trainDataY = np.concatenate([trainDataY, yValues], axis=0)

    if readPos % 50 == 0 and readPos > 0:
        print("Loaded " + str(readPos) + " training files")

    readPos += 1
print("\n\n")


# Reads evalutation data into memory
readPos = 0
for fileName in evalFiles:
    importedData = pandas.read_csv("./eval/" + fileName, sep=',')

    xValuesDF = importedData[["RSI14", "RSI50", "STOCH14K", "STOCH14D"]]
    yValuesDF = importedData[["longOutput", "shortOutput"]]

    xValues = np.array(xValuesDF.values.tolist())
    yValues = np.array(yValuesDF.values.tolist())

    evalDataX = np.concatenate([evalDataX, xValues], axis=0)
    evalDataY = np.concatenate([evalDataY, yValues], axis=0)

    if readPos % 50 == 0 and readPos > 0:
        print("Loaded " + str(readPos) + " training files")

    readPos += 1
print("\n\n")


# used to sample batches from your data for training
def createTrainingBatch(amount):

    randomBatchPos = np.random.randint(0, trainDataX.shape[0], amount)

    xOut = trainDataX[randomBatchPos]
    yOut = trainDataY[randomBatchPos]

    return xOut, yOut


tf.logging.set_verbosity(tf.logging.INFO)

# ML training and evaluation functions
def train():
    globalStepTensor = tf.Variable(0, trainable=False, name='global_step')

    sess = tf.InteractiveSession()

    # placeholder for the input features
    x = tf.placeholder(tf.float32, [None, 4])
    # placeholder for the one-hot labels
    y = tf.placeholder(tf.float32, [None, 2])
    # placeholder for node dropout rate
    internalDropout = tf.placeholder(tf.float32, None)

    net = x  # input layer is the trading indicators

    # Creates the neural network model
    with tf.name_scope('network'):
        # Initialises each layer in the network
        layerPos = 0
        for units in nodeLayout:
            net = tf.layers.dense(
                net,
                units=units,
                activation=tf.nn.tanh,
                name=str(
                    "dense" +
                    str(units) +
                    "_" +
                    str(layerPos)))  # adds each layer to the networm as specified by nodeLayout
            # dropout layer after each layer
            net = tf.layers.dropout(net, rate=internalDropout)
            layerPos += 1

    logits = tf.layers.dense(
        net, 2, activation=tf.nn.softmax)  # network output

    with tf.name_scope('lossFunction'):
        cross_entropy_loss = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(
                labels=y,
                logits=logits))  # on NO account put this within a name scope - tensorboard shits itself

    with tf.name_scope('trainingStep'):
        tf.summary.scalar('crossEntropyLoss', cross_entropy_loss)
        trainStep = tf.train.AdamOptimizer(0.0001).minimize(
            cross_entropy_loss, global_step=globalStepTensor)

    with tf.name_scope('accuracy'):
        correctPrediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, tf.float32))
        tf.summary.scalar('accuracy', accuracy)

    merged = tf.summary.merge_all()
    trainWriter = tf.summary.FileWriter(
        mainDirectory + '/train', sess.graph, flush_secs=1, max_queue=2)
    evalWriter = tf.summary.FileWriter(
        mainDirectory + '/eval', sess.graph, flush_secs=1, max_queue=2)
    tf.global_variables_initializer().run()

    # Saves the model at defined checkpoints and loads any available model at
    # start-up
    saver = tf.train.Saver(max_to_keep=2, name="checkpoint")
    path = tf.train.get_checkpoint_state(mainDirectory)
    if path is not None:
        saver.restore(sess, tf.train.latest_checkpoint(mainDirectory))

    lastTime = time()
    while tf.train.global_step(sess, globalStepTensor) <= trainingCycles:
        globalStep = tf.train.global_step(sess, globalStepTensor)

        # generates batch for each training cycle
        xFeed, yFeed = createTrainingBatch(batchSize)

        # Record summaries and accuracy on both train and eval data
        if globalStep % summarySteps == 0:
            currentTime = time()
            totalTime = (currentTime - lastTime)
            print(str(totalTime) + " seconds, " +
                  str(summarySteps / totalTime) + " steps/sec")
            lastTime = currentTime

            summary, accuracyOut, _ = sess.run([
                merged,
                accuracy,
                trainStep
            ],
                feed_dict={
                    x: xFeed,
                    y: yFeed,
                    internalDropout: dropout
                })
            trainWriter.add_summary(summary, globalStep)
            trainWriter.flush()
            print('Train accuracy at step %s: %s' % (globalStep, accuracyOut))

            summary, accuracyOut = sess.run([
                merged,
                accuracy,
            ],
                feed_dict={
                    x: evalDataX,
                    y: evalDataY,
                    internalDropout: 0
                })
            evalWriter.add_summary(summary, globalStep)
            evalWriter.flush()
            print('Eval accuracy at step %s: %s' % (globalStep, accuracyOut))

            print("\n\n")
            saver.save(sess, save_path=str(mainDirectory + "model"),
                       global_step=globalStep)  # saves a snapshot of the model

        else:  # Training cycle
            _ = sess.run(
                [trainStep], feed_dict={
                    x: xFeed,
                    y: yFeed,
                    internalDropout: dropout
                })

    trainWriter.close()
    evalWriter.close()


train()
