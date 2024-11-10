from osgeo import ogr

def read(path_input, field=None):
    '''Retrieve shapefile information: field and feature counts, field names, and unique values of a specified field.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0) # 0 表示以只读方式打开, 1 表示以读写方式打开
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 获取字段数量
    count_fields = layer.GetLayerDefn().GetFieldCount()
    
    # 获取要素数量
    count_features = layer.GetFeatureCount()
    
    # 获取字段名列表
    field_names = [layer.GetLayerDefn().GetFieldDefn(i).GetName() for i in range(count_fields)]
    
    # 获取指定字段的唯一值，并使用列表来保持字段值的插入顺序
    unique_values = None
    if field and field in field_names:
        unique_values = []
        for feature in layer:
            value = feature.GetField(field)
            if value is not None and value not in unique_values:
                unique_values.append(value)  # 如果值未在列表中，则添加
    
    # 关闭数据源
    data_source = None
    
    return count_fields, count_features, field_names, unique_values


def vec_sel(path_input, path_output, final_filter_expression):
    '''Feature selection by ogr with encoding support for multiple values.'''
    
    # 打开输入的 shapefile 文件
    data_source = ogr.Open(path_input, 0) # 0 表示以只读方式打开, 1 表示以读写方式打开
    
    # 获取图层
    layer = data_source.GetLayer()
    
    # 创建输出的 shapefile 文件
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 创建一个新的 shapefile 文件，用于存储选取的要素
    data_source_out = driver.CreateDataSource(path_output)

    # 创建输出图层，保持空间参考和编码系统一致
    layer_out = data_source_out.CreateLayer("selected_features", 
                                            geom_type=layer.GetGeomType(),
                                            srs=layer.GetSpatialRef(), 
                                            options=['ENCODING=UTF-8'] # 创建 .cpg 文件，指定为 UTF-8 编码
                                            )
    
    # 复制字段定义到输出图层
    layer_defn = layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        layer_out.CreateField(field_defn)
    
    # 应用筛选条件
    layer.SetAttributeFilter(final_filter_expression)
    print(f"筛选条件: {final_filter_expression}")
    
    # 检查筛选后的要素数量
    selected_feature_count = layer.GetFeatureCount()
    print(f"符合条件的要素数量为: {selected_feature_count}")
    
    if selected_feature_count > 0:
        # 遍历筛选后的要素并写入输出图层
        for feature in layer:
            layer_out.CreateFeature(feature.Clone())

    # 清理并关闭文件
    layer.SetAttributeFilter(None)  # 清除过滤条件
    data_source = None
    data_source_out = None

    print(f"要素选取完成，结果已保存到 {path_output}")

# 主程序逻辑
path_input = 'E:/YNU/5/OpenSourceGIS/Assignment_3/data/矢量数据/昆明市行政区划.shp'  # 输入的 shapefile 文件路径

# 调用 read 函数获取 shapefile 的字段数量、要素数量、字段名列表和唯一字段值（初始化为 None，待用户选择字段后再获取唯一值）
count_fields, count_features, field_names, unique_values = read(path_input)  

# 打印基本信息
print("字段数量:", count_fields)
print("要素数量:", count_features)
print("字段名：", ", ".join(field_names))

# 设置筛选表达式
filter_expressions = []  # 用于存储所有的筛选条件表达式

while True:

    field_name = input("请输入要选择的字段名：")
    
    print(f"字段 '{field_name}' 的唯一值列表：")
    print("、".join(unique_values))
    
    # 用户输入字段值，并将其处理为列表
    user_input = input("请输入要选取的字段值（若有多个值以顿号分隔）：")
    field_values = [value.strip() for value in user_input.split("、")]
    
    # 创建筛选表达式，并添加到筛选表达式列表中
    expression = " OR ".join([f"{field_name} = '{value}'" for value in field_values])
    filter_expressions.append(f"({expression})")  # 将生成的筛选表达式添加到列表中
    
    # 询问是否要继续选择其他字段
    continue_choice = input("是否继续选择其他字段？（是/否）：")
    if continue_choice.lower() != "是":
        break  # 如果选择 "否"，则结束筛选循环

# 将所有筛选条件用 " OR " 连接，生成最终的筛选表达式
final_filter_expression = " OR ".join(filter_expressions)  

# 根据字段值列表进行要素选取并保存到新文件
path_output = 'E:/YNU/5/OpenSourceGIS/Assignment_3/data/output/kunming_feature.shp'  # 输出文件路径
vec_sel(path_input, path_output, final_filter_expression)  # 调用 vec_sel 函数执行筛选并保存