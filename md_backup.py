#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import os
import sys
import glob
import shutil
import datetime
import ip_address
import port_number

ROOT_FOLDER = '/Users/davidodwyer/Documents/Writing'
TEMP_FOLDER = '/tmp/md_backup'

def copy_md_files():

   """Copies parent and child note-taking directories to /tmp. Prunes subdirectories
   containing pdf file versions or png images. Retains only .md files.
   """

   try:
      if os.path.exists(TEMP_FOLDER):
         shutil.rmtree(TEMP_FOLDER)
      shutil.copytree(ROOT_FOLDER, TEMP_FOLDER)

      subdirs = glob.glob(os.path.join(TEMP_FOLDER, '**/'), recursive=True)

      for d in subdirs:
         end_path = d[-5:]
         if (end_path == '/pdf/') or (end_path == '/png/'):
            shutil.rmtree(d)
   except Exception as e:
      print(e)
      sys.exit(1)

def compress_files(directory=TEMP_FOLDER):

   """Cds to created /tmp directory, creates gzip of parents and child dirs.
   Returns name of zip file.

   """
   try:
      os.chdir(directory)
      filename='md_backup_' + str(datetime.datetime.now().date())
      archive = shutil.make_archive(filename, format='gztar')
      return archive # archive name; no further chdir
   except Exception as e:
      print("Error Archiving")
      print(e)
      sys.exit(1)

def scp_to_server(archive):
    """Runs a bash command to scp the archive to server
    """
    
    try:
       os.system("scp -q -P {0} {1} david@{2}:~/Documents/MD-Backup".format(port_number.NUMBER, archive, ip_address.ADDRESS))
    except:
        print("SCP failed")
        sys.exit(1)

def main():
   copy_md_files()
   archive = compress_files()
   #migrate_archive_to_dropbox(archive)
   scp_to_server(archive)

if __name__ == '__main__':
   main()
   sys.exit(0)
