import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

def representative_dataset_gen():
  for data in raw_test_data.take(100):
    image = data['image'].numpy()
    image = tf.image.resize(image, (300, 300))
    image = image[np.newaxis,:,:,:]
    yield [image]


#tf.compat.v1.enable_eager_execution()

raw_test_data, info = tfds.load(name="voc/2007", with_info=True, split="validation", data_dir="~/TFDS", download=False)

# Integer Quantization - Input/Output=float32
converter = tf.lite.TFLiteConverter.from_saved_model('./saved_model')
converter.experimental_new_converter = True
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset_gen
tflite_quant_model = converter.convert()
with open('./ssdlite_mobilenet_v2_voc_300_integer_quant.tflite', 'wb') as w:
    w.write(tflite_quant_model)
print("Integer Quantization complete! - ssdlite_mobilenet_v2_voc_300_integer_quant.tflite")
