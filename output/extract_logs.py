import os
import sys
import mmap
from datetime import datetime

class LogExtractor:
    # Constructor: Initializes the log file path and output directory
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path  # Path to the log file to extract logs from
        self.output_dir = 'output'  # Directory where extracted logs will be saved
        os.makedirs(self.output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    
    # Extract logs corresponding to a specific date from the log file
    def extract_logs_for_date(self, target_date):
        try:
            # Ensure the target_date is in the correct format: YYYY-MM-DD
            datetime.strptime(target_date, '%Y-%m-%d')
            # Create the output file path to store the filtered logs
            output_file_path = os.path.join(self.output_dir, f'logs_{target_date}.txt')
            
            # Open the log file in binary mode to efficiently process large files
            with open(self.log_file_path, 'rb') as file:
                mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)  # Memory-mapped file for fast reading
                matching_logs = []  # List to store logs matching the target date
                current_pos = 0  # Position tracker in the file for reading log entries

                # Search for all log entries containing the target date
                while True:
                    line_start = mm.find(target_date.encode(), current_pos)  # Find the target date in the file
                    if line_start == -1:  # If no more matches are found, break the loop
                        break
                    
                    line_end = mm.find(b'\n', line_start)  # Find the end of the current log entry
                    if line_end == -1:  # If no newline is found, take the whole file as the log entry
                        line_end = len(mm)
                    
                    # Extract the log entry, decode it from bytes to string, and append to the results
                    log_entry = mm[line_start:line_end].decode('utf-8')
                    matching_logs.append(log_entry)

                    # Move the search position to the end of the current log entry
                    current_pos = line_end + 1
                
                # Write the extracted logs to an output file
                with open(output_file_path, 'w') as output_file:
                    output_file.write('\n'.join(matching_logs))
                
                # Provide feedback to the user about the extraction
                print(f"Logs for {target_date} extracted to {output_file_path}")
                print(f"Total logs found: {len(matching_logs)}")
                mm.close()  # Close the memory-mapped file after use
        
        # Handle invalid date format input by the user
        except ValueError:
            print(f"Invalid date format. Please use YYYY-MM-DD format.")
            sys.exit(1)
        # Handle file not found errors
        except FileNotFoundError:
            print(f"Log file not found: {self.log_file_path}")
            sys.exit(1)
        # Handle permission errors when accessing the file
        except PermissionError:
            print(f"Permission denied accessing {self.log_file_path}")
            sys.exit(1)

# Main function to run the program
def main():
    # Ensure the user provides a date argument
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)
    
    target_date = sys.argv[1]  # The date for which to extract logs
    # Create a LogExtractor object with the path to the log file
    extractor = LogExtractor('logs_2024.log')  
    # Call the method to extract logs for the given date
    extractor.extract_logs_for_date(target_date)

# Entry point for running the script directly
if __name__ == "__main__":
    main()
