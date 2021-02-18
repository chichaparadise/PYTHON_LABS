def gamma_function(a):
    if a == 1:
        return a
    else:
        return gamma_function(a - 1) * a

def main():
    n = input("Enter your number:\n")
    print("Your result is", gamma_function(int(n)))

if __name__ == "__main__":
    main()