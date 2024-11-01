class ShapefileReader:
    def __init__(self, shp_file_path):
        self.shp_file_path = shp_file_path  # 保存Shapefile文件路径
        self.shapes = []  # 存储从Shapefile中读取的点信息

    def read_bytes(self, f, num_bytes):
        # 从文件中读取指定数量的字节
        return f.read(num_bytes)

    def read_double(self, f):
        # 手动解析双精度浮点数（64位）
        bytes_data = self.read_bytes(f, 8)  # 读取8字节的数据
        # 解析符号位：如果最高位为1，则为负数，否则为正数
        sign = -1 if (bytes_data[0] & 0x80) else 1
        # 解析指数部分（11位）：从第一个字节的低7位和第二个字节的高4位组成
        exponent = ((bytes_data[0] & 0x7F) << 4) | (bytes_data[1] >> 4)
        # 解析尾数部分（52位）：从剩余的字节中提取
        mantissa = ((bytes_data[1] & 0x0F) << 48) | (bytes_data[2] << 40) | (bytes_data[3] << 32) | \
                   (bytes_data[4] << 24) | (bytes_data[5] << 16) | (bytes_data[6] << 8) | bytes_data[7]
        # 特殊情况处理：指数为0表示值为0，指数为最大值（2047）且尾数不为0表示NaN或无穷大
        if exponent == 0:
            return 0.0
        elif exponent == 0x7FF:
            return float('inf') if mantissa == 0 else float('nan')
        # 根据IEEE 754标准计算浮点数值
        return sign * (1 + mantissa / (1 << 52)) * (2 ** (exponent - 1023))

    def read_shapefile(self):
        with open(self.shp_file_path, 'rb') as f:
            # 跳过文件头部分，文件头长度为100字节
            self.read_bytes(f, 100)

            while True:
                # 读取记录头部（8字节）
                record_header = self.read_bytes(f, 8)
                if len(record_header) < 8:
                    print("读取完毕或文件不完整")
                    break  # 文件已读完

                # 手动解析记录号（4字节）和内容长度（4字节）
                record_number = (record_header[0] << 24) | (record_header[1] << 16) | (record_header[2] << 8) | record_header[3]
                content_length = (record_header[4] << 24) | (record_header[5] << 16) | (record_header[6] << 8) | record_header[7]
                print(f"记录号: {record_number}, 内容长度: {content_length}")
                # 读取形状类型（4字节）
                shape_type_bytes = self.read_bytes(f, 4)
                shape_type = (shape_type_bytes[0] << 24) | (shape_type_bytes[1] << 16) | (shape_type_bytes[2] << 8) | shape_type_bytes[3]
                print(f"形状类型: {shape_type}")
                if shape_type == 1:  # 判断是否为点类型（shape_type == 1 表示点）
                    x = self.read_double(f)  # 读取X坐标
                    y = self.read_double(f)  # 读取Y坐标
                    self.shapes.append({'type': 'Point', 'coordinates': [x, y]})
                else:
                    # 如果不是点类型，则跳过该记录的剩余内容
                    self.read_bytes(f, content_length * 2 - 4)

    

    def to_geojson(self, output_file):
        # 手动构建GeoJSON字符串
        geojson_str = '{"type": "FeatureCollection", "features": ['

        for i, shape in enumerate(self.shapes):
            # 构建GeoJSON的Feature部分
            feature_str = '{"type": "Feature", "geometry": {"type": "' + shape['type'] + '", "coordinates": [' + str(shape['coordinates'][0]) + ', ' + str(shape['coordinates'][1]) + ']}, "properties": {}}'
            geojson_str += feature_str
            if i < len(self.shapes) - 1:
                geojson_str += ','  # 如果不是最后一个Feature，添加逗号

        geojson_str += ']}'

        # 将GeoJSON字符串写入文件
        with open(output_file, 'w') as f:
            f.write(geojson_str)

        print(f"GeoJSON数据成功写入 {output_file}")

# 示例用法
shp_file_path = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\shape\\CN_county\\CN_county.shp"  # 替换为实际的.shp文件路径
output_geojson = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\path_output\\noku_no_data.geojson"

shapefile_reader = ShapefileReader(shp_file_path)
shapefile_reader.read_shapefile()
shapefile_reader.to_geojson(output_geojson)
