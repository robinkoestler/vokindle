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
  .action((file) => {
    // TODO: Implement the extraction logic
    console.log(`Processing file: ${file}`);
  });

program.parse(); 