# -*- coding: utf-8 -*-
PART = 1024


def copy_paste(file1, file2):
    """
    copies contents from "file" to the new file in the given folder but in chunks
    """
    try:
        file_content = None
        with open(file1, 'rb') as file1Handle:
            with open(file2, 'wb') as file2Handle:
                file_content = file1Handle.read(PART)
                while file_content != '':
                    file2Handle.write(file_content)
                    file_content = file1Handle.read(PART)
    except IOError as e:
        print "Error: error#", e.errno
        print e
        return False


def main():
    """
    calls copy_paste with paths to file1 and file2
    """
    copy_paste(r"/Users/eladeliav/PycharmProjects/School2018/Files/file",
               r"/Users/eladeliav/PycharmProjects/School2018/Files/NewFolder/file2")


if __name__ == '__main__':
    main()
