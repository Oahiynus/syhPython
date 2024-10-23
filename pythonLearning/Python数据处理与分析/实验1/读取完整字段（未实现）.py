class ShapefileReader:
    def __init__(self, shp_file_path, dbf_file_path):
        self.shp_file_path = shp_file_path  # Shapefile文件路径
        self.dbf_file_path = dbf_file_path  # DBF文件路径（包含属性数据）
        self.shapes = []  # 用于存储从Shapefile中读取的点信息
        self.fields = []  # 存储字段信息
        self.records = []  # 存储每条记录的数据

    def read_bytes(self, f, num_bytes):
        # 从文件中读取指定数量的字节，并返回这些字节作为字节对象
        return f.read(num_bytes)

    def read_double(self, f):
        """
        解析Shapefile中存储的双精度浮点数（64位）。Shapefile中的双精度浮点数以小端字节顺序存储。
        """
        bytes_data = self.read_bytes(f, 8)  # 读取8字节的数据
        # 手动解析小端存储的双精度浮点数
        sign = -1 if (bytes_data[7] & 0x80) else 1
        exponent = ((bytes_data[7] & 0x7F) << 4) | (bytes_data[6] >> 4)
        mantissa = ((bytes_data[6] & 0x0F) << 48) | (bytes_data[5] << 40) | (bytes_data[4] << 32) | \
                   (bytes_data[3] << 24) | (bytes_data[2] << 16) | (bytes_data[1] << 8) | bytes_data[0]
        if exponent == 0:
            return 0.0
        elif exponent == 0x7FF:
            return float('inf') if mantissa == 0 else float('nan')
        return sign * (1 + mantissa / (1 << 52)) * (2 ** (exponent - 1023))

    def read_dbf(self):
        """
        解析DBF文件的字段和记录数据。
        """
        with open(self.dbf_file_path, 'rb') as f:
            # 读取文件头
            header = self.read_bytes(f, 32)
            num_records = header[4] | (header[5] << 8) | (header[6] << 16) | (header[7] << 24)
            header_length = header[8] | (header[9] << 8)
            record_length = header[10] | (header[11] << 8)

            # 读取字段描述
            f.seek(32)  # 字段描述从文件头后的第32字节开始
            while True:
                field_desc = self.read_bytes(f, 32)
                if field_desc[0] == 0x0D:  # 字段描述区的结束标志
                    break
                field_name = field_desc[:11].decode('ascii').strip('\x00')
                field_type = chr(field_desc[11])
                field_length = field_desc[16]
                self.fields.append((field_name, field_type, field_length))

            # 读取每条记录
            for _ in range(num_records):
                record = {}
                record_data = self.read_bytes(f, record_length)
                offset = 1  # 跳过第一个字节（删除标记）
                for field_name, field_type, field_length in self.fields:
                    field_value = record_data[offset:offset + field_length].decode('ascii').strip()
                    record[field_name] = field_value
                    offset += field_length
                self.records.append(record)

    def read_shapefile(self):
        """
        读取Shapefile文件，解析每个记录的点坐标和属性。
        """
        self.read_dbf()  # 首先读取DBF文件中的属性数据

        with open(self.shp_file_path, 'rb') as f:
            # 跳过文件头部分，文件头长度为100字节（Shapefile文件的规范）
            self.read_bytes(f, 100)

            record_index = 0
            while True:
                # 读取记录头部（8字节，大端模式）
                record_header = self.read_bytes(f, 8)
                if len(record_header) < 8:
                    print("读取完毕或文件不完整")
                    break  # 文件已读完或不完整

                # 解析记录号（4字节）和内容长度（4字节），采用大端模式
                record_number = (record_header[0] << 24) | (record_header[1] << 16) | (record_header[2] << 8) | record_header[3]
                content_length = (record_header[4] << 24) | (record_header[5] << 16) | (record_header[6] << 8) | record_header[7]
                print(f"记录号: {record_number}, 内容长度: {content_length}")

                # 读取形状类型（4字节，小端模式）
                shape_type_bytes = self.read_bytes(f, 4)
                shape_type = shape_type_bytes[0] | (shape_type_bytes[1] << 8) | (shape_type_bytes[2] << 16) | (shape_type_bytes[3] << 24)
                print(f"形状类型: {shape_type}")

                if shape_type == 1:  # 如果形状类型为1，表示这是一个点类型记录
                    x = self.read_double(f)  # 读取X坐标
                    y = self.read_double(f)  # 读取Y坐标
                    properties = self.records[record_index] if record_index < len(self.records) else {}
                    print(f"读取到点: ({x}, {y})")
                    self.shapes.append({
                        'type': 'Point',
                        'coordinates': [x, y],
                        'properties': properties
                    })
                    record_index += 1
                else:
                    # 如果不是点类型（例如线或面），跳过该记录的剩余内容
                    self.read_bytes(f, content_length * 2 - 4)

    def to_geojson(self, output_file):
        """
        将读取到的点数据转换为格式化的GeoJSON格式，并输出到指定的文件中。
        """
        geojson_str = '{\n  "type": "FeatureCollection",\n  "features": [\n'

        for i, shape in enumerate(self.shapes):
            feature_str = (
                '    {\n'
                '      "type": "Feature",\n'
                '      "geometry": {\n'
                '        "type": "' + shape['type'] + '",\n'
                '        "coordinates": [' + str(shape['coordinates'][0]) + ', ' + str(shape['coordinates'][1]) + ']\n'
                '      },\n'
                '      "properties": ' + str(shape['properties']) + '\n'
                '    }'
            )
            geojson_str += feature_str
            if i < len(self.shapes) - 1:
                geojson_str += ',\n'

        geojson_str += '\n  ]\n}'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(geojson_str)

        print(f"GeoJSON数据成功写入 {output_file}")

# 示例用法
shp_file_path = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\shape\\CN_city\\CN_city.shp"
dbf_file_path = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\shape\\CN_city\\CN_city.dbf"
output_geojson = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\path_output\\CN_city111.geojson"

shapefile_reader = ShapefileReader(shp_file_path, dbf_file_path)
shapefile_reader.read_shapefile()
shapefile_reader.to_geojson(output_geojson)
