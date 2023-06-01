import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Search for keywords in files in a directory')
parser.add_argument('-p', '--path', type=str, help='The path of the directory to search')
parser.add_argument('-f', '--file', type=str, help='The path of the text file containing the list of keywords')
parser.add_argument('-o', '--output', type=str, help='The name of the output file to write the results to')
parser.add_argument('-s', '--strings', type=str, help='The path of the strings.exe utility')

args = parser.parse_args()

if not args.path or not args.file:
    print("Error: You must specify the path and file arguments")
    exit()

with open(args.file, "r", encoding="utf8") as f:
    keywords = f.read().splitlines()

def is_binary(file_path):
    text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, text_chars))
    return is_binary_string(open(file_path, 'rb').read(1024))

def search_file(filename, keywords):
    results = []
    if is_binary(filename) and args.strings:
        try:
            output = subprocess.check_output([args.strings, filename]).decode(errors='replace')
            for line_num, line in enumerate(output.split('\n'), start=1):
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        results.append((keyword, filename, line.rstrip()))
                        print(keyword + " : " + filename + " : " + line.rstrip())
        except Exception as e:
            print(f"Error processing file {filename} with strings.exe: {str(e)}")
    else:
        with open(filename, "r", encoding="latin-1", errors='ignore') as f:
            for line_num, line in enumerate(f, start=1):
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        results.append((keyword, filename, line_num, line.rstrip()))
                        print(keyword + " : " + filename + " : " + str(line_num) + " : " + line.rstrip())
    return results

def search_directory(directory, keywords):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            results += search_file(os.path.join(root, file), keywords)
    return results

results = search_directory(args.path, keywords)

if args.output:
    with open(args.output, "w", encoding="utf8") as f:
        for result in results:
            if len(result) == 3:
                f.write(result[0] + " : " + result[1] + " : " + result[2] + '\n')
            else:
                f.write(result[0] + " : " + result[1] + " : " + str(result[2]) + " : " + result[3] + '\n')
else:
    for result in results:
        if len(result) == 3:
            print(result[0] + " : " + result[1] + " : " + result[2])
        else:
            print(result[0] + " : " + result[1] + " : " + str(result[2]) + " : " + result[3])
