import struct
import json

class ShapefileReader:
    def __init__(self, shp_file_path):
        self.shp_file_path = shp_file_path
        self.shapes = []

    def read_shapefile(self):
        with open(self.shp_file_path, 'rb') as f:
            # 读取100字节的文件头
            header = f.read(100)
            # 跳过文件头部分，定位到主内容
            f.seek(100)

            while True:
                record_header = f.read(8)
                if len(record_header) < 8:
                    break

                # 读取记录头部信息（记录号和内容长度）
                record_number, content_length = struct.unpack('>2i', record_header)

                # 根据内容长度读取相应的内容（16位字为单位，乘2转为字节数）
                shape_type = struct.unpack('<i', f.read(4))[0]
                
                if shape_type == 1:  # 点类型
                    x, y = struct.unpack('<2d', f.read(16))
                    self.shapes.append({'type': 'Point', 'coordinates': [x, y]})
                else:
                    f.read(content_length * 2 - 4)  # 如果不是点类型，跳过该记录

    def to_geojson(self, output_file):
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        for shape in self.shapes:
            feature = {
                "type": "Feature",
                "geometry": shape,
                "properties": {}
            }
            geojson["features"].append(feature)

        # 将GeoJSON写入文件
        with open(output_file, 'w') as f:
            json.dump(geojson, f, indent=4)

        print(f"GeoJSON数据成功写入 {output_file}")

# 示例用法
shp_file_path = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\shape\\drinking.shp"  # 替换为实际的.shp文件路径
output_geojson = "E:\\YNU\\5\\PythonDataProcessingAnalysis\\作业1\\data\\output.geojson"

shapefile_reader = ShapefileReader(shp_file_path)
shapefile_reader.read_shapefile()
shapefile_reader.to_geojson(output_geojson)
