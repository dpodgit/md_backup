#!/Users/davidodwyer/anaconda3/bin/python

import os
import sys
import glob
import shutil
import datetime
import dropbox
import dropbox_credentials 

ROOT_FOLDER = '/Users/davidodwyer/Documents/Texts'
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
      archive = shutil.make_archive('temp_name', format='zip')
      return archive # archive name; no further chdir
   except Exception as e:
      print("Error Archiving")
      print(e)
      sys.exit(1)

def migrate_archive_to_dropbox(archive):

   """Reads zip file and uploads to dropbox via API.
   """

   with open(archive, 'rb') as file:
      data = file.read()
   
   try:
      dbx = dropbox.Dropbox(dropbox_credentials.ACCESS_TOKEN)
      archive_name = '/md_backup_' + str(datetime.datetime.now().date()) + '.gz'
      dbx.files_upload(data, archive_name, mute=True)
   except dropbox.exceptions.ApiError as err:
      print('*** API error', err)

def main():
   copy_md_files()
   archive = compress_files()
   migrate_archive_to_dropbox(archive)

if __name__ == '__main__':
   main()
   sys.exit(0)
