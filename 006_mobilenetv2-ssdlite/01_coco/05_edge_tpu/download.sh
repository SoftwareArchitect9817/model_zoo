#!/bin/bash

fileid="1_8bFUcATFt5apHpA4Ym9GyJNo2_dGz-M"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ssdlite_mobilenet_v2_coco_300_full_integer_quant_edgetpu.tflite

echo Download finished.
