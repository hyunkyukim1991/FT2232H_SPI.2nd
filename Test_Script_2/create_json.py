#!/usr/bin/env python3
"""
JSON 파일 수동 생성 및 업데이트 도구
"""

import json

def create_sample_json_data():
    """샘플 JSON 데이터 생성"""
    sample_data = {
        "registers": [
            {
                "address": "0x00",
                "description": "Reset Register",
                "fields": [
                    {
                        "name": "reset",
                        "bit_range": "15:0",
                        "upper_bit": 15,
                        "lower_bit": 0,
                        "default_value": "0",
                        "meaning": "System Reset Control"
                    }
                ],
                "default_value": 0
            },
            {
                "address": "0x01",
                "description": "Enable Register",
                "fields": [
                    {
                        "name": "EN_VCM",
                        "bit_range": "15:15",
                        "upper_bit": 15,
                        "lower_bit": 15,
                        "default_value": "0",
                        "meaning": "Enable VCM"
                    },
                    {
                        "name": "EN_TX",
                        "bit_range": "14:14",
                        "upper_bit": 14,
                        "lower_bit": 14,
                        "default_value": "0",
                        "meaning": "Enable TX"
                    },
                    {
                        "name": "EN_RX0",
                        "bit_range": "13:13",
                        "upper_bit": 13,
                        "lower_bit": 13,
                        "default_value": "0",
                        "meaning": "Enable RX0"
                    }
                ],
                "default_value": 0
            },
            {
                "address": "0x02",
                "description": "TX PATH_SEL",
                "fields": [
                    {
                        "name": "TX_SEN13_0",
                        "bit_range": "14:0",
                        "upper_bit": 14,
                        "lower_bit": 0,
                        "default_value": "1",
                        "meaning": "TX Path Selection"
                    }
                ],
                "default_value": 1
            },
            {
                "address": "0x03",
                "description": "RX0 PATH SEL",
                "fields": [
                    {
                        "name": "RX0_SEN15_0",
                        "bit_range": "14:0",
                        "upper_bit": 14,
                        "lower_bit": 0,
                        "default_value": "1",
                        "meaning": "RX0 Path Selection"
                    }
                ],
                "default_value": 1
            },
            {
                "address": "0x2B",
                "description": "RO_DATA_5",
                "fields": [
                    {
                        "name": "bit_15",
                        "bit_range": "15:15",
                        "upper_bit": 15,
                        "lower_bit": 15,
                        "default_value": "0",
                        "meaning": "Read Only Bit 15"
                    },
                    {
                        "name": "bit_14",
                        "bit_range": "14:14",
                        "upper_bit": 14,
                        "lower_bit": 14,
                        "default_value": "1",
                        "meaning": "Read Only Bit 14"
                    }
                ],
                "default_value": 16384
            }
        ]
    }
    return sample_data

def save_json_file(file_path, data):
    """JSON 파일 저장"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 파일 저장 완료: {file_path}")
        print(f"📝 저장된 레지스터 수: {len(data['registers'])}")
        return True
    except Exception as e:
        print(f"❌ JSON 파일 저장 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("🔧 JSON 파일 생성 도구")
    
    # 샘플 데이터 생성
    sample_data = create_sample_json_data()
    
    # JSON 파일 저장
    json_file_path = "RSC201_DR_v0_250418 (002)_UM232H_tree.json"
    
    if save_json_file(json_file_path, sample_data):
        print(f"\\n📋 생성된 레지스터 목록:")
        for i, reg in enumerate(sample_data['registers'], 1):
            print(f"  {i}. {reg['address']} - {reg['description']} ({len(reg['fields'])}개 필드)")
    
    print("\\n🎯 Register_Controller.py를 실행하여 GUI에서 확인하세요!")

if __name__ == "__main__":
    main()