# modifies the base path for google drive
import json
import os

def update_json_paths(json_file_path, new_base_path):
    """
    JSON 파일의 경로를 업데이트하는 함수
    
    Args:
        json_file_path (str): 수정할 JSON 파일의 경로
        new_base_path (str): 새로운 기본 경로
    """
    try:
        # JSON 파일 읽기
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 각 항목의 경로 업데이트
        for item in data['data']:
            # 오디오 파일 경로 업데이트
            audio_filename = os.path.basename(item['wav'])
            item['wav'] = os.path.join(new_base_path, 'audio', audio_filename)
            
            # 비디오 경로 업데이트
            item['video_path'] = os.path.join(new_base_path, 'frames/')
        
        # 원본 파일에 수정된 내용 저장
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            
        print(f"파일이 성공적으로 업데이트되었습니다: {json_file_path}")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

def main():
    # 사용자로부터 입력 받기
    json_file_path = "./datafiles/test_json.json"
    new_base_path = "/content/data"
    
    # 경로 업데이트 함수 호출
    update_json_paths(json_file_path, new_base_path)

if __name__ == "__main__":
    main()