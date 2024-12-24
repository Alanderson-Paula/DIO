# Créditos à: Jones Granatyr :)

import os

# o que o codigo abaixo faz: adiciona o nome e caminho de todos as fotos (.jpg) em um txt
imagens = []
os.chdir(os.path.join("data", "obj_valid"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".jpg"):
        imagens.append("data/obj_valid/" + filename)
os.chdir("..")

with open("test.txt", "w", encoding='utf-8') as outfile:
    for img in imagens:
        outfile.write(img)
        outfile.write("\n")
    outfile.close()
os.chdir("..")
