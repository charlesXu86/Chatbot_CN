import tensorflow as tf
#表示上下文（对话中提问的句子）的最大长度160个词，填充也填充到160个词
TEXT_FEATURE_SIZE = 160

def get_feature_columns(mode):
    # 存储tfrecord中每个样本的特征组合，包括context,context的长度，utterance，utterance的长度四种特征
  feature_columns = []

  feature_columns.append(tf.contrib.layers.real_valued_column(
    column_name="context", dimension=TEXT_FEATURE_SIZE, dtype=tf.int64))
  feature_columns.append(tf.contrib.layers.real_valued_column(
      column_name="context_len", dimension=1, dtype=tf.int64))
  feature_columns.append(tf.contrib.layers.real_valued_column(
      column_name="utterance", dimension=TEXT_FEATURE_SIZE, dtype=tf.int64))
  feature_columns.append(tf.contrib.layers.real_valued_column(
      column_name="utterance_len", dimension=1, dtype=tf.int64))

  if mode == tf.contrib.learn.ModeKeys.TRAIN:
    # 如果模型是训练，需要在输入中加入标签
    feature_columns.append(tf.contrib.layers.real_valued_column(
      column_name="label", dimension=1, dtype=tf.int64))

  if mode == tf.contrib.learn.ModeKeys.EVAL:
    # 如果模型在评估、测试过程中，不输入标签,但有干扰项
    # 本实验是一个正样本，九个负样本，负样本是随机生成的，
    # 评估时输入9个负样本的标志和长度
    for i in range(9):
      feature_columns.append(tf.contrib.layers.real_valued_column(
        column_name="distractor_{}".format(i), dimension=TEXT_FEATURE_SIZE, dtype=tf.int64))
      feature_columns.append(tf.contrib.layers.real_valued_column(
        column_name="distractor_{}_len".format(i), dimension=1, dtype=tf.int64))

  return set(feature_columns)

#因为需要在模型训练和测评时使用不用的输入函数，为防止重复书写代码，创建一个包装器（wrapper），针对不同的模型使用相应的代码
def create_input_fn(mode, input_files, batch_size, num_epochs):
  def input_fn():
    features = tf.contrib.layers.create_feature_spec_for_parsing(
        get_feature_columns(mode))

    feature_map = tf.contrib.learn.io.read_batch_features(
        file_pattern=input_files,
        batch_size=batch_size,
        features=features,
        reader=tf.TFRecordReader,
        randomize_input=True,
        num_epochs=num_epochs,
        queue_capacity=200000 + batch_size * 10,
        name="read_batch_features_{}".format(mode))

    # This is an ugly hack because of a current bug in tf.learn
    # During evaluation TF tries to restore the epoch variable which isn't defined during training
    # So we define the variable manually here
    # 手动定义验证代码
    if mode == tf.contrib.learn.ModeKeys.TRAIN:
      tf.get_variable(
        "read_batch_features_eval/file_name_queue/limit_epochs/epochs",
        initializer=tf.constant(0, dtype=tf.int64))

    if mode == tf.contrib.learn.ModeKeys.TRAIN:
      target = feature_map.pop("label")
    else:
      # 在评估过程中我们有10类回复（utterance），其中一个正确的，九个错误的
      # 并且第一个（索引为0的哪一个）是正确的（正样本）
      target = tf.zeros([batch_size, 1], dtype=tf.int64)
    return feature_map, target
  return input_fn
