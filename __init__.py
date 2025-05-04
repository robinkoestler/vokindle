from bs4 import BeautifulSoup
from translate import Translator
from typing import List, Dict, Optional, Union
import os
from tqdm import tqdm
from datetime import datetime
import json
from collections import defaultdict
import re

class Vokindle:
    def __init__(self, html_files: Union[str, List[str]], target_lang: str = "de"):
        """
        Initialize Vokindle with Kindle HTML export file(s).
        
        Args:
            html_files: Path to the Kindle HTML export file or list of files
            target_lang: Target language for translation (default: German)
        """
        self.html_files = [html_files] if isinstance(html_files, str) else html_files
        self.target_lang = target_lang
        self._soup = None
        self._translator = None
        self._highlights = None
        self._stats = None
        
        # Create output directories
        self.output_dir = "output"
        self.stats_dir = os.path.join(self.output_dir, "stats")
        os.makedirs(self.stats_dir, exist_ok=True)
    
    def _clean_word(self, word: str) -> str:
        """Clean a word by removing punctuation and whitespace"""
        # Remove punctuation from start and end
        word = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', word)
        return word.strip().lower()
    
    @property
    def soup(self) -> List[BeautifulSoup]:
        """Lazy loading of BeautifulSoup objects"""
        if self._soup is None:
            self._soup = []
            for file in self.html_files:
                with open(file, 'r', encoding='utf-8') as f:
                    self._soup.append(BeautifulSoup(f, 'html.parser'))
        return self._soup
    
    @property
    def translator(self) -> Translator:
        """Lazy loading of Translator object"""
        if self._translator is None:
            self._translator = Translator(to_lang=self.target_lang, from_lang="en")
        return self._translator
    
    @property
    def highlights(self) -> List[Dict]:
        """Lazy loading of all highlights with metadata"""
        if self._highlights is None:
            self._highlights = []
            for soup in self.soup:
                note_headings = soup.find_all('div', class_='noteHeading')
                note_texts = soup.find_all('div', class_='noteText')
                
                for heading, text in zip(note_headings, note_texts):
                    # Extract location information
                    location_text = heading.get_text().strip()
                    location_match = re.search(r'Seite (\d+) · Position (\d+)', location_text)
                    
                    highlight = {
                        'text': text.get_text().strip(),
                        'page': int(location_match.group(1)) if location_match else 0,
                        'position': int(location_match.group(2)) if location_match else 0,
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }
                    self._highlights.append(highlight)
            
            # Sort highlights by page and position
            self._highlights.sort(key=lambda x: (x['page'], x['position']))
        
        return self._highlights
    
    @property
    def stats(self) -> Dict:
        """Calculate statistics about the highlights"""
        if self._stats is None:
            self._stats = {
                'total_highlights': len(self.highlights),
                'vocabulary_words': len(self.extract_vocabulary()),
                'quotes': len(self.extract_quotes()),
                'pages_covered': len(set(h['page'] for h in self.highlights)),
                'highlight_dates': defaultdict(int),
                'word_frequency': defaultdict(int)
            }
            
            # Calculate word frequency
            for highlight in self.highlights:
                words = highlight['text'].lower().split()
                for word in words:
                    cleaned_word = self._clean_word(word)
                    if len(cleaned_word) > 1:  # Ignore single characters
                        self._stats['word_frequency'][cleaned_word] += 1
            
            # Sort word frequency
            self._stats['word_frequency'] = dict(
                sorted(self._stats['word_frequency'].items(), 
                      key=lambda x: x[1], reverse=True)
            )
        
        return self._stats
    
    def extract_vocabulary(self) -> List[str]:
        """Extract single-word highlights as vocabulary"""
        vocabulary = set()
        for highlight in self.highlights:
            text = highlight['text']
            if len(text.split()) == 1:  # Single word
                word = self._clean_word(text)
                if word:  # Only add if word is not empty after cleaning
                    vocabulary.add(word)
        
        return sorted(list(vocabulary))
    
    def extract_quotes(self) -> List[Dict]:
        """Extract multi-word highlights as quotes with metadata"""
        quotes = []
        for highlight in self.highlights:
            text = highlight['text']
            if len(text.split()) > 1:  # Multiple words
                quotes.append(highlight)
        
        return quotes
    
    def translate_vocabulary(self) -> Dict[str, str]:
        """Translate vocabulary to target language"""
        vocabulary = self.extract_vocabulary()
        translations = {}
        
        for word in tqdm(vocabulary, desc="Translating vocabulary"):
            try:
                translation = self.translator.translate(word)
                translations[word] = translation
            except Exception as e:
                translations[word] = f"Translation error: {str(e)}"
        
        return translations
    
    def _get_output_dir(self, html_file: str) -> str:
        """Get the output directory for a specific HTML file"""
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        output_dir = os.path.join(self.output_dir, base_name)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def save_vocabulary(self, html_file: str, translate: bool = False):
        """Save vocabulary to a file"""
        output_dir = self._get_output_dir(html_file)
        output_file = os.path.join(output_dir, "vocabulary.txt")
        
        if translate:
            translations = self.translate_vocabulary()
            with open(output_file, 'w', encoding='utf-8') as f:
                for word, translation in translations.items():
                    f.write(f"{word} - {translation}\n")
        else:
            vocabulary = self.extract_vocabulary()
            with open(output_file, 'w', encoding='utf-8') as f:
                for word in vocabulary:
                    f.write(f"{word}\n")
    
    def save_quotes(self, html_file: str):
        """Save quotes to a file with metadata"""
        output_dir = self._get_output_dir(html_file)
        output_file = os.path.join(output_dir, "quotes.txt")
        
        quotes = self.extract_quotes()
        with open(output_file, 'w', encoding='utf-8') as f:
            for quote in quotes:
                f.write(f"Page {quote['page']}, Position {quote['position']}:\n")
                f.write(f"{quote['text']}\n\n")
    
    def save_stats(self, html_file: str):
        """Save statistics to a JSON file"""
        base_name = os.path.splitext(os.path.basename(html_file))[0]
        output_file = os.path.join(self.stats_dir, f"{base_name}_stats.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
    
    def merge_with(self, other: 'Vokindle') -> 'Vokindle':
        """Merge this instance with another Vokindle instance"""
        merged_files = self.html_files + other.html_files
        merged = Vokindle(merged_files, self.target_lang)
        return merged 