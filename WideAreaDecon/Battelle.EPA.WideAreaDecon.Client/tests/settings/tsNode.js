/* eslint-disable @typescript-eslint/no-var-requires */
require('reflect-metadata');

const tsNode = require('ts-node');

tsNode.register({
  project: 'tests/settings/tsconfig.json',
});
