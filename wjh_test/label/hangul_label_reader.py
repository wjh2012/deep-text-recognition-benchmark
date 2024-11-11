import msgspec

class ImageInfo(msgspec.Struct):
    id: str
    width: int
    height: int
    file_name: str

class LabelInfo(msgspec.Struct):
    id: str
    image_id: str
    text: str

class Data(msgspec.Struct):
    images: list[ImageInfo]
    annotations: list[LabelInfo]

# 파일 경로와 읽고자 하는 상위 데이터 개수 설정
sample_json_path = r"C:\Users\WONJANGHO\Desktop\hangul_sample\label\handwriting_data_info_clean.json"
num_records = 10

# 복잡한 중첩 JSON 데이터 구조 디코딩 및 상위 항목 추출
with open(sample_json_path, "rb") as f:
    # 데이터 모델(Data)을 기반으로 JSON 디코딩
    decoder = msgspec.json.Decoder(Data)
    data = decoder.decode(f.read())

    # images와 annotations에서 상위 num_records 개 데이터 추출
    top_images = data.images[:num_records]
    top_annotations = data.annotations[:num_records]

    # 필요한 정보만 포함된 결과 출력
    extracted_data = {
        "images": [
            {
                "id": img.id,
                "width": img.width,
                "height": img.height,
                "file_name": img.file_name
            }
            for img in top_images
        ],
        "annotations": [
            {
                "id": ann.id,
                "image_id": ann.image_id,
                "text": ann.text
            }
            for ann in top_annotations
        ]
    }

print(extracted_data)
