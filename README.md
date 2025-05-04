Did you ever wanted to keep & organize your annotations from your Kindle, after having finished reading a book?

Such a clean exporting functionality is now possible with:

# Vokindle

A Python tool to extract vocabulary and quotes from Kindle HTML exports, with optional translation support and statistics.

## Features

- Extract single-word highlights as a sorted vocabulary list
- Extract multi-word highlights as quotes with metadata
- Support for translations into multiple languages
- Merge multiple Kindle exports into a single output, with duplicate handling
- Detailed statistics
- Clean output format with organized directory structure
- Easy to use command-line interface
- Python API for programmatic usage

## Installation

1. Clone the repository.
2. Navigate to the repository.
3. Execute the following to install the package with all library dependencies.

```bash
pip install -e .
```

## Usage

### Command Line Interface

Basic usage with a single file:
```bash
vokindle path/to/kindle.html
```

Process multiple files:
```bash
vokindle file1.html file2.html file3.html
```

Merge multiple files into a single output:
```bash
vokindle file1.html file2.html --merge
```

Translate vocabulary to a different language:
```bash
vokindle path/to/kindle.html --translate --target-lang fr
```

Extract only vocabulary:
```bash
vokindle path/to/kindle.html --vocab-only
```

Extract only quotes:
```bash
vokindle path/to/kindle.html --quotes-only
```

### Output Structure

The tool creates the following directory structure:

```
output/
├── stats/
│   └── bookname_stats.json
└── bookname/
    ├── vocabulary.txt
    └── quotes.txt
```

When merging multiple files:
```
output/
├── stats/
│   └── merged_book1_book2_stats.json
└── merged_book1_book2/
    ├── vocabulary.txt
    └── quotes.txt
```

### Python API

```python
from vokindle import Vokindle

# Initialize with single file
vokindle = Vokindle('path/to/kindle.html')

# Initialize with multiple files
vokindle = Vokindle(['file1.html', 'file2.html'])

# Initialize with custom target language
vokindle = Vokindle('path/to/kindle.html', target_lang='fr')

# Extract vocabulary
vocab = vokindle.extract_vocabulary()

# Extract quotes with metadata
quotes = vokindle.extract_quotes()

# Translate vocabulary
translated_vocab = vokindle.translate_vocabulary()

# Get statistics
stats = vokindle.stats

# Save outputs
vokindle.save_vocabulary('kindle.html', translate=True)
vokindle.save_quotes('kindle.html')
vokindle.save_stats('kindle.html')

# Merge with another instance
other_vokindle = Vokindle('another.html')
merged = vokindle.merge_with(other_vokindle)
```

## License

MIT License 
