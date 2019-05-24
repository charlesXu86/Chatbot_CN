import tensorflow as tf
import functools
from tensorflow.contrib.learn.python.learn.metric_spec import MetricSpec

#tensorflow 自带recall@k评价指标，为了使用这个指标，需要建一个字典，key为指标名称，value为对应的计算函数。
#return {'recall%1':fun1,'recall%2':fun2,'recall%5':fun5,'recall%10':fun10}
def create_evaluation_metrics():
    eval_metrics = {}
    for k in [1, 2, 5, 10]:
        eval_metrics["recall_at_%d" % k] = MetricSpec(metric_fn=functools.partial(
            tf.contrib.metrics.streaming_sparse_recall_at_k,
            k=k))
    return eval_metrics
