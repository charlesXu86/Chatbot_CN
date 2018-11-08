# ID-CNN-CWS
Source codes and corpora of paper "Iterated Dilated Convolutions for Chinese Word Segmentation".

![2017-10-20_13-23-31](http://wx3.sinaimg.cn/large/006Fmjmcly1fkpa3q8maej30dh0c2jup.jpg)


It implements the following `4` models for CWS:

- Bi-LSTM
- Bi-LSTM-CRF
- ID-CNN
- ID-CNN-CRF

## Dependencies

- Python >= 3.6
- TensorFlow >= 1.2

Both CPU and GPU are supported. GPU training is `10` times faster.

## Preparation

Run following script to convert corpus to TensorFlow dataset.

```
$ ./scripts/make.sh
```

## Train and Test

### Quick Start

```
$ ./scripts/run.sh $dataset $model
```

- `$dataset` can be `pku`, `msr`, `asSC` or `cityuSC`.
- `$model` can be `cnn` or `bilstm`.

For example:

```
$ ./scripts/run.sh pku cnn
```

It will train a `cnn` model on `pku` dataset, then evaluate performance on test set.

### CRF Layer

To enable CRF layer, simply append `--viterbi` to your command, e.g.

```
$ ./scripts/run.sh pku cnn --viterbi
```

## Accuracy

![2017-10-20_13-25-11](http://wx1.sinaimg.cn/large/006Fmjmcly1fkpa3in2haj30dq0h9q8u.jpg)


## Speed

![2017-10-20_11-44-42](http://wx3.sinaimg.cn/large/006Fmjmcly1fkp6wafcngj30d407l0th.jpg)

## Acknowledgments

- Corpora are from SIGHAN05, converted to Simplified Chinese via [HanLP](https://github.com/hankcs/HanLP). Note that the SIGHAN datasets should only be used for research purposes.
- Model implementations adopted from https://github.com/iesl/dilated-cnn-ner by [Emma Strubell](https://cs.umass.edu/~strubell).

