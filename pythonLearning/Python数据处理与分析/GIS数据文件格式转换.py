## 类定义和初始化方法
class ShapefileReader:
    '''
    1.__init__方法
    含义: 这是一个构造方法, 用于初始化ShapefileReader类的实例。
    原理: 当创建一个ShapefileReader对象时, 这个方法会被自动调用, 用于设置初始状态。
    作用机理: 
    self.shp_file_path: 存储传入的Shapefile文件路径, 这个路径将在后续的文件读取操作中使用。
    self.shapes: 初始化一个空列表, 用于存储从Shapefile文件中解析出的点数据。这个列表将在整个类的其他方法中填充数据, 并最终用于生成GeoJSON。
    该方法的核心作用是准备读取Shapefile文件的路径, 并为后续存储点数据提供结构支持。
    '''
    def __init__(self, shp_file_path):
        self.shp_file_path = shp_file_path  # Shapefile文件路径
        self.shapes = []  # 用于存储从Shapefile中读取的点信息

## 读取字节方法
    '''
    2.read_bytes方法
    含义: 
    从文件中读取指定数量的字节数据。
    原理: 
    Shapefile是一个二进制文件, 它的数据是按字节存储的。通过这个方法, 可以从文件对象中逐字节地读取指定长度的数据块。
    作用机理: 
    方法接收一个文件对象和要读取的字节数, 并返回读取到的字节内容。它用于处理Shapefile文件中的各种部分(如文件头、记录头、几何数据等), 
    确保可以精确地访问文件中的每一部分数据。
    '''
    def read_bytes(self, f, num_bytes):
        # 从文件中读取指定数量的字节, 并返回这些字节作为字节对象
        return f.read(num_bytes)
    
## 读取X、Y坐标信息方法
    '''
    3.read_double方法
    含义: 
    解析Shapefile文件中以小端方式存储的X、Y坐标信息。(64位)。
    原理: 
    Shapefile使用IEEE754标准(Shapefile的官方文档要求), 该标准定义了浮点数的二进制格式, 
    包括符号位、指数部分和尾数部分。Shapefile的存储格式为小端, 即最低有效位(LSB)在最低地址处。该方法按照这个格式解析一个8字节的双精度浮点数。
    作用机理: 
    读取8个字节的数据, 并按照小端模式进行解析。先解析符号位(位于最高位), 然后解析指数(11位)和尾数(52位)。根据这些解析出的值, 计算并返回浮点数的实际值。
    该方法的作用是确保可以正确解析Shapefile中存储的坐标值(X和Y坐标), 是几何数据解析的核心部分。
    '''
    def read_double(self, f):
        bytes_data = self.read_bytes(f, 8)  # 读取8字节的数据
        
        # 使用小端模式解析X、Y坐标信息
        # 解析符号位: 如果最高位为1, 则为负数, 否则为正数
        sign = -1 if (bytes_data[7] & 0x80) else 1
        
        # 解析指数部分(11位): 从第7个字节的低7位和第6个字节的高4位组成
        exponent = ((bytes_data[7] & 0x7F) << 4) | (bytes_data[6] >> 4)
        
        # 解析尾数部分(52位): 从剩余的字节中提取
        mantissa = ((bytes_data[6] & 0x0F) << 48) | (bytes_data[5] << 40) | (bytes_data[4] << 32) | \
                   (bytes_data[3] << 24) | (bytes_data[2] << 16) | (bytes_data[1] << 8) | bytes_data[0]
        
        # 特殊情况处理: 指数为0表示值为0, 指数为最大值(2047)且尾数不为0表示NaN或无穷大
        if exponent == 0:
            return 0.0
        elif exponent == 0x7FF:
            return float('inf') if mantissa == 0 else float('nan')
        
        # 根据IEEE 754标准(Shapefile的官方文档要求)计算双精度浮点数
        return sign * (1 + mantissa / (1 << 52)) * (2 ** (exponent - 1023))

