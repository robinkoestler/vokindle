#!/usr/bin/env node

const { program } = require('commander');
const path = require('path');
const fs = require('fs');

program
  .name('vokindle')
  .description('Extract and process Kindle highlights')
  .version('1.0.0');

program
  .command('extract')
  .description('Extract highlights from Kindle file')
  .argument('<file>', 'Path to the Kindle highlights file')
  .option('-o, --output <file>', 'Output file path (default: <input-file>.txt)')
  .action((file, options) => {
    try {
      // Read the input file
      const content = fs.readFileSync(file, 'utf8');
      
      // Extract highlights (basic implementation - you might want to enhance this)
      const highlights = extractHighlights(content);
      
      // Determine output file path
      const outputPath = options.output || file.replace(/\.html$/, '.txt');
      
      // Write the output
      fs.writeFileSync(outputPath, highlights.join('\n\n'));
      
      console.log(`Successfully processed ${file}`);
      console.log(`Output saved to: ${outputPath}`);
    } catch (error) {
      console.error('Error processing file:', error.message);
      process.exit(1);
    }
  });

function extractHighlights(content) {
  // Basic implementation - extracts text between highlight markers
  // You might want to enhance this based on your specific HTML structure
  const highlights = [];
  const regex = /<div class="noteText">(.*?)<\/div>/gs;
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    const highlight = match[1]
      .replace(/<[^>]*>/g, '') // Remove HTML tags
      .trim();
    if (highlight) {
      highlights.push(highlight);
    }
  }
  
  return highlights;
}

program.parse(); 