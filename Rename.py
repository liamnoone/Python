import os
import sys


def rename(file_, new_name, extension="", extensions=[]):
    if not os.path.isfile(file_):
        raise FileNotFoundError("File does not exist")

    else:
        os.path.normpath(file_)

        directory = os.sep.join(file_.split(os.sep)[0:-1])
        file_name = os.extsep.join(
            file_.split(os.sep)[-1].split(os.extsep)[0:-1])
        extension = file_.split(os.extsep)[-1]

        # Check if the file will actually be a different filename,
        # only rename
        if file_name == new_name:
            output = "No change: " + new_name

        else:
            os.rename(file_,
                      os.path.join(directory,
                                   os.extsep.join([new_name, extension])))

        # If the last word delimited by the extension seperator (usually '.')
        # is an extension, print all but that word,
        # otherwise print the full word (incase there i sn't an extension)
            output = (file_name if extension_check(extension, extensions) else
                      os.extsep.join([file_name, extension]))
            output += " -> " + new_name

        print(output)

def extension_check(string, array):
    return string.lower() in [str_.lower() for str_ in array]

if __name__ == "__main__":
    print("Args: ", len(sys.argv))
    if len(sys.argv) == 3:
        rename(sys.argv[1], sys.argv[2])
    else:
        raise AttributeError("Couldn't process. 2-3 Arguments expected:\n \
            1. File\n2. New name\n3. Optional: Seperator")
