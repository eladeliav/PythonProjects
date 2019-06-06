NEWFILENAME = '/file2'


# -*- coding: utf-8 -*-
def copy_paste(file, folder):
    file_content = None
    with open(file, 'r') as my_text:
        file_content = my_text.read()
    with open(folder + NEWFILENAME, 'w') as new_file:
        new_file.writelines(file_content)


def main():
    copy_paste(r"/Users/eladeliav/PycharmProjects/School2018/Files/file1",
               r"/Users/eladeliav/PycharmProjects/School2018/Files/NewFolder")


if __name__ == '__main__':
    main()
