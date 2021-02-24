import subprocess


result = subprocess.run(["amass", "enum", "-src", "-noalts", "-d", "imesec.ime.usp.br", "-json", "scr/output.json", "-log", "logs/amass.log"], 
                        stdout=subprocess.PIPE).stdout.decode("utf-8")

print(result)

