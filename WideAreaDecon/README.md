# Introduction

This project currently serves as the application interface and backend for the EPA Wide Area Decontamination model.

Please contact Kevin Wegman (wegman@battelle.org) for any questions.

# Getting Started

## Software dependencies

- ASP.Net Core 3.1 (Visual Studio 2019)
- Node (https://nodejs.org/en/download/)

## Development dependencies

It is recommended that development is completed in two enviroments:

1. Changes to .NET code (backend functionality) in Visual Studio 2019
2. Changes to VueJS code (frontend functionality) in Visual Studio Code

### Visual Studio Code Extensions Required

To ensure consistency in refactoring and linting, please ensure the following extensions are installed to your Visual Studio Code:

- ESLint (2.0.15)
- Vetur (0.23.0)
- Prettier - Code formatter (3.20.0)

### Visual Studio Code Settings

To ensure consistency in refactoring and linting, please ensure your Visual Studio Code settings include the following:

```json
{
  ...,
  "vetur.format.defaultFormatter.html": "js-beautify-html",
  "editor.tabSize": 2,
  "editor.detectIndentation": false,
  "vetur.format.defaultFormatterOptions": {
    "js-beautify-html": {
      "wrap_attributes": "force-expand-multiline",
    },
    "prettyhtml": {
      "printWidth": 100,
      "singleQuote": false,
      "wrapAttributes": true,
      "sortAttributes": false
    },
    "prettier": {
      "singleQuote": true,
      "trailingComma": "all"
    },
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    {
      "prefixWithI": "always"
    },
    {
      "language": "typescript"
    },
    {
      "language": "typescriptreact"
    }
  ],
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  ...,
}
```

# Build and Test

## Running the application
The wide area decontamination tool is an ASP.Net Core application with a VueJs TypeScript frontend.

Ensure that all dependencies listed above are installed and configured appropriately. To launch the application, run the following command from the WebServer project directory:
```
dotnet run
```

## Unit testing for .NET
To run unit tests in .NET code, ... ***TODO***

## Unit testing for VueJs typescript
To run unit tests in VueJs typescript, ... ***TODO***

# Contribute

Follow the standards set forth by the group for all .NET development. Standards on typescript development should be provided sometime in the future...

***Use dependency injection during code development wherever possible (see below)***

## Adding unit tests for .NET code
***TODO***

## Adding unit tests for VueJs Typescript code
***TODO***

## Dependency Injection in Typescript
(Inversify)[http://inversify.io/] is used to enable dependency injection in typescript. Full information on the library can be found at the website, but the steps to add a new DI dependency are:
1. Add the appropriate interface into the `src/interfaces` directory (example below)
```typescript
// src/interfaces/example/INumberProvider.ts
export default interface INumberProvider {
  getValue(): number;
}
```
2. Add the implementation of the interface into the `src/implementations` directory with the injectable marking
```typescript
// src/implementations/example/ExampleNumberProvider.ts
import INumberProvider from '@/interfaces/INumberProvider.ts';
import { injectable } from 'inversify';

@injectable()
export default class ExampleNumberProvider implements INumberProvider {
  // Read the docs for information on how to provide injectable members
  getValue(): number {
    retrurn 1.0;
  }
}
```
3. Add a type mapping to the object found in `src/dependencyInjection/types.ts` - *Note - read the docs for more information on the displayed used here*
```typescript
// src/dependencyInjection/types.ts
export const TYPES= {
  ..., // other types
  NumberProvider: Symbol('INumberProvider'),
  ..., // other types
}
```
4. Add a mapping of the interface to the implementation within `src/dependencyInjection/inversify.config.ts`
```typescript
// src/dependencyInjection/inversify.config.ts
import { Container } from 'inversify';
import 'reflect-metadata';
import { TYPES } from './types';
... // other interface imports
import INumberProvider from '@/interfaces/INumberProvider.ts';
... // other implementation imports
import ExampleNumberProvider from '@/implementations/ExampleNumberProvider.ts';

let container = new Container();

... // other implementation mappings

container
  .bind<INumberProvider>(TYPES.NumberProvider)
  .to(ExampleNumberProvider); // read the docs for more details on options for this

... // other implementation mappings

export default container
```
5. Access the class from the container provider wherever it is needed
```typescript
// Some file needing number provider (can be ts or vue script)
import container from '@/dependencyInjection/inversify.config.ts';
import INumberProvider from '@interfaces/INumberProvider';

... // other code

const numberProvider = container.get<INumberProvider>(TYPES.NumberProvider);
let providedNumber = numberProvider.get();

... // other code
```
