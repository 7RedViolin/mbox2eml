import argparse
import os
import sys
import hashlib

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def lets_go(file, folder):
  blank_lines_count = 2
  file_count = 0
  file_skipped_count = 0
  is_dupe = False

  with open(file, "r") as mbox_file:
    print("Processing file: {0}".format(file))
    print("Please wait ...")

    for line in mbox_file:
      line_stripped = line.strip()
      line_parts = line_stripped.split(' ')

      if blank_lines_count >= 1 and line_stripped.startswith("From "):
        msg_year = line_parts[7]
        msg_month = "{:0>2}".format(int(months.index(line_parts[3])) + 1)
        msg_day = line_parts[4]
        msg_time = line_parts[5].replace(':','')
        msg_hash = hashlib.sha1(line_stripped.encode("UTF-8")).hexdigest()

        eml_file = "{0}{1}{2}-{3}-{4}.eml".format(msg_year,msg_month,msg_day,msg_time,msg_hash[:10])

        full_output = os.path.join(folder, eml_file)

        if os.path.isfile(full_output):
          is_dupe = True
          file_skipped_count += 1
          print("File skipped: {0}".format(full_output))
          continue
        
        new_file = open(full_output, "a")
        file_count += 1
        print("File created: {0}".format(full_output))

        new_file.write("{0}".format(line))
      else:
        if is_dupe == True:
          continue
        new_file = open(full_output, "a")
        new_file.write("{0}".format(line))

      if line_stripped == '':
        blank_lines_count += 1
      else:
        blank_lines_count = 0

def main():
  parser = argparse.ArgumentParser(description="MBOX to eml files")
  parser.add_argument('--file','-f',type=str,required=True,help="MBOX file")
  parser.add_argument('--output','-o',type=str,required=False,help="Output directory. Defaults to '~/Desktop/results/'")

  args = parser.parse_args()

  if args.output is not None:
    folder_name = args.output
  else:
    folder_name = os.environ.get('HOME') + '/Desktop/results'

  #Check if folder exists. If not, make one
  if os.path.isdir(folder_name) is False:
    try:
      os.mkdir(folder_name)
    except:
      sys.exit("Error! Could not create directory {0}".format(folder_name))
  else:
    print("Directory {0} already exists. Data may be overwritten.".format(folder_name))

  if os.path.exists(args.file) is False:
    sys.exit("Error! Could not find file {0}".format(args.file))
  else:
    print("Using file {0}".format(args.file))

  lets_go(args.file, folder_name)

if __name__ == "__main__":
  sys.exit(main())