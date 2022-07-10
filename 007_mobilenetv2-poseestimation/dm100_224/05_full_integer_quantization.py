### tensorflow==2.3.0-rc1

import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

def representative_dataset_gen():
  for data in raw_test_data.take(100):
    image = data['image'].numpy()
    image = tf.image.resize(image, (368, 432))
    image = image[np.newaxis,:,:,:]
    image = image - 127.5
    image = image * 0.007843
    yield [image]

raw_test_data, info = tfds.load(name="coco/2017", with_info=True, split="test", data_dir="~/TFDS", download=False)

# Full Integer Quantization - Input/Output=int8
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
converter.representative_dataset = representative_dataset_gen
tflite_quant_model = converter.convert()
with open('mobilenet_v2_pose_368x432_dm100_full_integer_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Integer Quantization complete! - mobilenet_v2_pose_368x432_dm100_full_integer_quant.tflite")