## 读取Shapefile文件方法
    '''
    4.read_shapefile方法
    含义: 
    从Shapefile文件中读取记录, 并解析出点坐标。
    原理: 
    Shapefile文件由一个固定长度的文件头(100字节)和多个记录组成。每个记录有一个固定长度的记录头(8字节), 
    记录内容的长度根据记录的类型和具体数据变化。点类型的记录包含形状类型(4字节)以及后续的坐标数据(X和Y, 各8字节)。
    作用机理: 
    首先跳过文件头(100字节), 然后逐条读取记录头(8字节), 解析出记录号和记录长度(大端模式)。根据解析出的记录长度和形状类型, 
    确定如何处理记录内容: 如果形状类型为点类型(shape_type==1), 调用read_double方法解析并存储X和Y坐标; 如果不是点类型, 则跳过该记录内容, 直到文件末尾。
    '''
    def read_shapefile(self):
        # 打开Shapefile文件
        with open(self.shp_file_path, 'rb') as f:
            # 跳过主文件头部分, 主文件头长度为100字节(Shapefile文件的规范)
            self.read_bytes(f, 100)

            while True:
                # 读取记录头部(8字节, 大端模式)
                record_header = self.read_bytes(f, 8)
                if len(record_header) < 8:
                    print("数据读取完毕")
                    break  # 文件已读完或不完整
                # 解析记录号(4字节)和内容长度(4字节), 采用大端模式
                record_number = (record_header[0] << 24) | (record_header[1] << 16) | (record_header[2] << 8) | record_header[3]
                content_length = (record_header[4] << 24) | (record_header[5] << 16) | (record_header[6] << 8) | record_header[7]
                print(f"记录号: {record_number}, 内容长度: {content_length}")
                # 读取形状类型(4字节, 小端模式)
                shape_type_bytes = self.read_bytes(f, 4)
                shape_type = shape_type_bytes[0] | (shape_type_bytes[1] << 8) | (shape_type_bytes[2] << 16) | (shape_type_bytes[3] << 24)
                print(f"形状类型: {shape_type}")
                if shape_type == 1:  # 如果形状类型为1, 表示这是一个点类型记录
                    x = self.read_double(f)  # 读取X坐标
                    y = self.read_double(f)  # 读取Y坐标
                    print(f"读取到点: ({x}, {y})")
                    self.shapes.append({'type': 'Point', 'coordinates': [x, y]})
                else:
                    self.read_bytes(f, content_length * 2 - 4)# 如果不是点类型(例如线或面), 跳过该记录的剩余内容

## 将点数据转换为GeoJSON格式方法
    '''
    5.to_geojson方法
    含义: 
    将解析出来的点数据转换为GeoJSON格式并输出为文件。
    原理: 
    GeoJSON是一种基于JSON的标准格式, 用于表示地理要素。一个GeoJSON文件通常由一个FeatureCollection对象组成, 
    包含多个Feature, 每个Feature代表一个地理实体。在Shapefile中, 每个点数据可以映射到一个GeoJSON的Feature对象。
    作用机理: 
    方法先构建一个GeoJSON字符串的基础结构(FeatureCollection), 遍历self.shapes列表, 
    将每个点数据转换为GeoJSON格式的Feature, 包括点的类型和坐标信息。将所有Feature拼接在一起, 最终形成完整的GeoJSON结构。
    最后将生成的GeoJSON字符串写入到指定的输出文件中。
    '''
    def to_geojson(self, output_file):
        # 构建GeoJSON的基础结构
        geojson_str = '{\n  "type": "FeatureCollection",\n  "features": [\n'

        for i, shape in enumerate(self.shapes):
            # 构建每个点的GeoJSON Feature
            feature_str = (
                '    {\n'
                '      "type": "Feature",\n'
                '      "geometry": {\n'
                '        "type": "' + shape['type'] + '",\n'
                '        "coordinates": [' + str(shape['coordinates'][0]) + ', ' + str(shape['coordinates'][1]) + ']\n'
                '      },\n'
                '      "properties": {}\n'
                '    }'
            )
            geojson_str += feature_str
            if i < len(self.shapes) - 1:
                geojson_str += ',\n'  # 如果不是最后一个Feature, 添加逗号和换行符

        geojson_str += '\n  ]\n}'

        # 将格式化后的GeoJSON字符串写入文件
        with open(output_file, 'w') as f:
            f.write(geojson_str)

        print(f"GeoJSON数据成功写入 {output_file}")


## 主程序
# 输入.shp文件路径, 输出.geojson文件路径
shp_file_path = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\shape\\CN_county\\CN_county.shp"  # 输入.shp文件路径
output_geojson = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\path_output\\CN_county.geojson"  # 输出.geojson文件路径
# 创建ShapefileReader对象并读取Shapefile文件
shapefile_reader = ShapefileReader(shp_file_path)  # 创建ShapefileReader对象
shapefile_reader.read_shapefile()  # 读取Shapefile中的点数据
shapefile_reader.to_geojson(output_geojson)  # 将数据转换为GeoJSON并输出到文件