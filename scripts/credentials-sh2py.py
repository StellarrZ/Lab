def _mapper(line):
    ind_eq = line.find("=")
    return "os.environ[\"" + line[7:ind_eq] + "\"] = \"" + line[ind_eq + 1:] + "\""
    

lines = """    """

res = list(map(_mapper, lines.split("\n")))
print("import os")
print("\n".join(res))
