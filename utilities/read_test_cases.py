import os


def return_path_files(test_folder="tests"):
    path_to_files = os.path.join(
        os.getcwd(),
        test_folder,
    )

    files = list(set([x.split(".")[0] for x in os.listdir(path_to_files)]))
    files = sorted(files, key=lambda x: int(x))

    return path_to_files, files
