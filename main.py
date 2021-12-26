import os
import shutil
import random
import pandas as pd

groups = ['Acc', 'Acc Back', 'Acc Eye', 'BG', 'Body', 'Buri', 'Eye', 'Hair', 'Head']
grades_dic = {"a": 0.01, "b": 0.03, "c": 0.06, "d": 0.1, "e": 0.3, "f": 0.5}

FOLDER_PATH = "C:/Users/starm/Desktop/bms"
GROUP_FOLER_PATH = "C:/dev/workspace/bms-project/group/"

FILENAME_EXTENSION = ".png"

#  후보 pool
pool = []

# 선택된 횟수 체크

# 엑셀 저장용 데이터
accessory = []
background = []
body = []
clothes = []
face = []
hair = []
total_probability = []


# 붙여넣을 대상 폴더 생성
def create_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print("Error")

def folder_read():
    file_list = os.listdir(GROUP_FOLER_PATH)

    print(file_list)

# 조합 생성
def create_combination():

    combination = {}

    # 종합 확률
    total_p = 0

    # 그룹마다 하나씩 뽑아야 함
    for group in groups:
        # 가중치 기준 랜덤으로 생성 (소수점 두자리까지)
        pivot = round(random.random(), 2)

        # 가산 변수
        acc = 0



        # 등급 dictionary 순회
        for key, value in grades_dic.items():
            print(key)
            print(value)
            # 각 등급별 가중치 값을 더하고
            acc += value
            # 더해진 값이 기준값보다 크거나 같은지 확인
            if acc >= pivot:
                # 맞다면 조합에 추가
                combination[group] = key
                # 당첨된 등급의 확률 값 종합 확률에 추가
                total_p += value
                break
    
    # 종합 확률도 조합 정보에 추가
    # 종합 확률을 6으로 나누면 최대가 0.5가 되기 때문에 한번 더 나눠준 값으로 세팅
    combination['total_probability'] = round(total_p / (len(groups)/2), 2)

    print(combination)

    # pool에 이미 있지 않은 값이 맞다면
    if combination not in pool:
        # 추가
        pool.append(combination)
        
        # 엑셀 저장을 위해 각 소스별 배열 생성
        accessory.append(combination['accessory'])
        background.append(combination['background'])
        body.append(combination['body'])
        clothes.append(combination['clothes'])
        face.append(combination['face'])
        hair.append(combination['hair'])
        total_probability.append(combination['total_probability'])


def save_to_excel():

    raw_data = {'accessory': accessory, 'background': background, 'body': body, 'clothes': clothes, 'face': face, 'hair': hair, 'total_probability': total_probability}
    excel_data = pd.DataFrame(raw_data)

    excel_data.to_excel(FOLDER_PATH+"/sample.xlsx")


def file_copy():

    for index, combination in enumerate(pool):
        # 붙여넣을 폴더 생성
        to_path = FOLDER_PATH+"/"+str(index)
        os.makedirs(to_path)

        for key, value in combination.items():
            # 종합 확률 정보가 아니면
            if key != 'total_probability':
                _from = "./group/" + key + "/" + key + "_" + value + FILENAME_EXTENSION
                shutil.copyfile(_from, to_path + "/" + key + "_" + value + FILENAME_EXTENSION)



def name_change():
    group_list = os.listdir(GROUP_FOLER_PATH)

    # print("group_list")
    # print(group_list)

    for group in group_list:
        path = GROUP_FOLER_PATH + group
        file_list = os.listdir(path)

        for file in file_list:
            change_name = file.replace(" ", "").replace("_","")

            src = path + "/" + file
            dst = path + "/" + change_name

            print(src)
            print(dst)

            os.rename(src, dst)

        # print("file_list")
        # print(file_list)


def temp_count_set():

    group_list = os.listdir(GROUP_FOLER_PATH)

    for group in group_list:
        path = GROUP_FOLER_PATH + group
        file_list = os.listdir(path)

        for file in file_list:
            change_name = file.replace(".", "_10.")

            src = path + "/" + file
            dst = path + "/" + change_name



            os.rename(src, dst)

        # print("file_list")
        # print(file_list)




# 붙여넣을 대상 폴더 생성
# create_folder(FOLDER_PATH)

# 폴더별 파일들 확인하구 딕셔너리 생성
create_dictionary()

# folder_read()



# pool 갯수가 10000개가 될 때 까지
# while len(pool) < 10000:
    # 조합 생성
    # create_combination()

# 목록 엑셀 다운로드
# save_to_excel()

# 파일 복사
# file_copy()

# 이름 변경 작업
# name_change()

# 감산할 반복 횟수 임시 세팅
# temp_count_set()
