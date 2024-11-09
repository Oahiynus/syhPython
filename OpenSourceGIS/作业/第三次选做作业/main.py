from osgeo import ogr, osr, gdal

# 设置输出编码为 UTF-8
gdal.SetConfigOption('SHAPE_ENCODING', 'UTF-8')

def read(path_input):  # path_input 为矢量数据路径
    '''Vector reading by ogr.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0) # 0 表示以只读方式打开, 1 表示以读写方式打开
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 获取字段数量
    count_fields = layer.GetLayerDefn().GetFieldCount()
    
    # 获取要素数量
    count_features = layer.GetFeatureCount()
    
    # 关闭数据源
    data_source = None
    
    # 返回字段数量和要素数量
    return count_fields, count_features


def vec_sel(path_input, path_output, field, field_value):  # path_input 为矢量数据路径, path_output 为输出路径, field 为字段, field_value 为字段值
    '''Feature selection by ogr with encoding support.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0) # 0 表示以只读方式打开, 1 表示以读写方式打开
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 创建输出的 shapefile 文件
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 创建一个新的 shapefile 文件，用于存储选取的要素
    data_source_out = driver.CreateDataSource(path_output)

    # 创建图层定义，用于定义输出图层的结构
    layer_out = data_source_out.CreateLayer("selected_features", 
                                   geom_type = layer.GetGeomType(), 
                                   srs = layer.GetSpatialRef() 
                                   ) ##创建图层，定义成一个面,空间参考与读入数据一致
    
    # 复制字段定义到输出图层
    layer_defn = layer.GetLayerDefn()

    # 写入每个字段特定信息
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        layer_out.CreateField(field_defn)
    
    # 设置字段过滤条件，根据 field 和 field_value 进行筛选
    filter_expression = f"{field} = '{field_value}'"
    layer.SetAttributeFilter(filter_expression)
    print(f"筛选条件: {filter_expression}")
    
    # 检查筛选后的要素数量
    selected_feature_count = layer.GetFeatureCount()
    print(f"符合条件的要素数量为: {selected_feature_count}")
    
    if selected_feature_count == 0:
        print("没有符合筛选条件的要素。")
    
    # 遍历筛选后的要素并写入输出图层
    for feature in layer:
        layer_out.CreateFeature(feature.Clone())
    
    # 创建 .cpg 文件，指定为 UTF-8 编码
    with open(path_output.replace('.shp', '.cpg'), 
              'w', 
              encoding='utf-8') as cpg_file: cpg_file.write('UTF-8')

    # 清理并关闭文件
    layer.SetAttributeFilter(None)  # 清除过滤条件
    data_source = None
    data_source_out = None

    print(f"要素选取完成，结果已保存到 {path_output}")

# 读取矢量数据的信息
path_input = 'E:/YNU/5/OpenSourceGIS/Assignment_3/data/矢量数据/昆明市行政区划.shp'  # 输入 shapefile 文件路径
count_fields, count_features = read(path_input)
print("字段数量:", count_fields)
print("要素数量:", count_features)

# 根据字段值进行要素选取并保存到新文件
path_output = 'E:/YNU/5/OpenSourceGIS/Assignment_3/data/output/kunming_feature.shp'  # 输出文件路径
field_name = "dt_name"  # 替换为实际字段名
field_value = "安宁市"  # 替换为实际字段值
vec_sel(path_input, path_output, field_name, field_value)