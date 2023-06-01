# Keyword Search in Directory

This Python script recursively searches for specified keywords in all files within a provided directory path. It can handle both text and binary files.

## Usage

This script requires Python 3.6 or later. Run it with the following command:


```
python keyword_search.py -p <path> -f <file> [-o <output>] [-s <strings.exe>]
```

The arguments are as follows:

- `-p`, `--path`: (Required) The path of the directory to search.
- `-f`, `--file`: (Required) The path of the text file containing the list of keywords to search for, one per line.
- `-o`, `--output`: (Optional) The name of the output file to write the results to. If not provided, results will be printed to stdout.
- `-s`, `--strings`: (Optional) The path of the `strings.exe` utility, used to extract readable content from binary files. If not provided, the script will only search in text files.

## Results

For each keyword found, a line is output in the following format:


`<keyword> : <filename> : <line number> : <line text>`

For binary files processed with `strings.exe`, the line number and line text are replaced with the string found:



`<keyword> : <filename> : <string found>`

## Dependencies

This script uses Python's built-in libraries. If the `-s` or `--strings` option is used, the `strings.exe` utility (or equivalent on non-Windows systems) must be available.
