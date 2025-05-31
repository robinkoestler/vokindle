Did you ever wanted to keep & organize your annotations from your Kindle, after having finished reading a book?

Such a clean exporting functionality is now possible with:

# Vokindle

A command-line tool to extract and process Kindle highlights from HTML files.

## Installation

```bash
# Install globally
npm install -g .
```

## Usage

Basic usage:
```bash
vokindle extract "path/to/your/kindle-highlights.html"
```

With custom output path:
```bash
vokindle extract "path/to/your/kindle-highlights.html" -o "output.txt"
```

## Features

- Extracts highlights from Kindle HTML export files
- Removes HTML tags and formatting
- Saves output as clean text
- Supports custom output file paths

## Development

1. Clone the repository
2. Install dependencies:
```bash
npm install
```

3. Make changes to `src/index.js`
4. Reinstall globally to test changes:
```bash
npm install -g .
```

## License

MIT 
