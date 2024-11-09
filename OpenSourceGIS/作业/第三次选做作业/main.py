from osgeo import ogr, osr, gdal

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


def get_field_names(path_input):
    '''Retrieve all field names from the shapefile.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0)
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 获取字段名列表
    layer_defn = layer.GetLayerDefn()
    field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())]
    
    # 关闭数据源
    data_source = None
    
    return field_names


def get_unique_field_values(path_input, field):
    '''Retrieve unique values from a specified field, maintaining original order.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0)
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 使用列表来保持字段值的插入顺序
    unique_values = []
    for feature in layer:
        value = feature.GetField(field)
        if value is not None and value not in unique_values:
            unique_values.append(value)  # 如果值未在列表中，则添加
    
    # 关闭数据源
    data_source = None
    
    return unique_values


def vec_sel(path_input, path_output, filter_expressions):  # filter_expressions 为包含字段和字段值的筛选表达式列表
    '''Feature selection by ogr with encoding support for multiple values.'''
    
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
                                            geom_type=layer.GetGeomType(), 
                                            srs=layer.GetSpatialRef(), 
                                            options=['ENCODING=UTF-8']
                                            )  # 保持空间参考和编码系统一致
    
    # 复制字段定义到输出图层
    layer_defn = layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        layer_out.CreateField(field_defn)
    
    # 合并所有筛选条件
    filter_expression = " AND ".join(filter_expressions)
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
    with open(path_output.replace('.shp', '.cpg'), 'w', encoding='utf-8') as cpg_file:
        cpg_file.write('UTF-8')

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

# 设置筛选表达式列表
filter_expressions = []

while True:
    # 显示所有字段名供用户选择
    field_names = get_field_names(path_input)
    print("可选字段名：", ", ".join(field_names))
    field_name = input("请输入要选择的字段名：")
    
    # 获取该字段下的所有唯一值，并显示给用户
    unique_values = get_unique_field_values(path_input, field_name)
    print(f"字段 '{field_name}' 的唯一值列表：")
    print("、".join(unique_values))
    
    # 从输入字段值，并将其处理为列表
    user_input = input("请输入要选取的字段值（若有多个值以顿号分隔）：")
    field_values = [value.strip() for value in user_input.split("、")]
    
    # 创建筛选表达式
    expression = " OR ".join([f"{field_name} = '{value}'" for value in field_values])
    filter_expressions.append(f"({expression})")
    
    # 询问用户是否要继续选择其他字段
    continue_choice = input("是否继续选择其他字段？(是/否)：")
    if continue_choice.lower() != "是":
        break

# 根据字段值列表进行要素选取并保存到新文件
path_output = 'E:/YNU/5/OpenSourceGIS/Assignment_3/data/output/kunming_feature.shp'  # 输出文件路径
vec_sel(path_input, path_output, filter_expressions)
