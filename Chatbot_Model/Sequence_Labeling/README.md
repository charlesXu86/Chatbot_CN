# Sequential Labeling using BiLSTM+CRF
---
### Attention plz: `tensorflow` upgrades too much frequently causing the codes unrunnabel. But that still can be used to be a reference.
---
# @char embedding
### Input

```
N  B
B	M
A	E
D	O

an empty line

Z	O
Z	O
Z	O
```
### Output
```
NBAD\<@\>NBA
ZZZZZ\<@\>
```
---
# @word embedding
*same as `char embedding`*
```
I  B
like	M
you	E
,	O
……

```
---

# Installation Requirements
- python 3.5
- tensorflow 1.9
- numpy
- pandas

# References
- https://github.com/manubharghav/NER
- https://github.com/glample/tagger
- https://github.com/chilynn/sequence-labeling
