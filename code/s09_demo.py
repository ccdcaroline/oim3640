

# i = 0 
# while i < 5:
#    print(i)
#    i += 1


# response = ""
# while response != "quit":
#    response = input("Enter command: ")
#    print(f"You said {response}") 

# Simple while loop example: counting down
# countdown = 5
# while countdown > 0:
#     # print(f"Countdown: {countdown}")
#     # countdown -= 1
# print("Blastoff!")

# while True: 
#     user_input = input("Enter username: ")
#     pass_input = input("Enter password: ")

#     if user_input == "admin" and pass_input == "password": 
#         print("Login successful!")
#         break 


# break - exit the loop immediately
# words = ["hello", "world", "target", "python"]
# for w in words:
#     print('checking:' , w)
#     if w == "target":
#         print("Found it!\n")
#         continue
#     print("Not the target\n")

# # continue - skip to the next iteration
# for num in range(10):
#     if num % 2 == 0:
#         continue
#     print(num)  # prints odd numbers only

def f(n): 
    for num in range(n): 
        if num % 2 == 0: 
            continue
        return(num)
    
print(f(10))


# Check if downloaded words text file
for line in open("data/words.txt"): 
    print(line) 