from whois import whois 

def raw_input(data):
    return data

data = raw_input(input("Enter a Domain name: "))

w = whois(data)
print(w)