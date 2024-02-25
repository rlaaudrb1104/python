import random


num = int(input("몇 장을 뽑으실 건가요?"))


for i in range(1, num+1):
  lotto_num = [0,0,0,0,0,0]
  for r in range(0, 6):
    lotto_num[r] = random.randint(1,45)
    if r > 0:
      for k in range(0, r):
        if lotto_num[r] == lotto_num[k]:
          lotto_num[r] = random.randint(1,45)

    bonus_lotto_num = random.randint(1,45)
  for j in range(0, 6):
    if bonus_lotto_num == lotto_num[j]:
      bonus_lotto_num = random.randint(1,45)


  lotto_num.sort()
  print(lotto_num ,'+', bonus_lotto_num)
