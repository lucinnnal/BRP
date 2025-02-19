import os
import json
import random
from typing import List, Dict

def get_video_files(video_dir: str) -> List[str]:
    """비디오 파일 목록을 가져옵니다."""
    return [f for f in os.listdir(video_dir) if f.endswith('.flv')]

def create_data_entry(filename: str) -> Dict:
    """개별 비디오 파일에 대한 데이터 엔트리를 생성합니다."""
    # 파일 확장자 제거
    video_id = filename.replace('.flv', '')
    
    # wav 파일 경로 생성
    wav_path = os.path.join("/Users/kipyokim/Desktop/cav-mae/src/preprocess/audio", f"{video_id}.wav")
    
    # video_path 설정
    video_path = "/Users/kipyokim/Desktop/cav-mae/src/preprocess/frames/"
    
    # labels 추출 (파일명의 마지막 숫자)
    labels = filename.split('_')[-1].replace('.flv', '')
    
    return {
        "video_id": video_id,
        "wav": wav_path,
        "video_path": video_path,
        "labels": labels
    }

def create_dataset_splits(video_dir: str, train_ratio: float = 0.8):
    """데이터셋을 train과 test로 나누고 JSON 파일을 생성합니다."""
    # 비디오 파일 목록 가져오기
    video_files = get_video_files(video_dir)
    
    # 파일 무작위 섞기
    random.shuffle(video_files)
    
    # train/test 분할
    split_idx = int(len(video_files) * train_ratio)
    train_files = video_files[:split_idx]
    test_files = video_files[split_idx:]
    
    # train과 test 데이터 생성
    train_data = {"data": [create_data_entry(f) for f in train_files]}
    test_data = {"data": [create_data_entry(f) for f in test_files]}
    
    train_json_path = "./datafiles/train_json.json"
    test_json_path = "./datafiles/test_json.json"

    # JSON 파일 저장
    with open(train_json_path, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    
    with open(test_json_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"총 {len(video_files)}개 파일 중:")
    print(f"- Train 데이터: {len(train_files)}개")
    print(f"- Test 데이터: {len(test_files)}개")

# 사용 예시
if __name__ == "__main__":
    video_directory = "./video/"  
    create_dataset_splits(video_directory)