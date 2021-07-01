const g = 7;
const C = [
  0.99999999999980993,
  676.5203681218851,
  -1259.1392167224028,
  771.32342877765313,
  -176.61502916214059,
  12.507343278686905,
  -0.13857109526572012,
  9.9843695780195716e-6,
  1.5056327351493116e-7,
];

function gamma(z: number): number {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
  // eslint-disable-next-line no-param-reassign
  z -= 1;

  let x = C[0];
  for (let i = 1; i < g + 2; i += 1) x += C[i] / (z + i);

  const t = z + g + 0.5;
  return Math.sqrt(2 * Math.PI) * (t ** z + 0.5) * Math.exp(-t) * x;
}

function convertToLog10(value?: number): number | undefined {
  return value && value > 0 ? Math.log10(value) : undefined;
}

function convertToLog(value?: number): number | undefined {
  return value && value > 0 ? Math.log(value) : undefined;
}

// eslint-disable-next-line import/prefer-default-export
export { gamma, convertToLog10, convertToLog };
