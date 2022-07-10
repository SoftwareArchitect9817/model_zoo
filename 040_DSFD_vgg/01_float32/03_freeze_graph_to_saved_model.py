### tensorflow-gpu==1.15.2

import tensorflow as tf
from tensorflow.python import ops
import shutil

def get_graph_def_from_file(graph_filepath):
    tf.compat.v1.reset_default_graph()
    with ops.Graph().as_default():
        with tf.compat.v1.gfile.GFile(graph_filepath, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            return graph_def

def convert_graph_def_to_saved_model(export_dir, graph_filepath, input_name, outputs):
    graph_def = get_graph_def_from_file(graph_filepath)
    with tf.compat.v1.Session(graph=tf.Graph()) as session:
        tf.import_graph_def(graph_def, name='')
        tf.compat.v1.saved_model.simple_save(
            session,
            export_dir,# change input_image to node.name if you know the name
            inputs={input_name: session.graph.get_tensor_by_name('{}:0'.format(node.name))
                for node in graph_def.node if node.op=='Placeholder'},
            outputs={t.rstrip(":0"):session.graph.get_tensor_by_name(t) for t in outputs}
        )
        print('Optimized graph converted to SavedModel!')

shutil.rmtree('saved_model', ignore_errors=True)
convert_graph_def_to_saved_model('saved_model', 'detector_256x256.pb', 'tower_0/images', ['tower_0/boxes:0','tower_0/labels:0','tower_0/scores:0','tower_0/num_detections:0'])

"""
$ saved_model_cli show --dir saved_model_kitti --all

MetaGraphDef with tag-set: 'serve' contains the following SignatureDefs:

signature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['depth_prediction/raw_input'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 128, 416, 3)
        name: depth_prediction/raw_input:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['truediv'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 128, 416, 1)
        name: truediv:0
  Method name is: tensorflow/serving/predict
"""

"""
$ saved_model_cli show --dir saved_model_cityscapes --all

MetaGraphDef with tag-set: 'serve' contains the following SignatureDefs:

signature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['depth_prediction/raw_input'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 128, 416, 3)
        name: depth_prediction/raw_input:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['truediv'] tensor_info:
        dtype: DT_FLOAT
        shape: (1, 128, 416, 1)
        name: truediv:0
  Method name is: tensorflow/serving/predict

"""