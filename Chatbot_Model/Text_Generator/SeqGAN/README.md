# SeqGAN_tensorflow

This code is used to reproduce the result of synthetic data experiments in "SeqGAN: Sequence Generative Adversarial Nets with Policy Gradient" (Yu et.al). It replaces the original tensor array implementation with higher level tensorflow API for better flexibility.

## Introduction
The baisc idea of SeqGAN is to regard sequence generator as an agent in reinforcement learning. To train this agent, it applies REINFORCE (Williams, 1992) algorithm to train the generator and a discriminator is trained to provide the reward. To calculate the reward of partially generated sequence, Monte-Carlo sampling is used to rollout the unfinished sequence to get the estimated reward.
![seqgan](https://github.com/ChenChengKuan/SeqGAN_tensorflow/blob/master/misc/seqgan.png)

Some works based on training method used in SeqGAN:
   * Recurrent Topic-Transition GAN for Visual Paragraph Generation (Liang et.al, ICCV 2017)
   * Towards Diverse and Natural Image Descriptions via a Conditional GAN (Dai et.al, ICCV 2017)
   * Show, Adapt and Tell: Adversarial Training of Cross-domain Image Captioner (Chen et.al, ICCV 2017)
   * Adversarial Ranking for Language Generation (Lin et.al, NIPS 2017)
   * Long Text Generation via Adversarial Training with Leaked Information (Guo et.al, AAAI 2018)

## Prerequisites
   * Python 3.5.3
   * Tensorflow 1.9
## Run the code
Simply run `python train.py` will start the training process. It will first pretrain the generator and discriminator then start adversarial training.

## Results
The output in experiment.log would be something similar to below, which is close to reported result in [original implementation](https://github.com/LantaoYu/SeqGAN)
```
pre-training...
epoch:	0	nll:	10.1971
epoch:	5	nll:	9.4694
epoch:	10	nll:	9.2169
epoch:	15	nll:	9.17986
epoch:	20	nll:	9.16206
epoch:	25	nll:	9.1344
epoch:	30	nll:	9.12127
epoch:	35	nll:	9.0948
epoch:	40	nll:	9.10186
epoch:	45	nll:	9.10108
epoch:	50	nll:	9.0971
epoch:	55	nll:	9.11246
epoch:	60	nll:	9.1182
epoch:	65	nll:	9.10095
epoch:	70	nll:	9.09244
epoch:	75	nll:	9.08816
epoch:	80	nll:	9.10319
epoch:	85	nll:	9.08916
epoch:	90	nll:	9.08348
epoch:	95	nll:	9.09661
epoch:	100	nll:	9.10361
epoch:	105	nll:	9.11718
epoch:	110	nll:	9.10492
epoch:	115	nll:	9.1038
adversarial training...
epoch:	0	nll:	9.09558
epoch:	5	nll:	9.03083
epoch:	10	nll:	8.96725
epoch:	15	nll:	8.91415
epoch:	20	nll:	8.87554
epoch:	25	nll:	8.82305
epoch:	30	nll:	8.76805
epoch:	35	nll:	8.73597
epoch:	40	nll:	8.71933
epoch:	45	nll:	8.71653
epoch:	50	nll:	8.71746
epoch:	55	nll:	8.7036
epoch:	60	nll:	8.68666
epoch:	65	nll:	8.68931
epoch:	70	nll:	8.68588
epoch:	75	nll:	8.69977
epoch:	80	nll:	8.69636
epoch:	85	nll:	8.69916
epoch:	90	nll:	8.6969
epoch:	95	nll:	8.71021
epoch:	100	nll:	8.72561
epoch:	105	nll:	8.71369
epoch:	110	nll:	8.71723
epoch:	115	nll:	8.72388
epoch:	120	nll:	8.71293
epoch:	125	nll:	8.70667
epoch:	130	nll:	8.70341
epoch:	135	nll:	8.69929
epoch:	140	nll:	8.69793
epoch:	145	nll:	8.67705
epoch:	150	nll:	8.65372
```
Note: Part of this code (dataloader, discriminator, target LSTM) is based on [original implementation by Lantao Yu](https://github.com/LantaoYu/SeqGAN). Many thanks to his code
