import os

file_imports = 'src' + os.sep + 'imports.py'
file_main = 'src' + os.sep + 'main.py'
special = (file_imports, file_main)
def read_file(path):
	c = open(path, 'rt')
	t = c.read()
	c.close()
	return t

def get_all(path):
	global special
	output = []
	for thing in os.listdir(path):
		newpath = path + os.sep + thing
		if '.svn' in newpath:
			continue
		if os.path.isdir(newpath):
			output = output + get_all(newpath)
		else:
			if newpath in special:
				pass
			else:
				output.append(read_file(newpath))
	return output

files = get_all('src')
files = [read_file(file_imports)] + files + [read_file(file_main), "main()"]

code = "\n\n".join(files)

c = open('run.py', 'wt')
c.write(code)
c.close()
