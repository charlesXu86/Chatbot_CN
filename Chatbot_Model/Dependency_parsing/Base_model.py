import tensorflow as tf


class Model(object):
    """Abstracts a Tensorflow graph for a learning task.

    We use various Model classes as usual abstractions to encapsulate tensorflow
    computational graphs. Each algorithm you will construct in this homework will
    inherit from a Model object.
    """


    def add_placeholders(self):
        raise NotImplementedError("Each Model must re-implement this method.")


    def create_feed_dict(self, inputs_batch, labels_batch=None):
        raise NotImplementedError("Each Model must re-implement this method.")


    def add_prediction_op(self):
        raise NotImplementedError("Each Model must re-implement this method.")


    def add_loss_op(self, pred):
        raise NotImplementedError("Each Model must re-implement this method.")


    def add_accuracy_op(self, pred):
        raise NotImplementedError("Each Model must re-implement this method.")


    def add_training_op(self, loss):
        raise NotImplementedError("Each Model must re-implement this method.")


    def train_on_batch(self, sess, inputs_batch, labels_batch):
        feed = self.create_feed_dict(inputs_batch, labels_batch=labels_batch)
        _, loss = sess.run([self.train_op, self.loss], feed_dict=feed)
        return loss


    def predict_on_batch(self, sess, inputs_batch):
        feed = self.create_feed_dict(inputs_batch)
        predictions = sess.run(self.pred, feed_dict=feed)
        return predictions


    def print_trainable_varibles(self):
        print("\n******** Model Trainable Variables :: <name, shape> ********")
        for name, shape in zip(map(lambda x: x.name, tf.trainable_variables()),
                               map(lambda x: x.get_shape(), tf.trainable_variables())):
            print ("variable: {} \t shape: {}".format(name, shape))

        print("*" * 70)


    def build(self):
        self.add_placeholders()
        self.pred = self.add_cube_prediction_op()
        #self.pred = self.add_prediction_op()
        self.loss = self.add_loss_op(self.pred)
        self.accuracy = self.add_accuracy_op(self.pred)
        self.train_op = self.add_training_op(self.loss)
