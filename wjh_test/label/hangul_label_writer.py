import msgspec
import os

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

def generate_labels(sample_json_path: str, output_txt_path: str):
    # 디렉토리가 없으면 생성
    output_dir = os.path.dirname(output_txt_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 복잡한 중첩 JSON 데이터 구조 디코딩 및 상위 항목 추출
    with open(sample_json_path, "rb") as f:
        # 데이터 모델(Data)을 기반으로 JSON 디코딩
        decoder = msgspec.json.Decoder(Data)
        data = decoder.decode(f.read())

        images = data.images
        annotations = data.annotations
        data_len = len(images)

    # 결과를 텍스트 파일로 작성
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        for i in range(data_len):
            image = images[i]
            annotation = annotations[i]

            if image.id == annotation.image_id:
                file_name = image.file_name
                label = f"images/{file_name}\t{annotation.text}\n"
                txt_file.write(label)

    print(f"텍스트 파일이 '{output_txt_path}' 경로에 성공적으로 작성되었습니다.")

# 예제 호출
image_path = r"C:\Users\WONJANGHO\Desktop\hangul_sample\source\01_handwriting_sentence_images\1_sentence"
label_json_path = r"C:\Users\WONJANGHO\Desktop\hangul_sample\label\handwriting_data_info_clean.json"
output_txt_path = r"C:\Users\WONJANGHO\Desktop\hangul_sample_result\gt.txt"
output_image_path = r"C:\Users\WONJANGHO\Desktop\hangul_sample_result\images"
generate_labels(label_json_path, output_txt_path)
