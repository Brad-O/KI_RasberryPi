import visa


print("Connecting to resources....")
rm = visa.ResourceManager('@py')
print(rm.list_resources())
rm.close()
