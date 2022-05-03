import os
from structure import sfm


dataset_path = 'dataset/building'
spare_path = dataset_path+'/sparse'
dense_path = dataset_path+'/dense'
image_path = dataset_path+'/images'

if not os.path.exists(spare_path):
    os.mkdir(spare_path)

if not os.path.exists(dense_path):
    os.mkdir(dense_path)

# 图像特征提取
os.system(
    'colmap feature_extractor'+
    ' --database_path {}'.format(dataset_path+'/database.db')+ 
    ' --image_path {}'.format(image_path)
)

# 特征点匹配
os.system(
    'colmap exhaustive_matcher'+
    ' --database_path {}'.format(dataset_path+'/database.db')
)

# 稀疏重建（SFM）
os.system(
    'colmap mapper'+
    ' --database_path {}'.format(dataset_path+'/database.db')+
    ' --image_path {}'.format(image_path) +
    ' --output_path {}'.format(spare_path)
)
sfm(dataset_path,image_path,spare_path)

# 图像去畸变
os.system(
    'colmap image_undistorter'+ 
    ' --image_path {}'.format(image_path) +
    ' --input_path {}'.format(os.path.join(spare_path, '0')) +
    ' --output_path {}'.format(dense_path) + 
    ' --output_type COLMAP --max_image_size 2000'
)
# 稠密重建
os.system(
    'colmap patch_match_stereo'+
    ' --workspace_path {}'.format(dense_path) +
    ' --workspace_format COLMAP'+
    ' --PatchMatchStereo.geom_consistency true'
)
# 特征融合
os.system(
    'colmap stereo_fusion' +
    ' --workspace_path {}'.format(dense_path) +
    ' --workspace_format COLMAP' +
    ' --input_type geometric' +
    ' --output_path {}'.format(os.path.join(dense_path, 'fused.ply'))
)
# 可视化
# 稀疏重建结果可视化
os.system(
    'colmap poisson_mesher'+
    ' --input_path {}'.format(os.path.join(dense_path, 'fused.ply')) +
    ' --output_path {}'.format(os.path.join(dense_path, 'meshed-poisson.ply'))
)

os.system(
    'colmap delaunay_mesher'+
    ' --input_path {}'.format(dense_path) +
    ' --output_path {}'.format(os.path.join(dense_path, 'meshed-delaunay.ply'))
)
