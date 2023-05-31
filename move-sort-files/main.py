import shutil
import sys
import os
import time

def t_or_f(arg):
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
       return True
    elif 'FALSE'.startswith(ua):
       return False
    else:
       pass  #error condition maybe?
   
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)

# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")
     
print("\n")
old_path = sys.argv[1]
new_path = sys.argv[2]
b_cut = t_or_f(sys.argv[3])

# Get the file listing int a directory from original folder
if(old_path):
    dir_list = os.listdir(old_path)

# get the number of files in our director
num_of_files = len(dir_list)

# now loop through the files
for i in range(0, num_of_files):
    #Get the created time   
    time_m = os.path.getmtime(old_path+dir_list[i])
    
    m_time = time.ctime(time_m)
    
    # Using the timestamp string to create a
    # time object/structure
    t_obj = time.strptime(m_time)
    
    # Transforming the time object to a timestamp
    # of ISO 8601 format
    T_stamp = time.strftime("%Y_%m_%d\\", t_obj)
    print(T_stamp)
    
    new_dir_path = new_path+T_stamp
    #now we need to check to see if a folder of this name exists in the new location and create if we need to
    #create folder
    #check to see if new path exists
    if not (os.path.exists(new_path)):
        print("Creating director at " + new_path)
        os.mkdir(new_path)
        
    if not (os.path.exists(new_dir_path)):
        print("Creating director at " + new_dir_path)
        os.mkdir(new_dir_path)
    
    new_file_path = new_dir_path+dir_list[i]
    current_file_path = old_path+dir_list[i]
    #copy/cut file to new location
    if b_cut:
        print("Moving file from \n" + current_file_path +  " \ntime stamp " +T_stamp + " " + "\n to \n" + new_file_path)
        shutil.move(current_file_path, new_file_path)
    else:
        print("Copy file from \n" + current_file_path + " \ntime stamp " + T_stamp + " " + "\n to \n" + new_file_path)
        shutil.copy(current_file_path,new_file_path)


