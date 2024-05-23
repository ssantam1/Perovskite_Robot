import subprocess

#Method to install packages using pip
def pip_install(packageName:str):
    try:
        print(f'Attempting to install {packageName}, please allow up to 30 seconds for installation.')
        subprocess.call(f'py -m pip install {packageName}')
    except:
        print(f'Aailed to install {packageName} using py -m pip, trying raw pip request.')
        subprocess.call(f'pip install {packageName}')
        print(f'{packageName} should be installed, fatal errors will occur if install failed.')

#Check for pyserial installation, and install it if it isn't found
try:
    import serial
except:
    pip_install("pyserial")

#This is only here so the program doesn't immediately exit when there's an error
input("Press any key to exit")