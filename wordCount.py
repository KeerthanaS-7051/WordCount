import os
import sys
import re
import argparse
from collections import Counter
from tabulate import tabulate

stop_words=['the','in','on','a','at','to','is','it','and','or']     #stop words

def analyze_text(text, case_sensitive=False):
    if not case_sensitive:
        text=text.lower()

    words=re.findall(r"\b\w+\b",text)                                       #count words
    total_words=len(words)
    lines=text.splitlines()                                                 #count lines
    total_lines=len(lines)
    paragraphs=[p for p in text.split("\n\n") if p.strip()]                 #count paras
    total_paragraphs=len(paragraphs)
    sentences=re.split(r'[.!?]+',text)                                      #count sentences
    sentences=[s.strip() for s in sentences if s.strip()]
    total_sentences=len(sentences)
    total_characters=len(text)                                               #count characteres with space
    total_char_space=len(text.replace(" ",''))                               #count characters without space
    freq=Counter(w for w in words if w not in stop_words)                    #word cloud data (word:freq pairs)
    top_10=freq.most_common(10)                                              #top 10 words
    hapax=[w for w,c in freq.items() if c==1]                                #words that occur once
    avg_words=total_words/total_sentences if total_sentences else 0          #avg words per sentence
    avg_chars=total_char_space/total_words if total_words else 0             #avg characs per word
    unique_words=set(words)                                                  #unique words
    vocab_size=len(unique_words)                                             #vocab size
    longest_word=max(words,key=len) if words else ''                         #longest word
    shortest_word=min(words,key=len) if words else ''                        #shortest word
    reading_time=total_words/200                                             #estimated reading time

    return{
        "Total words":total_words,
        "Total characters":total_characters,
        "Total characters excluding space":total_char_space,
        "Total lines":total_lines,
        "Total paragraphs":total_paragraphs,
        "Top 10 frequent words":top_10,
        "Longest word":longest_word,
        "Shortest word": shortest_word,
        "Average words per sentence":round(avg_words,2),
        "Average characters per word":round(avg_chars,2),
        "Unique words": unique_words,
        "Total vocabulary size": vocab_size,
        "Words that occur only once (hapax legomena)":hapax,
        "Estimated reading time in min":round(reading_time,2),
        "Word cloud data":dict(freq)
    }

def process_file(path, case_sensitive=False):
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except UnicodeDecodeError:
        print(f"Could not read file {path} with UTF-8 encoding.")
        return None

    return analyze_text(text, case_sensitive)

def main():
    files_input = input("Enter file paths to analyze (separate multiple files with space): ").strip()
    files = files_input.split()

    case_choice = input("Do you want case-sensitive analysis? (yes/no): ").strip().lower()
    case_sensitive = case_choice == "yes"

    csv_choice = input("Do you want to export results to a CSV file? (yes/no): ").strip().lower()
    csv_filename = None
    if csv_choice == "yes":
        csv_filename = input("Enter CSV file name (e.g., results.csv): ").strip()

    results = []
    summary_metrics = [
        "Total words",
        "Total characters",
        "Total characters excluding space",
        "Total lines",
        "Total paragraphs",
        "Average words per sentence",
        "Average characters per word",
        "Longest word",
        "Shortest word",
        "Total vocabulary size",
        "Estimated reading time in min",
    ]

    for file in files:
        stats = process_file(file, case_sensitive)
        if stats:
            print(f"\n=== Analysis for {file} ===\n")
            table = [[metric, stats[metric]] for metric in summary_metrics]
            print(tabulate(table, headers=["Metric", "Value"], tablefmt="grid"))

            print("\n--- Additional Details ---")
            print(f"Top 10 frequent words: {list(stats['Top 10 frequent words'])[:20]}")
            print(f"Unique words count: {stats['Total vocabulary size']}")
            print(f"Unique words (first 20 shown): {list(stats['Unique words'])[:20]}")
            print(f"Hapax count: {len(stats['Words that occur only once (hapax legomena)'])}")
            print(f"Hapax legomena (first 20 shown): {stats['Words that occur only once (hapax legomena)'][:20]}")
            print(f"Word cloud data (top 20 shown): {list(stats['Word cloud data'].items())[:20]}")

            results.append((file, stats))

    # Comparison across files
    if len(results) > 1:
        print("\n=== Comparison Between Files ===\n")
        comp_table = []
        headers = ["Metric"] + [file for file, _ in results]
        for metric in summary_metrics:
            row = [metric] + [stats[metric] for _, stats in results]
            comp_table.append(row)
        print(tabulate(comp_table, headers=headers, tablefmt="grid"))
        
    # csv export
    if csv_filename and csv_filename.strip() and results: 
        import csv, os, time
        filename = csv_filename
        if os.path.exists(filename):
            filename = f"{os.path.splitext(csv_filename)[0]}_{int(time.time())}.csv"
            print(f"File already exists. Saving as {filename} instead.")

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            headers = ["File"] + summary_metrics
            writer.writerow(headers)
            for file, stats in results:
                row = [file] + [stats[metric] for metric in summary_metrics]
                writer.writerow(row)
        print(f"\nResults exported to {filename}")
        
if __name__=='__main__':
    main()
