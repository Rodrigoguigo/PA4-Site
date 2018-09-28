from firebase.DbBasic import DbBasic

x = "ola gostaria de uma pizza de queijo e duas de calabresa com uma fanta \u00e9 uma coca nao seria ruim"
print(x[76:80])

ola = {2: 1, 3: 4}
print(str(list(ola.values())) + " " + str(list(ola.keys())[0]))

f=["a","b","c"]
f.remove(2)
print(f)
y = DbBasic()

print(y.pegarEndereco('15998180031'))

y.cadastrarUsuario('84334234325', 'av. novo', 'po')

y.cadastrarUsuario('15998180031', 'av. trujila', 'gutaolox')

dic = {'ola': 'ta'}
print(dic['xau'])
