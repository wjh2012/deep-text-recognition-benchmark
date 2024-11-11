import msgspec
import os
import shutil

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

def generate_labels(sample_json_path: str, output_txt_path: str, image_path: str, output_image_path: str):
    # 디렉토리가 없으면 생성
    output_dir = os.path.dirname(output_txt_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(output_image_path):
        os.makedirs(output_image_path)

    # 복잡한 중첩 JSON 데이터 구조 디코딩 및 상위 항목 추출
    with open(sample_json_path, "rb") as f:
        decoder = msgspec.json.Decoder(Data)
        data = decoder.decode(f.read())

        images = data.images
        annotations = data.annotations
        data_len = len(images)

    # 라벨에 존재하는 이미지 파일 이름 수집
    valid_image_files = {image.file_name for image in images}

    # image_path에 있는 파일 중 라벨에 존재하는 파일을 output_image_path로 이동
    for img_file in os.listdir(image_path):
        if img_file in valid_image_files:
            src_file_path = os.path.join(image_path, img_file)
            dst_file_path = os.path.join(output_image_path, img_file)
            shutil.move(src_file_path, dst_file_path)
            print(f"이동됨: {src_file_path} -> {dst_file_path}")

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
    print(f"이미지 파일들이 '{output_image_path}' 경로로 성공적으로 이동되었습니다.")

# 예제 호출
image_path = r"D:\ml\한국어글자체이미지-샘플\source\01_handwriting_sentence_images\1_sentence"
label_json_path = r"D:\ml\한국어글자체이미지-샘플\label\handwriting_data_info_clean.json"
output_txt_path = "wjh_data/hangul_data/gt.txt"
output_image_path = "wjh_data/hangul_data/images"
generate_labels(label_json_path, output_txt_path, image_path, output_image_path)
