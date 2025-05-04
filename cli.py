import argparse
import sys
from . import Vokindle
from tqdm import tqdm
import os

def main():
    parser = argparse.ArgumentParser(
        description="Extract vocabulary and quotes from Kindle HTML exports"
    )
    parser.add_argument(
        "html_files",
        nargs="+",
        help="Path(s) to the Kindle HTML export file(s)"
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate vocabulary to target language"
    )
    parser.add_argument(
        "--target-lang",
        default="de",
        help="Target language for translation (default: de)"
    )
    parser.add_argument(
        "--vocab-only",
        action="store_true",
        help="Extract only vocabulary"
    )
    parser.add_argument(
        "--quotes-only",
        action="store_true",
        help="Extract only quotes"
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge multiple Kindle exports into a single output"
    )
    
    args = parser.parse_args()
    
    try:
        if args.merge:
            # Create a single Vokindle instance with all files
            vokindle = Vokindle(args.html_files, target_lang=args.target_lang)
            
            # Create a merged output directory
            merged_name = "merged_" + "_".join(
                os.path.splitext(os.path.basename(f))[0] for f in args.html_files
            )
            merged_dir = os.path.join("output", merged_name)
            os.makedirs(merged_dir, exist_ok=True)
            
            if not args.quotes_only:
                vokindle.save_vocabulary(args.html_files[0], translate=args.translate)
                print(f"Vocabulary saved to {merged_dir}/vocabulary.txt")
            
            if not args.vocab_only:
                vokindle.save_quotes(args.html_files[0])
                print(f"Quotes saved to {merged_dir}/quotes.txt")
            
            vokindle.save_stats(args.html_files[0])
            print(f"Statistics saved to output/stats/{merged_name}_stats.json")
            
            # Print summary statistics
            stats = vokindle.stats
            print("\nSummary Statistics:")
            print(f"Total highlights: {stats['total_highlights']}")
            print(f"Vocabulary words: {stats['vocabulary_words']}")
            print(f"Quotes: {stats['quotes']}")
            print(f"Pages covered: {stats['pages_covered']}")
            print("\nTop 10 most frequent words:")
            for word, count in list(stats['word_frequency'].items())[:10]:
                print(f"{word}: {count}")
            
        else:
            # Process each file separately
            for html_file in tqdm(args.html_files, desc="Processing files"):
                vokindle = Vokindle(html_file, target_lang=args.target_lang)
                
                if not args.quotes_only:
                    vokindle.save_vocabulary(html_file, translate=args.translate)
                    print(f"Vocabulary saved to output/{os.path.splitext(os.path.basename(html_file))[0]}/vocabulary.txt")
                
                if not args.vocab_only:
                    vokindle.save_quotes(html_file)
                    print(f"Quotes saved to output/{os.path.splitext(os.path.basename(html_file))[0]}/quotes.txt")
                
                vokindle.save_stats(html_file)
                print(f"Statistics saved to output/stats/{os.path.splitext(os.path.basename(html_file))[0]}_stats.json")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 