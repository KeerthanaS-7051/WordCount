# Word Count and Text Analysis

A Python-based tool to analyze text files and generate detailed statistics such as word count, character count, vocabulary size, frequent words, and more. It also provides options to export results to CSV.

## Features
- Count total words, characters, lines, paragraphs and sentences
- Analyze top 10 frequent words, unique words nad vocabulary size, words that occur once (hapax legomena), longest and shortest words
- Calculate average words per sentence, average characters per word and estimated reading time (200 words/min)
- Output:
  - Summary displayed in a table
  - Additional details outside the table
  - Option to export to csv file
- Support multiple file formats .txt, .py, .html
- Can choose case-sensitivity
- Works for different languages
  
## How to Run

Clone the repository

Run the script
```bash
python wordCount.py
```

Enter file paths
```bash
Enter file paths to analyze (separate multiple files with space): yoga_report.txt
```

Choose case-sentivity
```bash
Do you want case-sensitive analysis? (yes/no): no
```

Export to csv file:
```bash
Do you want to export results to a CSV file? (yes/no): yes
```

If yes, enter the csv file name
```bash
Enter CSV file name (e.g., results.csv): yoga_stats.csv
```
