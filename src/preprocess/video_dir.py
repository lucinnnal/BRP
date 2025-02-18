import os

# 비디오 파일들이 위치한 디렉토리
video_dir = './video/'

# 비디오 파일 목록 얻기 (.flv 파일만 필터링)
file_list = [f for f in os.listdir(video_dir) if f.endswith('.flv')]

# 경로를 포함한 파일 이름 생성
file_paths = [os.path.join(video_dir, file_name) for file_name in file_list]

# CSV 파일로 저장 (컬럼 없이)
output_file = './video_extract_list.csv'
with open(output_file, 'w') as f:
    for path in file_paths:
        f.write(f"{path}\n")

print(f"CSV 파일이 {output_file}로 저장되었습니다.")
