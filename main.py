# 作者：虚字潜心
# C语言工程生成器，但是也支持生成其他的东西，只不过对C语言做了特别处理
# 虽然重构了，但是也没完全重构——如构，反正你用这个，也不用捏着鼻子看

import os
import shutil

instructionList = ["yl", "cd", "crt", "cpy", "del", "help"]
keyWord = ["-f", "-inc", "var", "define"]
programFolderPath = ''
filenameExtension = ''
fileCrtMode = 0
includeHead = "#include "
fileHeadList = []
variableList = {}


def instruction_yl(instruction):
    global variableList
    temp = []

    if os.path.isfile(instruction[1]):
        program_make_file_name, program_make_file_extension = os.path.splitext(instruction[1])
        if program_make_file_extension == ".cpm":
            program_make_file = open(instruction[1], "r", encoding="UTF-8")
            for line in program_make_file:
                line = line.strip()

                if not line:
                    continue
                elif (line[0] == '#') or (line[0] == ';'):
                    continue
                elif line.find("#") != -1:
                    line = line[:line.find("#")]
                elif line.find(";") != -1:
                    line = line[:line.find(";")]
                else:
                    pass

                if line[-1] == '\\':
                    line = line[:(len(line) - 1)]
                    temp = line.split()
                    continue
                else:
                    instruction = line.split()

                if not temp:
                    pass
                else:
                    instruction = temp + instruction
                    instruction = list(filter(None, instruction))
                    temp = []

                if instruction[0] == "var" and instruction[2] == "=":
                    variableList[instruction[1]] = instruction[3].replace("_", " ").replace("\"", " ").strip()
                    continue
                elif instruction[0] == "define":
                    variableList[instruction[1]] = instruction[2].replace("_", " ")
                    continue
                elif instruction[0] != "var" and instruction[1] == "=":
                    if variableList.get(instruction[0]):
                        variableList[instruction[0]] = instruction[2].replace("_", " ").replace("\"", " ").strip()
                        continue
                    else:
                        continue
                else:
                    pass

                for index, token in enumerate(instruction):
                    if token.find("$") != -1:
                        variable_temp = list(filter(None, token.split("$")))
                        if token.find("$") == 0:
                            variable_name = variable_temp[0]
                            variable_index = 0
                        elif token.find("$") == len(token):
                            variable_name = variable_temp[2]
                            variable_index = 2
                        else:
                            variable_name = variable_temp[1]
                            variable_index = 1
                        if variableList.get(variable_name):
                            variable_temp[variable_index] = variableList.get(variable_name)
                            instruction[index] = "".join(variable_temp)
                print(instruction)
                if instruction[0] == instructionList[0]:
                    print("E:文件禁止使用yl")
                elif instruction[0] == instructionList[1]:
                    instruction_cd(instruction)
                elif instruction[0] == instructionList[2]:
                    instruction_crt(instruction)
                elif instruction[0] == instructionList[3]:
                    instruction_cpy(instruction)
                elif instruction[0] == instructionList[4]:
                    instruction_del(instruction)
                elif instruction[0] == instructionList[5]:
                    print("W:文件内help指令无效")
                else:
                    pass
            program_make_file.close()
            print("创建完成")
        else:
            print("E:path is not file")


def instruction_cd(instruction):
    global programFolderPath

    programFolderPath = instruction[1]
    if os.path.isdir(programFolderPath):
        os.chdir(programFolderPath)
        print("open >> " + programFolderPath)
    else:
        print("E:path error or Folder not found")


def instruction_crt(instruction):
    global programFolderPath
    global fileCrtMode
    global filenameExtension
    global fileHeadList

    if "-f" in instruction:
        if instruction.index("-f") == 2:
            instruction.remove("-f")
            folder_path = instruction[1]
        else:
            folder_path = ''
    else:
        folder_path = instruction[1]

    if not os.path.exists(folder_path) and not folder_path == '':
        os.makedirs(folder_path)
        if programFolderPath == '':
            programFolderPath = folder_path
            os.chdir(programFolderPath)
            print(os.getcwd())

    elif len(instruction) < 2 and os.path.exists(folder_path):
        print("E:path error or already exists")

    if len(instruction) > 2:
        fileCrtMode = 0
        if folder_path != '':
            os.chdir(folder_path)

        if "-inc" in instruction:
            is_have_inc = True
            fileHeadList = instruction[(instruction.index("-inc") + 1):]
            instruction = instruction[:instruction.index("-inc")]
        else:
            is_have_inc = False

        for fileName in instruction[2:len(instruction)]:
            if fileName[0] == "*":
                filenameExtension = fileName.replace("*", ".")
                fileCrtMode = 1
                continue

            if (fileName + filenameExtension == "main.c") or (fileName == "main.c"):
                if not is_have_inc:
                    chose = input("检测到main.c文件，是否需要个性化生成[Y/N]")
                else:
                    chose = "Y"
                if chose == "Y":
                    if not is_have_inc:
                        fileHeadList = input("输入库文件:").split()
                    else:
                        pass
                    file = open(fileName + filenameExtension, "w", encoding='utf-8')
                    for fileHead in fileHeadList:
                        file.writelines(includeHead + fileHead + "\n")

                    file.writelines("\n")

                    file.writelines("int main()\n")
                    file.writelines("{\n")
                    file.writelines("\treturn 0;\n")
                    file.writelines("}\n")

                    file.close()
                    continue

            if fileCrtMode == 1 and not os.path.exists(fileName + filenameExtension):
                if filenameExtension == ".c":
                    file = open(fileName + filenameExtension, "w", encoding='utf-8')
                    file.writelines(includeHead + fileName + ".h")
                    file.close()

                elif filenameExtension == ".h":
                    file = open(fileName + filenameExtension, "w", encoding='utf-8')
                    file.writelines("#ifndef __" + (fileName + filenameExtension).replace(".", "_").upper() + "__\n")
                    file.writelines("#define __" + (fileName + filenameExtension).replace(".", "_").upper() + "__\n\n")
                    file.writelines("#ifdef __cplusplus\nextern \"C\"{\n#endif\n\n")
                    file.writelines("#ifdef __cplusplus\n}\n#endif\n")
                    file.writelines(
                        "#endif /* __" + (fileName + filenameExtension).replace(".", "_").upper() + "__ */\n")

                else:
                    open(fileName + filenameExtension, "w", encoding='utf-8').close()

            elif not os.path.exists(fileName):
                open(fileName, "w").close()

        os.chdir(programFolderPath)


