# Mesh R-CNN

Mesh-RCNN方法需要通过Pytorch3d和detectron2两个代码库实现。

Pytorch3d的安装：

```sh
pip install pytorch3d
```

（注意，Pytorch版本必须是1.9.1才能成功运行Pytorch3d）

detectron2的安装：

```
git clone https://github.com/facebookresearch/detectron2.git
CC=clang CXX=clang++ ARCHFLAGS="-arch x86_64" python -m pip install -e detectron2
```

最终的测试命令：

```sh
python demo.py \
--config-file configs/pix3d/meshrcnn_R50_FPN.yaml \
--input IMG_7906.JPG \
--output output_demo \
--onlyhighest \
MODEL.WEIGHTS meshrcnn://meshrcnn_R50.pth MODEL.DEVICE 'cpu' 
```

这部分引用了MeshRCNN代码库的配置。
