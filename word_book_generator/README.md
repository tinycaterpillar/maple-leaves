This program takes a PDF file as input and generates a wordbook by extracting its text, analyzing word frequencies, and filtering out high-frequency words based on real-world usage data. The output is a curated list of less common or more useful vocabulary found in the text.

Vocabulary levels are determined using the following reference:
https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000

How to build?
pyinstaller --clean wordbook_debug.spec