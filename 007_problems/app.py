import math
# import string
# dict1= {
#     "a": list(range(1,11)),
#     "b": list(range(11,21)),
#     "c": list(range(21,31))
# }

# for key,val in dict1.items():
#     print(f"{key} has values : {val}")


# print(string.ascii_uppercase)
# s=""
# with open("note.txt", 'r') as file_t:
#     s=file_t.read()


# list1 = s.split(" ")
# print(len(list1))



# string1= "Hey,I am sorry!,donot panic"

# st2= string1.replace(","," ")
# list2= st2.split(" ")
# print(len(list2))

# print(math.cos(1.57))

# print(dir(math))

# wallet_money= 50 

# item_cost= 15

# discount= 3

# item_sp= (1-(0.01*discount))*item_cost 

# remaining= wallet_money-item_sp

# print(remaining)



# days= int(input("how many days till your birthday: "))

# weeks= int(days/7)
# days_w= days%7 

# print(f"your birthday is in {weeks} weeks and {days_w} days")


marks= int(input("Enter the marks you got in maths: "))

if 0<=marks<=100:
    if marks>=90:
        print("You got an A")
    elif marks>=80:
        print("You got a B")
    elif marks>=70:
        print("You got a C")
    elif marks>=60:
        print("You got a D")
    elif marks >= 50:
        print("You got an E")
    else:
        print("OOPS! You got a F")
else:
    print("Invalid marks entered")