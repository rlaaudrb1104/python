import base64

def base64_encode(filename):
  with open (filename, 'rb') as file:
    result = base64.b64encode(file.read())
    file.close()
  with open (filename, 'wb') as file:
    file.write(result)
    file.close()
    print(result)

def base64_decode(filename):
  with open(filename, 'rb') as file:
    result = (base64.b64decode(file.read()))
  with open(filename, 'wb') as file:
    file.write(result)
    file.close()
    print(result)


num = int(input("1.base64 encodig\n2.base64 decoding\n"))
filename = input("파일 이름 입력:\n")
if (num == 1):
  base64_encode(filename)
elif(num == 2):
  base64_decode(filename)
else:
  print("잘못된 입력입니다.")

