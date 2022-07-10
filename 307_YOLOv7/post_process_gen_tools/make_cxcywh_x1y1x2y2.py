#! /usr/bin/env python

import torch
import torch.nn as nn
import numpy as np
import onnx
from onnxsim import simplify
from argparse import ArgumentParser

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()

    def forward(self, cxcywh):
        x1 = (cxcywh[..., 0] - cxcywh[..., 2] / 2)[..., np.newaxis]  # top left x
        y1 = (cxcywh[..., 1] - cxcywh[..., 3] / 2)[..., np.newaxis]  # top left y
        x2 = (cxcywh[..., 0] + cxcywh[..., 2] / 2)[..., np.newaxis]  # bottom right x
        y2 = (cxcywh[..., 1] + cxcywh[..., 3] / 2)[..., np.newaxis]  # bottom right y
        x1y1x2y2 = torch.cat([x1,y1,x2,y2], dim=2)
        return x1y1x2y2


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-o',
        '--opset',
        type=int,
        default=11,
        help='onnx opset'
    )
    parser.add_argument(
        '-b',
        '--batches',
        type=int,
        default=1,
        help='batch size'
    )
    parser.add_argument(
        '-x',
        '--boxes',
        type=int,
        default=5040,
        help='boxes'
    )
    args = parser.parse_args()

    model = Model()

    MODEL = f'cxcywh_x1y1x2y2'
    OPSET=args.opset
    BATCHES = args.batches
    BOXES = args.boxes

    onnx_file = f"{MODEL}_{BOXES}.onnx"
    cxcywh = torch.randn(BATCHES, BOXES, 4)

    torch.onnx.export(
        model,
        args=(cxcywh),
        f=onnx_file,
        opset_version=OPSET,
        input_names = ['cxcywh'],
        output_names=['x1y1x2y2'],
    )
    model_onnx1 = onnx.load(onnx_file)
    model_onnx1 = onnx.shape_inference.infer_shapes(model_onnx1)
    onnx.save(model_onnx1, onnx_file)

    model_onnx2 = onnx.load(onnx_file)
    model_simp, check = simplify(model_onnx2)
    onnx.save(model_simp, onnx_file)
