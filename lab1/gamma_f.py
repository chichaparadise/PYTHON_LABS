import pickle
def gamma_function(a):
    if a == 1:
        return a
    else:
        return gamma_function(a - 1) * a

def main():
    try:
        n = int(input("Enter your number: "))
        print("Your result is", gamma_function(int(n)))
    except:
        print("Error!")

if __name__ == "__main__":
    main()