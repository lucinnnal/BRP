import pandas as pd
import os

# 기존 CSV 파일 읽기 (파일 이름만 있는 CSV)
input_file = './original_csv.csv'
output_file = './datafiles/labels.csv'

# 파일 리스트 불러오기
file_list = pd.read_csv(input_file, header=None, dtype=str).squeeze().tolist()

# 저장할 데이터 리스트
data = []

# 파일 이름에서 필요한 정보 추출
for idx, file_name in enumerate(file_list):
    # 확장자 제외한 파일 이름에서 video_id 추출
    file_base = os.path.splitext(file_name)[0]  # 확장자 제거한 파일 이름
    stress_score = file_base.split('_')[-1]    # 파일 이름의 마지막 부분이 스트레스 점수
    
    # video_id는 확장자 제외한 전체 이름에서 스트레스 점수까지 포함
    video_id = file_base  # 스트레스 점수까지 포함한 전체 이름

    # 결과를 리스트에 추가 (Index는 0부터 시작)
    data.append([idx, video_id, stress_score])

# DataFrame으로 변환하여 CSV로 저장
df = pd.DataFrame(data, columns=['Index', 'Video_ID', 'Stress_Score'])
df.to_csv(output_file, index=False)

print(f"CSV 파일이 {output_file}로 저장되었습니다.")