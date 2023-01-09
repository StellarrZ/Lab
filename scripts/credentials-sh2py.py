def _mapper(line):
    ind_eq = line.find("=")
    return "os.environ[\"" + line[7:ind_eq] + "\"] = \"" + line[ind_eq + 1:] + "\""
    

credentials = """    """

print("import os")
print("\n".join(map(_mapper, credentials.split("\n"))))
