# Text Processing Program: Keyword Search and Data Extraction
This program integrates several text processing techniques, including keyword search via an Aho-Corasick automaton, Red-Black Tree for efficient insertion and searching, and data extraction from web pages and PDF files. The program allows you to extract text from either a URL or a PDF, process the text to find keywords, and organize the results for further use.

# Key Features
Keyword Search with Aho-Corasick Automaton: The program utilizes the Aho-Corasick algorithm, which constructs an automaton for efficient keyword searching in large texts. It allows users to search for multiple keywords across a given text, efficiently finding all occurrences.

Red-Black Tree: Implements a Red-Black Tree data structure for maintaining a balanced collection of keywords or values, supporting efficient insertions, deletions, and searches.

Web Scraping: Fetches a web page’s content using the requests library and processes it to extract the text. The program can handle webpage content extraction and keyword searching from HTML data.

PDF Text Extraction: Extracts plain text from PDF documents using the fitz library, enabling the program to read and process content from PDFs.

Sentence Extraction: Utilizes regular expressions to split text into sentences, making it easier to understand and analyze the content.

# Workflow
Data Input: The user can choose to either scrape a web page or extract text from a PDF. They are prompted to provide a URL or a file path accordingly.

Text Processing: The program extracts sentences from the fetched text using regular expressions and tokenizes it into individual sentences.

Keyword Search: After the text extraction, the program uses the Aho-Corasick automaton to find all occurrences of specified keywords within the text. Keywords can be entered by the user as space-separated words.

Red-Black Tree for Data Storage: Keywords are managed using a Red-Black Tree, allowing for efficient insertions and searches.