def instruction_cpy(instruction):
    if os.path.isdir(instruction[1]) or os.path.isfile(instruction[1]):
        for i in instruction[2:]:
            if i.find("|"):
                if os.path.isdir(i.split("|")[0]):
                    temp_path = i.split("|")[0]
                    main_path = temp_path.replace((temp_path.split("\\")[-1]), '')
                    folder_list = i.split("|")
                    folder_list[0] = temp_path.split("\\")[-1]
                    for f in folder_list:
                        dir_path = main_path + f
                        src_path = instruction[1] + "\\" + f
                        if os.path.exists(src_path):
                            os.makedirs(src_path)
                        try:
                            shutil.copytree(dir_path, src_path)
                        except FileNotFoundError:
                            print("未找到文件夹")
                        except PermissionError:
                            print("权限不足")
                        except FileExistsError:
                            print("目标目录存在同名文件夹")
                elif os.path.isfile(i.split("|")[0]):
                    main_path = os.path.dirname(i.split("|")[0])
                    file_list = i.split("|")
                    file_list[0] = os.path.basename(i.split("|")[0])
                    for j in file_list:
                        dir_path = main_path + "\\" + j
                        try:
                            shutil.copy(dir_path, instruction[1])
                        except FileNotFoundError:
                            print("未找到文件")
                        except PermissionError:
                            print("权限不足")

            else:
                if os.path.isdir(i):
                    try:
                        src_path = instruction[1] + "\\" + i.split("\\")[-1]
                        if os.path.exists(src_path):
                            os.makedirs(src_path)
                        shutil.copytree(src_path, instruction[1])
                    except FileNotFoundError:
                        print("未找到文件夹")
                    except PermissionError:
                        print("权限不足")
                    except FileExistsError:
                        print("目标目录存在同名文件夹")
                elif os.path.isfile(i):
                    try:
                        shutil.copy(i, instruction[1])
                    except FileNotFoundError:
                        print("未找到文件")
                    except PermissionError:
                        print("权限不足")


def instruction_del(instruction):
    file_or_folder_path = instruction[1]
    if os.path.isdir(file_or_folder_path) and not os.listdir(file_or_folder_path):
        os.rmdir(file_or_folder_path)
    elif os.path.isdir(file_or_folder_path) and os.listdir(file_or_folder_path):
        shutil.rmtree(file_or_folder_path)
    elif os.path.isfile(file_or_folder_path):
        os.remove(file_or_folder_path)
    else:
        print("E:path error")


def instruction_help(instruction):
    if len(instruction) > 1:
        if instruction[1] == instructionList[0]:
            print("yl")
        elif instruction[1] == instructionList[1]:
            print("cd")
        elif instruction[1] == instructionList[2]:
            print("crt")
        elif instruction[1] == instructionList[3]:
            print("cpy")
        elif instruction[1] == instructionList[4]:
            print("del")
        elif instruction[1] == instructionList[5]:
            print("help")
    else:
        print("instruction list: yl cd Crt Cpy del help")
        print("help + instruction get more message")


while True:
    globalInstruction = input(">> " + os.getcwd() + " >>").split()
    programFolderPath = os.getcwd()
    if globalInstruction[0] == instructionList[0]:  # yl指令
        instruction_yl(globalInstruction)
    elif globalInstruction[0] == instructionList[1]:  # cd指令
        instruction_cd(globalInstruction)
    elif globalInstruction[0] == instructionList[2]:  # crt指令
        instruction_crt(globalInstruction)
    elif globalInstruction[0] == instructionList[3]:  # cpy指令
        instruction_cpy(globalInstruction)
    elif globalInstruction[0] == instructionList[4]:  # del指令
        instruction_del(globalInstruction)
    elif globalInstruction[0] == instructionList[5]:  # help指令
        instruction_help(globalInstruction)
    elif (globalInstruction[0] == "Q") or (globalInstruction[0] == "q"):
        break
    else:
        print("E:method error! you can use help to study")

    globalInstruction.clear()
