from ext import ext
print("hi")
ext.cpu_add(1,4)
print(f"add in cpu : {ext.cpu_add(1,2)} ")
print(f"add in gpu : {ext.gpu_add(1,2)} ")
