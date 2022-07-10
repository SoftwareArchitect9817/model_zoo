### tensorflow==2.2.0

import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

def representative_dataset_gen():
  for data in raw_test_data.take(10):
    image = data['image'].numpy()
    image = tf.image.resize(image, (416, 416))
    image = image[np.newaxis,:,:,:]
    image = image / 255.
    yield [image]

raw_test_data, info = tfds.load(name="voc/2007", with_info=True, split="validation", data_dir="~/TFDS", download=False)

# Integer Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_saved_model('./saved_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS,tf.lite.OpsSet.SELECT_TF_OPS]
converter.experimental_new_converter = False
converter.representative_dataset = representative_dataset_gen
tflite_quant_model = converter.convert()
with open('yolov4_416_integer_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Integer Quantization complete! - yolov4_416_integer_quant.tflite")
