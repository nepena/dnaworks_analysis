import sys
import os
import subprocess

def generate_dnaworks_input(sequence, output_file="run1.inp", logfile_name="run1.txt"):
    #Set this as the template (keeping all parameters consist and unadjustable by user)
    # Modify the template to use the custom logfile name
    template = f"""# DNAWORKS.inp sample
# Noah Peña, Nov 7th, 2024
# 
# Directives must be flat against the left margin
#
# Comments demarcated by '#'.  All text following # is ignored.
#
TITLE "test2" 

# timelimit 0 # seconds until giving up, 0 means wait forever

melting low 62 # default

length low 50 # default

frequency threshold 10 # default

concentration oligo 1E-7 sodium 0.05 magnesium 0.002 # default


repeat 8 # default

misprime 18 tip 6 max 8 # default

# weight twt 1.0 cwt 1.0 rwt 1.0 mwt 1.0 gwt 1.0 awt 1.0 lwt 1.0 pwt 1.0 fwt 1.0 # default


logfile "{logfile_name}" # default

# previous $I [ $S ]
# previous 1 "{logfile_name}" # default
#
# Mutant run:
#  PREVious 1
#  PREVious 1 "mutant1.out"
#

NUCLeotide
{sequence}
//
"""
    
    # Write to the output file
    with open(output_file, 'w') as file:
        file.write(template)

    print(f"\nThank you, the input file was generated. Data is stored as {output_file}. Log file is {logfile_name}.")

def run_dnaworks(input_file):
    #Run an dnaworks program 
    try:
        # Run the dnaworks command and capture its output in real-time
        process = subprocess.Popen(
            ["dnaworks", input_file], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )

        # Read and print stdout and stderr in real-time
        for line in process.stdout:
            print(line, end='')  # Print each line of stdout from DNAWorks

        for line in process.stderr:
            print(f"Error: {line}", end='')  # Print each line of stderr from DNAWorks

        # Wait for the process to finish and get the return code
        process.wait()

        # Check if there were any errors running the program
        if process.returncode != 0:
            print(f"\nDNAWorks finished with errors. Return code: {process.returncode}")
        else:
            print("\nDNAWorks finished successfully.")
        
    except Exception as e:
        print(f"\nError occurred while running DNAWorks: {str(e)}")

def print_logfile(logfile_name):
    """Print the contents of the log file to the screen."""
    try:
        with open(logfile_name, 'r') as log_file:
            print("\nLog file contents:")
            print(log_file.read())
    except FileNotFoundError:
        print(f"Log file {logfile_name} not found.")
    except Exception as e:
        print(f"Error reading log file: {str(e)}")

def main():
    # Step 1: Ask the user for the DNA sequence with clear prompts
    print("\nHello, welcome! Please provide the DNA sequence below. You can paste the sequence with line numbers or without.")
    print("\nExample format with line numbers:\n   1 TGGTGGGTCTGGCTGATTATTGCCCTGTGCTTTGCCGCATTTTGCTTGTTGGTTTTCTGG\n  61 ATCTTTATTTGCACTGGATGCTGCGGCGGATGTTGTAATTGTTGTGGAATACCTGCACTT")
    print("\nExample format without line numbers:\nTGGTGGGTCTGGCTGATTATTGCCCTGTGCTTTGCCGCATTTTGCTTGTTGGTTTTCTGG\nATCTTTATTTGCACTGGATGCTGCGGCGGATGTTGTAATTGTTGTGGAATACCTGCACTT")
    print("\nPaste your DNA sequence below (with or without line numbers). When you're done, press Enter, type 'DONE', and press Enter again.\n")

    sequence_input = ""
    while True:
        # Reading input sequence with multi-line support
        line = input()
        
        # Check if the line contains only 'DONE' (case-insensitive), to break the loop
        if line.strip().upper() == "DONE":
            break
        
        # Otherwise, add the line to the sequence input
        sequence_input += line + "\n"
    
    # Step 2: Validate that the sequence contains only valid DNA characters (A, T, C, G) and line numbers
    valid_chars = set("ATCG0123456789 ")  # Include digits and spaces for line numbers
    # Filter out the 'DONE' line and validate only actual sequence content
    sequence_lines = sequence_input.splitlines()
    for line in sequence_lines:
        if line.strip().upper() != "DONE":  # Skip the DONE line
            if not set(line.upper()).issubset(valid_chars):
                print("\nError: The sequence should only contain valid DNA characters (A, T, C, G) and numbers for line numbers.")
                sys.exit(1)

    # Step 3: Ask the user for a custom name for the input file (excluding extension)
    print("\nPlease enter a name for this run (without the '.inp' extension):")
    run_name = input().strip()

    # Ensure the file name ends with '.inp' and logfile ends with '.txt'
    if not run_name.endswith('.inp'):
        run_name += '.inp'
    
    logfile_name = run_name.replace('.inp', '.txt')  # Change the extension for the log file

    # Define the directory for saving the log file on the Desktop
    desktop_path = os.path.expanduser('~/Desktop')
    logs_directory = os.path.join(desktop_path, 'DNAworks logs')

    # Create the 'DNAworks logs' directory if it doesn't exist
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Update the file paths to save the log and input files in the 'DNAworks logs' directory
    logfile_name = os.path.join(logs_directory, logfile_name)
    run_name = os.path.join(logs_directory, run_name)

    print(f"\nInput file name: {run_name}")
    print(f"Log file name: {logfile_name}\n")

    # Step 4: Generate the input file with the custom name and logfile name
    generate_dnaworks_input(sequence_input, run_name, logfile_name)

    # Step 5: Ask if the user wants to continue and run DNAWorks
    while True:
        user_input = input("\nTo continue, type 'y' to run DNAWorks on your input file: ").strip().lower()
        if user_input == 'y':
            print(f"\nRunning DNAWorks on your input file {run_name}...\n")
            # Run DNAWorks and capture its output
            run_dnaworks(run_name)

            # Print the contents of the log file
            print_logfile(logfile_name)
            
            break
        else:
            print("\nTo continue, please type 'y'. If you need to quit, type 'n'.")
            user_input = input()

if __name__ == "__main__":
    main()
