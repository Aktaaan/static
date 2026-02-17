import os
import shutil

def copy_directory(source_path, destination_path):
    # delete public contents
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir(f"public")

    def reck_copy(src_path, dst_path):
        for filename in os.listdir(src_path):
            from_path = os.path.join(src_path, filename)
            to_path = os.path.join(dst_path, filename)

            if os.path.isfile(from_path):
                shutil.copy(from_path, to_path)
            else:
                os.mkdir(to_path)
                reck_copy(from_path, to_path)

    reck_copy(source_path, destination_path)

