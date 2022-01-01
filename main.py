import os
import shutil
import random
import pandas as pd

# dictionary 세팅
acc_dic = {}
acc_back_dic = {}
acc_eye_dic = {}
bg_dic = {}
body_dic = {}
buri_dic = {}
eye_dic = {}
hair_dic = {}
head_dic = {}

FOLDER_PATH = "C:/Users/starm/Desktop/bms"
GROUP_FOLDER_PATH = "C:/dev/workspace/bms-project/group/"

FILENAME_EXTENSION = ".png"

#  후보 pool
pool = []

# 엑셀 저장용 데이터
acc = []
acc_back = []
acc_eye = []
bg = []
body = []
buri = []
eye = []
hair = []
head = []


# 붙여넣을 대상 폴더 생성
def create_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError:
        print("Error")


# 폴더 내 파일들 딕셔너리로 생성
def create_dictionary():
    group_list = os.listdir(GROUP_FOLDER_PATH)

    for group in group_list:

        path = GROUP_FOLDER_PATH + group
        file_list = os.listdir(path)

        dic = {}

        if group == 'Acc':
            dic = acc_dic
        elif group == 'Acc Back':
            dic = acc_back_dic
        elif group == 'Acc Eye':
            dic = acc_eye_dic
        elif group == 'BG':
            dic = bg_dic
        elif group == 'Body':
            dic = body_dic
        elif group == 'Buri':
            dic = buri_dic
        elif group == 'Eye':
            dic = eye_dic
        elif group == 'Hair':
            dic = hair_dic
        elif group == 'Head':
            dic = head_dic

        for file in file_list:
            file_set_list = file.split("_")
            dic[file_set_list[0] + "_" + file_set_list[1]] = int(file_set_list[2].replace(FILENAME_EXTENSION, ''))


# 조합 생성
def create_combination():

    groups = [acc_dic, acc_back_dic, acc_eye_dic, bg_dic, body_dic, buri_dic, eye_dic, hair_dic, head_dic]

    combination = {}

    # 그룹마다 하나씩 뽑아야 함
    for group in groups:

        index = random.randint(1, len(group.keys())) - 1

        # 부분별로 조합 생성
        combination[list(group)[index].split('_')[0]] = list(group)[index]

    if combination not in pool:
        pool.append(combination)

        # 엑셀 목록 생성
        acc.append(combination['Acc'])
        acc_back.append(combination['Acc Back'])
        acc_eye.append(combination['Acc Eye'])
        bg.append(combination['BG'])
        body.append(combination['Body'])
        buri.append(combination['Buri'])
        eye.append(combination['Eye'])
        hair.append(combination['Hair'])
        head.append(combination['Head'])
        
        # 숫자 감산 or dict에서 삭제
        selected_parts = combination.values()

        for part in selected_parts:

            dic = {}

            part_name = part.split("_")[0]

            if part_name == 'Acc':
                dic = acc_dic
            elif part_name == 'Acc Back':
                dic = acc_back_dic
            elif part_name == 'Acc Eye':
                dic = acc_eye_dic
            elif part_name == 'BG':
                dic = bg_dic
            elif part_name == 'Body':
                dic = body_dic
            elif part_name == 'Buri':
                dic = buri_dic
            elif part_name == 'Eye':
                dic = eye_dic
            elif part_name == 'Hair':
                dic = hair_dic
            elif part_name == 'Head':
                dic = head_dic

            existing_count = dic[part]

            if existing_count - 1 == 0:
                del dic[part]
            else:
                dic[part] = existing_count - 1


def save_to_excel():

    raw_data = {'acc': acc, 'acc_back': acc_back, 'acc_eye': acc_eye, 'bg': bg, 'body': body, 'buri': buri, 'eye': eye, 'hair': hair, 'head': head}
    excel_data = pd.DataFrame(raw_data)

    excel_data.to_excel(FOLDER_PATH + "/combination_list.xlsx")


def file_copy():

    for index, combination in enumerate(pool):
        # 붙여넣을 폴더 생성
        to_path = FOLDER_PATH+"/"+str(index + 1)
        os.makedirs(to_path)

        for key, value in combination.items():
            _from = "./copy_items/" + key + "/" + value + FILENAME_EXTENSION
            shutil.copyfile(_from, to_path + "/" + value + FILENAME_EXTENSION)


def name_change():
    group_list = os.listdir(GROUP_FOLDER_PATH)

    for group in group_list:
        path = GROUP_FOLDER_PATH + group
        file_list = os.listdir(path)

        for file in file_list:
            change_name = file.replace(" ", "").replace("_","")

            src = path + "/" + file
            dst = path + "/" + change_name

            print(src)
            print(dst)

            os.rename(src, dst)


def multiple_count_number():

    group_list = os.listdir(GROUP_FOLDER_PATH)

    for group in group_list:
        path = GROUP_FOLDER_PATH + group
        file_list = os.listdir(path)

        for file in file_list:
            file_name_list = file.split('_')
            extend_number = int(file_name_list[2].replace(FILENAME_EXTENSION, '')) * 2
            change_name = file_name_list[0] + "_" + file_name_list[1] + "_" + str(extend_number) + ".png"

            src = path + "/" + file
            dst = path + "/" + change_name

            os.rename(src, dst)


# 붙여넣을 대상 폴더 생성
# create_folder(FOLDER_PATH)

# 폴더 내 파일들 딕셔너리로 생성
create_dictionary()

# 조합 생성
# create_combination()

# pool 갯수가 10000개가 될 때 까지
while len(pool) < 10000:
    # 조합 생성
    create_combination()

# print(pool)
print(acc_dic)
print(acc_back_dic)
print(acc_eye_dic)
print(bg_dic)
print(body_dic)
print(buri_dic)
print(eye_dic)
print(hair_dic)
print(head_dic)


# print(pool)
# 목록 엑셀 다운로드
save_to_excel()

# 파일 복사
file_copy()

# 이름 변경 작업
# name_change()

# 횟수 곱셈
# multiple_count_number()
