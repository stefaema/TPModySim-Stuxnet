import psutil, platform, time, ctypes, os,sys, random, string, statistics,win32api, win32event, win32security, shutil, subprocess
from datetime import datetime
from cryptography.fernet import Fernet

#Compara dos archivos de 500kb para ver si son exactamente el mismo (simula la etapa de CFG)
def compare_files(file1, file2):
    start_time = time.time()
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
    isEqual = content1 == content2
    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken

#Encuentra si el OS es de 64 o 32 bits
def get_os_architecture():
    start_time = time.time()
    arquitectura =  platform.architecture()[0]
    end_time = time.time()
    time_taken = end_time - start_time
    return  time_taken

#Encuentra la versión del OS
def get_os_version():
    start_time = time.time()
    version =  platform.platform()
    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken

#Encuentra si la fecha de hoy es después del 24 de junio de 2012
def is_after_june_24_2012():
    start_time = time.time()
    date = datetime.now()
    comparison_date = datetime(2012, 6, 24)
    end_time = time.time()
    time_taken = end_time - start_time
    comparison = date > comparison_date
    return time_taken

#Encuentra la marca de "Do Not Infect" (Aquí usamos la palabra clave "PALABRACLAVE" pero en stuxnet es una fecha donde "“Habib Elghanian was executed by a firing 
#squad in Tehran sending shock waves through the closely knit Iranian Jewish community.")
def find_keyword_in_file():
    start_time = time.time()
    with open("virucito.txt", 'r') as file:
        content = file.read()
    end_time = time.time()
    time_taken = end_time - start_time
    comparison = 'PALABRACLAVE' in content
    return time_taken

#Devuelve si el proceso tiene permisos administrativos
def is_admin():
    start_time = time.time()
    booleano = ctypes.windll.shell32.IsUserAnAdmin()
    end_time = time.time()
    time_taken = end_time - start_time

    return time_taken
 

#Genera tres archivos de 300k palabras cifradas con una llave aleatoria y luego los borra (Simula la etapa de encriptación de Stuxnet)
def generate_random_words(num_words):
    words = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(num_words)]
    return ' '.join(words)
