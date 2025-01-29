# 作者：虚字潜心
# C语言工程生成器，但是也支持生成其他的东西，只不过对C语言做了特别处理
# 代码以后在重构，反正你用这个，也不用捏着鼻子看
import os
import shutil

instructionList = ["yl", "cd", "crt", "cpy", "del", "help"]
programFolderPath = ''
filenameExtension = ''
fileCrtMode = 0
includeHead = "#include "
fileHeadList = []
variableList = []

while True:
    instruction = input(">> "+os.getcwd()+" >>").split()
    programFolderPath = os.getcwd()
    if instruction[0] == instructionList[0]:        # yl指令
        if os.path.isfile(instruction[1]):
            programMakeFile = open(instruction[1], "r")
            for line in programMakeFile:
                line.find("$")
            programMakeFile.close()
        else:
            print("E:path is not file")

    elif instruction[0] == instructionList[1]:      # cd指令
        programFolderPath = instruction[1]
        if os.path.isdir(programFolderPath):
            os.chdir(programFolderPath)
            print("open >> "+programFolderPath)
        else:
            print("E:path error or Folder not found")

    elif instruction[0] == instructionList[2]:      # crt指令
        if "-f" in instruction:
            if instruction.index("-f") == 2:
                instruction.remove("-f")
                folderPath = instruction[1]
            else:
                folderPath = ''
        else:
            folderPath = instruction[1]

        if not os.path.exists(folderPath) and not folderPath == '':
            os.makedirs(folderPath)
            if programFolderPath == '':
                programFolderPath = folderPath
                os.chdir(programFolderPath)
                print(os.getcwd())

        elif len(instruction) < 2 and os.path.exists(folderPath):
            print("E:path error or already exists")

        if len(instruction) > 2:
            fileCrtMode = 0
            if folderPath != '':
                os.chdir(folderPath)
            for fileName in instruction[2:len(instruction)]:
                if fileName[0] == "*":
                    filenameExtension = fileName.replace("*", ".")
                    fileCrtMode = 1
                    continue

                if (fileName + filenameExtension == "main.c") or (fileName == "main.c"):
                    chose = input("检测到main.c文件，是否需要个性化生成[Y/N]")
                    if chose == "Y":
                        fileHeadList = input("输入库文件:").split()
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
                        file.writelines(includeHead+fileName+".h")
                        file.close()

                    elif filenameExtension == ".h":
                        file = open(fileName + filenameExtension, "w", encoding='utf-8')
                        file.writelines("#ifndef __"+(fileName+filenameExtension).replace(".", "_").upper()+"__\n")
                        file.writelines("#define __"+(fileName+filenameExtension).replace(".", "_").upper()+"__\n\n")
                        file.writelines("#ifdef __cplusplus\nextern \"C\"{\n#endif\n\n")
                        file.writelines("#ifdef __cplusplus\n}\n#endif\n")
                        file.writelines("#endif /* __"+(fileName+filenameExtension).replace(".", "_").upper()+"__ */\n")

                    else:
                        open(fileName + filenameExtension, "w", encoding='utf-8').close()

                elif not os.path.exists(fileName):
                    open(fileName, "w").close()

            os.chdir(programFolderPath)

    elif instruction[0] == instructionList[3]:      # cpy指令
        if os.path.isdir(instruction[1]) or os.path.isfile(instruction[1]):
            for i in instruction[2:]:
                if i.find("|"):
                    if os.path.isdir(i.split("|")[0]):
                        tempPath = i.split("|")[0]
                        mainPath = tempPath.replace((tempPath.split("\\")[-1]), '')
                        folderList = i.split("|")
                        folderList[0] = tempPath.split("\\")[-1]
                        for f in folderList:
                            dirPath = mainPath + f
                            srcPath = instruction[1] + "\\" + f
                            if os.path.exists(srcPath):
                                os.makedirs(srcPath)
                            try:
                                shutil.copytree(dirPath, srcPath)
                            except FileNotFoundError:
                                print("未找到文件夹")
                            except PermissionError:
                                print("权限不足")
                            except FileExistsError:
                                print("目标目录存在同名文件夹")
                    elif os.path.isfile(i.split("|")[0]):
                        mainPath = os.path.dirname(i.split("|")[0])
                        fileList = i.split("|")
                        fileList[0] = os.path.basename(i.split("|")[0])
                        for j in fileList:
                            dirPath = mainPath + "\\" + j
                            try:
                                shutil.copy(dirPath, instruction[1])
                            except FileNotFoundError:
                                print("未找到文件")
                            except PermissionError:
                                print("权限不足")

                else:
                    if os.path.isdir(i):
                        try:
                            srcPath = instruction[1] + "\\" + i.split("\\")[-1]
                            if os.path.exists(srcPath):
                                os.makedirs(srcPath)
                            shutil.copytree(srcPath, instruction[1])
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

    elif instruction[0] == instructionList[4]:      # del指令
        fileOrFolderPath = instruction[1]
        if os.path.isdir(fileOrFolderPath) and not os.listdir(fileOrFolderPath):
            os.rmdir(fileOrFolderPath)
        elif os.path.isdir(fileOrFolderPath) and os.listdir(fileOrFolderPath):
            shutil.rmtree(fileOrFolderPath)
        elif os.path.isfile(fileOrFolderPath):
            os.remove(fileOrFolderPath)
        else:
            print("E:path error")

    elif instruction[0] == instructionList[5]:      # help指令
        print("instruction list: yl cd Crt Cpy del help")
        print("help + instruction get more messega")

    elif (instruction[0] == "Q") or (instruction[0] == "q"):
        break

    else:
        print("E:method error! you can use help to study")

    instruction.clear()
