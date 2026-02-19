def get_txt_dict(path: str):
    with open(path, 'r') as f:
        return {line.split("=")[0]: line.split("=")[1].strip() for line in f.readlines()}