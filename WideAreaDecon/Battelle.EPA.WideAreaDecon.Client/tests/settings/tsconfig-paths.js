/* eslint-disable @typescript-eslint/no-var-requires */
const fs = require('fs');
const path = require('path');
const json = require('comment-json');

const tsConfigPaths = require('tsconfig-paths');

const testDirectory = path.resolve('tests/settings'); // from cwd
const jsonConfigPath = path.resolve(testDirectory, 'tsconfig.json');

const tsConfig = json.parse(fs.readFileSync(jsonConfigPath).toString());

const baseUrl = path.resolve(testDirectory, tsConfig.compilerOptions.baseUrl);

tsConfigPaths.register({
  baseUrl, // ./src/
  paths: { ...(tsConfig.compilerOptions.paths || {}) },
});
