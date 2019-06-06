# -*- coding: utf-8 -*-


def check_file_exits(filename):
    try:
        file1 = open(filename, 'r')
        return True
    except IOError:
        print('There was an error opening the file!')
        return False


def copy_paste(file1, folder):
    """
    copies the contents of file to file2
    """
    file_content = None
    with open(file1, 'rb') as my_text:
        file_content = my_text.read()
    with open(folder, 'wb') as new_file:
        new_file.write(file_content)


def main():
    """
    calls copy_paste with the paths to file and file2
    """
    copy_paste(r"/Users/eladeliav/PycharmProjects/School2018/Files/file1",
               r"/Users/eladeliav/PycharmProjects/School2018/Files/NewFolder/file2")


if __name__ == '__main__':
    main()
