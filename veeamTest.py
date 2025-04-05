import time
import datetime
import os, shutil
import errno
import logging



def syncDir(src, dest, period):
    # Copy all files at the first start of the program
    for root, dirs, files in os.walk(src):  # Interate over all directories and subdirectories
        for file in files:
            source_file = os.path.join(root, file)  #Construct full path of source file
            dest_file = os.path.join(dest, os.path.relpath(source_file, src)) #Construct full path of destination file
            dest_dir = os.path.dirname(dest_file)   #Construct full path of destination directory
            if not os.path.exists(dest_dir):    #If directory doesn't exist - create it and log it
                os.makedirs(dest_dir)
                logging.info(f'Created directory: {dest_dir}')
                print((f'Created directory: {dest_dir}'))
            shutil.copy(source_file, dest_file)  # Copy source file to destination file and log it
            logging.info(f'Copied file: {source_file} to {dest_file}')
            print((f'Copied file: {source_file} to {dest_file}'))

    # Store the last modification time of each file
    file_mtime = {} #Dictionary to store the last modification time of each file
    dir_mtime = {} #Dictionary to store the last modification time of each directory   
    for root, dirs, files in os.walk(src):
        for file in files:
            source_file = os.path.join(root, file)
            file_mtime[source_file] = os.path.getmtime(source_file)

    while True:
        # Check for modified files and copy them
        for root, dirs, files in os.walk(src):
            for dir in dirs:
                dir_path = os.path.join(root, dir)  #Construct full path of directory
                if dir_path not in dir_mtime:   #If path not in dictionary - add it
                    dir_mtime[dir_path] = os.path.getmtime(dir_path)    #Add path to dictionary
                    dest_dir_path = os.path.join(dest, os.path.relpath(dir_path, src))
                    if not os.path.exists(dest_dir_path):   #If directory doesn't exist - create it and log it
                        os.makedirs(dest_dir_path)
                        logging.info(f'Created directory: {dest_dir_path}')
                        print(f'Created directory: {dest_dir_path}')
            
            for file in files:
                source_file = os.path.join(root, file)
                if source_file not in file_mtime:   #If path not in dictionary - add it and log it
                    file_mtime[source_file] = os.path.getmtime(source_file)
                    logging.info(f'Created file: {source_file}')
                    print(f'Created file: {source_file}')
                if os.path.getmtime(source_file) > file_mtime[source_file]: #Check if file is modified 
                    dest_file = os.path.join(dest, os.path.relpath(source_file, src)) #Construct full path of destination file
                    dest_dir = os.path.dirname(dest_file)   #Construct full path of destination directory
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir, exist_ok=True) #If directory doesn't exist - create it and log it
                        logging.info(f'Created directory: {dest_dir}')
                        print(f'Created directory: {dest_dir}')
                    shutil.copy(source_file, dest_file)  # Copy source file to destination file and log it
                    logging.info(f'Copied file: {source_file} to {dest_file}')
                    print(f'Copied file: {source_file} to {dest_file}')
                    file_mtime[source_file] = os.path.getmtime(source_file) #Update dictionary

        # Check for removed files and remove them
        for file in list(file_mtime.keys()):
            if not os.path.exists(file):
                dest_file = os.path.join(dest, os.path.relpath(file, src)) # Gets a path to the file in the destination directory
                if os.path.exists(dest_file):
                    os.remove(dest_file)              #Removes the file and logs it
                    logging.warning(f'Removed file: {dest_file}')
                    print(f'Removed file: {dest_file}')
                del file_mtime[file]                  #Removes the file from the dictionary
                
        # Check for removed directories and remove them
        for dir_path in list(dir_mtime.keys()):
            dest_dir_path = os.path.join(dest, os.path.relpath(dir_path, src)) # Gets a path to the directory in the destination directory
            if not os.path.exists(dir_path):
                if os.path.exists(dest_dir_path):
                    shutil.rmtree(dest_dir_path)         #Removes the directory and logs it
                    logging.warning(f'Directory deleted: {dir_path}')
                    print(f'Directory deleted: {dir_path}')
                del dir_mtime[dir_path]                  #Removes the directory from the dictionary

        time.sleep(period)  # Sleep for the specified period
    
# Function to create text files
def textFileMake(path, idx):
    file = open(path +"\\textFile" + str(idx) + ".txt", "w")
    file.write("Testing text file " + str(idx))
    file.close()
    logging.info(path +"\\textFile" + str(idx) + ".txt" + " directory created successfully.")
    print(path + "\\textFile" + str(idx) + ".txt" + " text file created successfully.")

# Function to create initial directories
def folderCreate(path):
    try:
        os.mkdir(path)
        print(path + " directory created successfully.")
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(path + " directory already exists.")
        else:
            raise
            
def create_directories(inputPath, syncPath, logPath):
    folderCreate(logPath)   #
    folderCreate(inputPath) # Creating 3 directories
    folderCreate(syncPath)  #

    e = datetime.datetime.now()
    currentTime = e.strftime("%Y-%m-%d_%H-%M-%S")
    logFormat = str(currentTime + ".log")       # Setting logging file naming format sorted by current date and it's path
    timePath = os.path.join(logPath, logFormat)
    logging.basicConfig(level=logging.INFO, filename=str(timePath) ,filemode="a", format="%(asctime)s %(levelname)s %(message)s")
    
    # Create directories in input directory to fill it's contents for this test purposes
    for i in range(5):
        try:
            os.mkdir(inputPath + "\\Text File Directory " + str(i))
            print(inputPath + "\\Text File Directory " + str(i) + " directory created successfully.")
            logging.info(inputPath + "\\Text File Directory " + str(i) + " directory created successfully.")
        except OSError as e:
            if e.errno == errno.EEXIST:
                logging.error(inputPath + "\\Text File Directory " + str(i) + " directory already exists.")
                print(inputPath + "\\Text File Directory " + str(i) + " directory already exists.")
            else:
                raise
        textFileMake(inputPath + "\\Text File Directory " + str(i), i) # Call for creating text files
    

def main():
    sourcePath = input("Enter path: ")                              # Get source path
    syncPath = input("Enter synchronization path: ")                # Get synchronization path
    logPath = input("Enter log path: ")                             # Get log path
    syncTime = input("Enter synchronization interval in seconds: ") # Get synchronization interval
    create_directories(sourcePath, syncPath, logPath)               #Create directories and initialize logging
    syncDir(sourcePath, syncPath, int(syncTime))                    #Begin synchronization
    
    
main()