def cipher_text(text, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(text.encode())
    return cipher_text
def create_ciphered_files(num_files, num_words):
    start_time = time.time()
    key = Fernet.generate_key()
    filenames = []
    for i in range(num_files):
        filename = f'ciphered_file_{i}.txt'
        filenames.append(filename)
        words = generate_random_words(num_words)
        ciphered_words = cipher_text(words, key)
        with open(filename, 'wb') as file:
            file.write(ciphered_words)
    end_time = time.time()
    time_taken = end_time - start_time
    for filename in filenames:
        os.remove(filename)
    
    return time_taken

#Encuentra un proceso específico en el admin. de tareas (Simula la búsqueda de procesos de antivirus para inyectar código como proceso)
def find_process(name):
    success = False
    start_time = time.time()
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name:
            success = True
    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken

def create_and_release_global_mutex(mutex_name):
    start_time = time.time()
    try:
        # Try to create a mutex. If it already exists, this will fail and throw an exception.
        mutex = win32event.CreateMutex(None, False, 'Global\\' + mutex_name)
        if win32api.GetLastError() == 183:
            print(f'Global mutex {mutex_name} already exists')
        else:
            print(f'Global mutex {mutex_name} created')
        
    finally:
        if mutex:
            # Close the handle to the mutex
            win32api.CloseHandle(mutex)
    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken

def get_sacl_status(object_name):
    start_time = time.time()
    # Get the security descriptor for the object
    sd = win32security.GetFileSecurity(object_name, win32security.DACL_SECURITY_INFORMATION)

    # Get the DACL from the security descriptor
    dacl = sd.GetSecurityDescriptorDacl()

    # If the DACL is None, the object is unprotected
    if dacl is None:
        end_time = time.time()
        time_taken = end_time - start_time
        return time_taken

# If the DACL is present, iterate over it to get the access control entries
    for i in range(0, dacl.GetAceCount()):
        ace = dacl.GetAce(i)
        # Each ACE is a tuple containing (ace_type, ace_flags, trustee)
        # You can inspect these values to determine the specific permissions
        ace_type, ace_flags, trustee = ace
        print(f"ACE type: {ace_type}, ACE flags: {ace_flags}, Trustee: {trustee}")

    end_time = time.time()
    time_taken = end_time - start_time
    return time_taken

def injection():
    start_time = time.time()
    # Get the current script name
    script_name = os.path.basename(__file__)
    # Create a new script name for the copy
    new_script_name = 'copy_' + script_name
    # Check if the copy already exists
    if not os.path.basename(__file__) == "copy_scriptsDuracion.py":
        # Copy the script
        shutil.copy(script_name, new_script_name)
        # Execute the copied script
        subprocess.call(['python', new_script_name])

    end_time = time.time()
    time_taken = end_time - start_time
    os.remove(new_script_name)
    return time_taken




#Función que ejecuta todas las funciones anteriores y devuelve el tiempo promedio y la desviación estándar    
def repeat_function1(repetitions):
    results = []
    for _ in range(repetitions):
        result = compare_files("fileA", "fileB")
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function1(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function2(repetitions):
    results = []
    for _ in range(repetitions):
        result = get_os_architecture()
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function2(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function3(repetitions):
    results = []
    for _ in range(repetitions):
        result = get_os_version()
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function3(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function4(repetitions):
    results = []
    for _ in range(repetitions):
        result = is_after_june_24_2012()
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function4(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function5(repetitions):
    results = []
    for _ in range(repetitions):
        result = find_keyword_in_file()
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function5(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function6(repetitions):
    results = []
    for _ in range(repetitions):
        result = is_admin()
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function6(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function7(repetitions): 
    results = []
    for _ in range(repetitions):
        result = create_ciphered_files(3, 30000)
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function7(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function8(repetitions):
    results = []
    for _ in range(repetitions):
        result = find_process("Discord.exe")  
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function8(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function9(repetitions):
    results = []
    for _ in range(repetitions):
        result = create_and_release_global_mutex("MyMutex")  
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function9(repetitions)
        return
    std_dev = statistics.stdev(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)
    return mean, std_dev

def repeat_function10(repetitions):
    results = []
    for _ in range(repetitions):
        result = get_sacl_status("C:\\Users\\stefa\\Desktop\\TPModySim\\scriptsDuracion.py")  
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function10(repetitions)
        return
    std_dev = statistics.stdev(results)
    print(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)

def repeat_function11(repetitions):
    results = []
    for _ in range(repetitions):
        result = injection() 
        results.append(result)
    mean = statistics.mean(results)
    if(mean == 0.0):
        repeat_function11(repetitions)
        return
    std_dev = statistics.stdev(results)
    print(results)
    msg = "Mean: " + str(mean) + " seconds\nStandard deviation: " + str(std_dev) + " seconds"
    print(msg)

def master_repeat(repeticiones):
    print("\nCFG:")
    repeat_function1(repeticiones)
    print("\nOS architecture:")
    repeat_function2(repeticiones)
    print("\nOS version:")
    repeat_function3(repeticiones)
    print("\nFecha limite")
    repeat_function4(repeticiones)
    print("\nDO NOT INFECT marker:")
    repeat_function5(repeticiones)
    print("\nAdmin Peivileges:")
    repeat_function6(repeticiones)
    print("\nCifrado de archivos:")
    repeat_function7(2)
    print("\nIdentificando procesos:")
    repeat_function8(2)
    #print("\nGlobal Mutex:")
    #repeat_function9(2)
    # print("\nSACL Status:")
    # repeat_function10(2)
    print("\nInjection:")
    repeat_function11(2)

master_repeat(100)