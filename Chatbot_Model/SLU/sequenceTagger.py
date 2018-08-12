'''
'''

import argparse
from basicModel import KerasModel

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--arch', dest='arch', type=str, default='lstm', help='architecture to use')
    parser.add_argument('--train', dest='train_data_path', type=str, help='path to datasets')
    parser.add_argument('--dev', dest='dev_data_path', type=str, help='path to datasets')
    parser.add_argument('--test', dest='test_data_path', type=str, help='path to datasets')
    parser.add_argument('--out', dest='result_path', type=str, help='path to datasets')
    parser.add_argument('--trainnum', dest='train_numfile', type=str, help='path to train num file')
    parser.add_argument('--devnum', dest='dev_numfile', type=str, help='path to dev num file')
    parser.add_argument('--testnum', dest='test_numfile', type=str, help='path to test num file')
   
    # network parameters
    parser.add_argument('--sgdtype', dest='sgdtype', type=str, default='adam', help='SGD type: sgd/rmsprop/adagrad/adadelta/adam/adamax')
    parser.add_argument('--momentum', dest='momentum', type=float, default=0.1, help='momentum for vanilla SGD')
    parser.add_argument('--decay_rate', dest='decay_rate', type=float, default=0.0, help='decay rate for sgd')
    parser.add_argument('--rho', dest='rho', type=float, default=0.9, help='rho for rmsprop/adadelta')
    parser.add_argument('--beta1', dest='beta1', type=float, default=0.9, help='beta1 for adam/adamax')
    parser.add_argument('--beta2', dest='beta2', type=float, default=0.999, help='beta2 for adam/adamax')
    parser.add_argument('-l', '--learning_rate', dest='learning_rate', type=float, default=1e-2, help='learning rate')
    parser.add_argument('-b', '--batch_size', dest='batch_size', type=int, default=10, help='batch size')
    parser.add_argument('-m', '--max_epochs', dest='max_epochs', type=int, default=300, help='maximum number of epochs to train the model')
    parser.add_argument('-a', '--output_att', dest='output_att', type=str, help='whether output the attention distribution')
    parser.add_argument('--iter_per_epoch', dest='iter_per_epoch', type=int, default=100, help='number of iterations per epoch')
    parser.add_argument('--hidden_size', dest='hidden_size', type=int, default=50, help='size of hidden layer')
    parser.add_argument('--embedding_size', dest='embedding_size', type=int, default=100, help='dimension of embeddings')
    parser.add_argument('--activation_func', dest='activation_func', type=str, default='tanh', help='activation function for hidden units: sigmoid, tanh, relu')
    parser.add_argument('--input_type', dest='input_type', type=str, default='1hot', help='input type, could be: 1hot/embedding/predefined')
    parser.add_argument('--embedding_file', dest='embedding_file', type = str, help='path to the embedding file')
    parser.add_argument('--init', dest='init_type', type = str, default='glorot_uniform', help='weight initialization function: glorot_uniform/glorot_normal/he_uniform/he_normal')
    parser.add_argument('--forget_bias', dest='forget_bias', type = float, default=1.0, help='LSTM parameter to set forget bias values')
  
    # regularization
    parser.add_argument('--smooth_eps', dest='smooth_eps', type=float, default=1e-8, help='epsilon smoothing for rmsprop/adagrad/adadelta/adam/adamax')
    parser.add_argument('--dropout', dest='dropout', type = bool, default=False, help='True/False for performing dropout')
    parser.add_argument('--dropout_ratio', dest='dropout_ratio', type = float, default=0.5, help='ratio of weights to drop')
    parser.add_argument('--time_length', dest='time_length', type = int, default=60, help='the number of timestamps in given sequences. Short utterances will be padded to this length')
    parser.add_argument('--his_length', dest='his_length', type = int, default=20, help='the number of history turns considered for making prediction')
    parser.add_argument('--mdl_path', dest='mdl_path', type = str, help='the directory of storing tmp models')
    parser.add_argument('--default', dest='default_flag', type = bool, default=True, help='whether use the default values for optimizers')
    parser.add_argument('--log', dest='log', type = str, default=None, help='the log file output')
    parser.add_argument('--record_epoch', dest='record_epoch', type = int, default=-1, help='how many epochs we predict once')
    parser.add_argument('--load_weight', dest='load_weight', help='the weight file for initialization')
    parser.add_argument('--combine_his', dest='combine_his', type = bool, default=False, help='whether combine his and current one for prediction')
    parser.add_argument('--time_decay', dest='time_decay', type = bool, default=False, help='whether add another matrix for modeling time decay')
    parser.add_argument('--shuffle', dest='shuffle', type = bool, default=True, help='whether shuffle the data')
    parser.add_argument('--set_batch', dest='set_batch', type = bool, default=False, help='whether set the batch size')
    parser.add_argument('--tag_format', dest='tag_format', type = str, default='conlleval', help='defined tag format conlleval/normal (defaul is for conlleval usage, normal one outputs a tag sequence for one sentence per line) ')
    parser.add_argument('--e2e', dest='e2e_flag', type = bool, default=False, help='whether only using the last turn (end-to-end training)')

    args = parser.parse_args()
    argparams = vars(args)

    KerasModel(argparams).run()

