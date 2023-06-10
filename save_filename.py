import os

def list_files(directory, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            print(len(files))
            for file in files:
                f.write(file[:-4] + '\n')
# 遍历的目标文件夹
folder_path = '/media/multiai5/poseidon3/Jiuqing/Object365/VOC_XML/train'
output_file = '/media/multiai5/poseidon3/Jiuqing/Object365/train.txt'
list_files(folder_path, output_file)
print('Filename is already saved to ', output_file)
folder_path = '/media/multiai5/poseidon3/Jiuqing/Object365/VOC_XML/val'
output_file = '/media/multiai5/poseidon3/Jiuqing/Object365/val.txt'
list_files(folder_path, output_file)
print('Filename is already saved to ', output_file)