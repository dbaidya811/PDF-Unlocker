# PDF Password Unlocker

A powerful tool to unlock password-protected PDF files using brute force techniques. This application can handle both encrypted and unencrypted PDFs with a user-friendly interface.

## Features

- **Brute Force Attack**: Systematically tries all possible numeric combinations to unlock PDFs
- **Smart Detection**: Automatically detects if a PDF is already unlocked
- **Efficient Processing**: Tries passwords in a specific order (4-digit, 5-digit, then 6-digit)
- **Real-time Progress**: Shows current password attempts and cracking speed
- **Modern UI**: Clean, dark-themed interface with drag-and-drop support

## How Brute Force Works

The application uses a **sequential brute force** method to attempt unlocking PDFs:

1. **Password Lengths**: Tries passwords in this order:
   - 4-digit numbers (0000 to 9999)
   - 5-digit numbers (00000 to 99999)
   - 6-digit numbers (000000 to 999999)

2. **Optimized Search**:
   - Tries passwords in sequential order
   - Reports progress every 25 attempts
   - Shows attempts per second (avg. 100-150 attempts/sec)
   - Stops immediately when the correct password is found

3. **Performance**:
   - Single-threaded for reliability
   - Processes approximately 100-150 password attempts per second
   - Memory-efficient PDF handling

## Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dbaidya811/PDF-Unlocker.git
   cd PDF-Unlocker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`

3. Upload a PDF file:
   - Drag and drop or click to select a file
   - The app will automatically detect if it's encrypted
   - If encrypted, the brute force process will begin
   - If successful, the unlocked PDF will be downloaded automatically

## Security Notes

- This tool is for legal use only
- Always ensure you have permission to unlock the PDF files
- The application runs entirely in your browser - no files are uploaded to any server
- Processing happens locally on your machine

## Performance Tips

- For best results, use on a modern computer
- Close other CPU-intensive applications while cracking
- The process may take time for longer password lengths
- Progress is shown in the terminal and web interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided for educational and legal use only. The developers are not responsible for any misuse of this software. Always ensure you have the legal right to unlock any PDF file before proceeding.
