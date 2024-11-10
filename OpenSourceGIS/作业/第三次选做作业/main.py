from osgeo import ogr

def read(path_input, field=None):
    '''Vector reading by ogr.'''
    
    # 打开输入的 shapefile 文件，以只读模式打开 (0 表示只读，1 表示读写)
    data_source = ogr.Open(path_input, 0)
    
    # 获取图层（shapefile 的主数据集包含一个图层）
    layer = data_source.GetLayer()
    
    # 获取字段数量（图层的定义中包含字段数量）
    count_fields = layer.GetLayerDefn().GetFieldCount()
    
    # 获取要素数量（图层中包含的要素数量）
    count_features = layer.GetFeatureCount()
    
    # 获取字段名列表：遍历字段定义，并提取每个字段的名称
    field_names = [layer.GetLayerDefn().GetFieldDefn(i).GetName() for i in range(count_fields)]
    
    # 初始化 unique_values 为 None，若未指定 field 参数则不需要唯一值
    unique_values = None
    
    # 检查是否指定了有效的字段名称，若有则获取该字段的唯一值并保持顺序
    if field and field in field_names:
        unique_values = []  # 初始化 unique_values 为空列表，用于存储唯一字段值
        for feature in layer:  # 遍历图层中的每个要素
            value = feature.GetField(field)  # 获取指定字段的值
            # 如果值不为空且尚未在 unique_values 中，添加该值
            if value is not None and value not in unique_values:
                unique_values.append(value)
    
    # 关闭数据源，以释放资源
    data_source = None
    
    # 返回字段数量、要素数量、字段名列表和唯一字段值列表（如果指定了字段）
    return count_fields, count_features, field_names, unique_values


def vec_sel(path_input, path_output, final_filter_expression):
    '''Feature selection by ogr.'''
    
    # 打开输入的 shapefile 文件，以只读模式打开
    data_source = ogr.Open(path_input, 0)
    
    # 获取图层（包含要素的主要数据集）
    layer = data_source.GetLayer()
    
    # 获取 shapefile 驱动，用于创建新的 shapefile 文件
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 创建一个新的 shapefile 文件，指定输出文件路径
    data_source_out = driver.CreateDataSource(path_output)

    # 创建输出图层，保持与输入图层一致的空间参考和几何类型
    layer_out = data_source_out.CreateLayer("selected_features",  # 输出图层名称
                                            geom_type=layer.GetGeomType(),  # 设置几何类型与输入图层一致
                                            srs=layer.GetSpatialRef(),  # 设置空间参考与输入图层一致
                                            options=['ENCODING=UTF-8']  # 将编码指定为 UTF-8
                                            )
    
    # 获取图层定义，用于遍历并复制字段
    layer_defn = layer.GetLayerDefn()
    
    # 遍历图层中的每个字段定义，将其添加到输出图层
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)  # 获取每个字段定义
        layer_out.CreateField(field_defn)  # 将字段定义添加到输出图层中
    
    # 设置筛选条件，将符合条件的要素保留
    layer.SetAttributeFilter(final_filter_expression)
    print(f"筛选条件: {final_filter_expression}")
    
    # 获取筛选后的要素数量，显示符合条件的要素数
    selected_feature_count = layer.GetFeatureCount()
    print(f"符合条件的要素数量为: {selected_feature_count}")
    
    # 如果有符合条件的要素，则将其写入输出图层
    if selected_feature_count > 0:
        for feature in layer:  # 遍历符合条件的要素
            layer_out.CreateFeature(feature.Clone())  # 克隆要素并写入到输出图层

    # 清理并关闭文件，移除筛选条件并释放数据源
    layer.SetAttributeFilter(None)
    data_source = None
    data_source_out = None

    # 显示要素选取完成消息
    print(f"要素选取完成，结果已保存到 {path_output}")


# 主程序
# 定义输入文件路径
path_input = 'data/data_Input/昆明市行政区划.shp'  # 输入的 shapefile 文件路径

# 调用 read 函数获取 shapefile 的字段数量、要素数量、字段名列表
count_fields, count_features, field_names, _ = read(path_input)

# 打印基本信息，显示字段数量和要素数量
print("字段数量:", count_fields)
print("要素数量:", count_features)
print("字段名：", ", ".join(field_names))

# 初始化筛选表达式列表，用于存储所有的筛选条件表达式
filter_expressions = []

# 循环以获取用户的筛选输入
while True:
    # 提示用户输入筛选字段的名称
    field_name = input("请输入要选择的字段名：")
    
    # 调用 read 函数获取指定字段的唯一值列表
    _, _, _, unique_values = read(path_input, field_name)
    print(f"字段 '{field_name}' 的唯一值列表：")
    print("、".join(unique_values))
    
    # 提示用户输入字段值，多个值使用顿号分隔
    user_input = input("请输入要选取的字段值（若有多个值以顿号分隔）：")
    field_values = [value.strip() for value in user_input.split("、")]  # 去除每个字段值的空格并分割成列表
    
    # 创建 OR 连接的筛选表达式，将用户选择的字段值生成筛选条件
    expression = " OR ".join([f"{field_name} = '{value}'" for value in field_values])

    # 检查是否已有条件，若已有则提示用户选择逻辑关系
    if filter_expressions:
        connect = input("请选择逻辑关系来连接条件 (与/或/非）：")
        
        # 根据用户选择的逻辑关系连接表达式
        if connect == "与":
            expression = f"({filter_expressions[-1]}) AND ({expression})"
            filter_expressions[-1] = expression  # 使用 AND 连接更新最后一个表达式
        elif connect == "或":
            expression = f"({filter_expressions[-1]}) OR ({expression})"
            filter_expressions[-1] = expression  # 使用 OR 连接更新最后一个表达式
        elif connect == "非":
            expression = f"NOT ({expression})"
            filter_expressions.append(expression)  # 添加 NOT 表达式
    else:
        # 如果这是第一个条件，直接添加到筛选表达式列表
        filter_expressions.append(expression)

    # 询问用户是否继续选择其他字段
    continue_choice = input("是否继续选择其他字段？（是/否）：")
    if continue_choice.lower() != "是":  # 若用户选择 "否"，则退出循环
        break

# 生成最终的筛选表达式，若有多个条件则使用最后一个条件
final_filter_expression = filter_expressions[-1] if filter_expressions else ""

# 定义输出文件路径，并调用 vec_sel 函数将符合条件的要素保存到新文件
path_output = 'data/data_output/kunming_feature.shp'
vec_sel(path_input, path_output, final_filter_expression)