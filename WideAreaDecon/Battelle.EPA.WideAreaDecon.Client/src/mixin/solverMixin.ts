/* eslint-disable max-classes-per-file */

function weightedSum(w1: number, v1: number[], w2: number, v2: number[]): number[] {
  const ret = new Array<number>(v1.length);
  for (let j = 0; j < ret.length; j += 1) {
    ret[j] = w1 * v1[j] + w2 * v2[j];
  }
  return ret;
}

export class Simplex {
  Id: number;

  Input: number[];

  Output: number;

  constructor(id: number, input: number[], output: number) {
    this.Id = id;
    this.Input = input;
    this.Output = output;
  }
}

export class Parameters {
  maxIterations = 400;

  nonZeroDelta = 1.05;

  zeroDelta = 0.001;

  minErrorDelta = 1e-6;

  minTolerance = 1e-5;

  rho = 1;

  chi = 2;

  psi = -0.5;

  sigma = 0.5;

  history?: Simplex[];
}

/** minimizes a function using the downhill simplex method */
// eslint-disable-next-line import/prefer-default-export, @typescript-eslint/explicit-module-boundary-types,@typescript-eslint/no-explicit-any
export function nelderMead(f: (guess: number[]) => number, x0: number[], parameters?: Parameters): Simplex {
  // eslint-disable-next-line no-param-reassign
  parameters = parameters || new Parameters();
  let maxDiff;

  // initialize simplex.
  const N = x0.length;
  const simplex = new Array<Simplex>();
  simplex.push(new Simplex(0, x0, f(x0)));
  for (let i = 0; i < N; i += 1) {
    const point = x0.slice();
    point[i] = point[i] ? point[i] * parameters.nonZeroDelta : parameters.zeroDelta;
    simplex.push(new Simplex(i + 1, point, f(point)));
  }

  function updateSimplex(value: Simplex) {
    simplex[N] = value;
  }

  const sortOrder = (a: Simplex, b: Simplex): number => {
    return a.Output - b.Output;
  };

  const centroid = x0.slice();

  for (let iteration = 0; iteration < parameters.maxIterations; iteration += 1) {
    simplex.sort(sortOrder);

    maxDiff = 0;
    for (let i = 0; i < N; i += 1) {
      maxDiff = Math.max(maxDiff, Math.abs(simplex[0].Input[i] - simplex[1].Input[i]));
    }

    if (
      Math.abs(simplex[0].Output - simplex[N].Output) < parameters.minErrorDelta &&
      maxDiff < parameters.minTolerance
    ) {
      break;
    }

    // compute the centroid of all but the worst point in the simplex
    for (let i = 0; i < N; i += 1) {
      centroid[i] = 0;
      for (let j = 0; j < N; j += 1) {
        centroid[i] += simplex[j].Input[i];
      }
      centroid[i] /= N;
    }

    // reflect the worst point past the centroid  and compute loss at reflected
    // point
    const worst = simplex[N];
    let sum = weightedSum(1 + parameters.rho, centroid, -parameters.rho, worst.Input);
    const reflected = new Simplex(worst.Id, sum, f(sum));

    // if the reflected point is the best seen, then possibly expand
    if (reflected.Output < simplex[0].Output) {
      sum = weightedSum(1 + parameters.chi, centroid, -parameters.chi, worst.Input);
      const expanded = new Simplex(worst.Id, sum, f(sum));
      if (expanded.Output < reflected.Output) {
        updateSimplex(expanded);
      } else {
        updateSimplex(reflected);
      }
    }

    // if the reflected point is worse than the second worst, we need to
    // contract
    else if (reflected.Output >= simplex[N - 1].Output) {
      let shouldReduce = false;

      if (reflected.Output > worst.Output) {
        // do an inside contraction
        sum = weightedSum(1 + parameters.psi, centroid, -parameters.psi, worst.Input);
        const contracted = new Simplex(worst.Id, sum, f(sum));
        if (contracted.Output < worst.Output) {
          updateSimplex(contracted);
        } else {
          shouldReduce = true;
        }
      } else {
        // do an outside contraction
        sum = weightedSum(1 - parameters.psi * parameters.rho, centroid, parameters.psi * parameters.rho, worst.Input);
        const contracted = new Simplex(worst.Id, sum, f(sum));
        if (contracted.Output < reflected.Output) {
          updateSimplex(contracted);
        } else {
          shouldReduce = true;
        }
      }

      if (shouldReduce) {
        // if we don't contract here, we're done
        if (parameters.sigma >= 1) break;

        // do a reduction
        for (let i = 1; i < simplex.length; i += 1) {
          simplex[i].Input = weightedSum(1 - parameters.sigma, simplex[0].Input, parameters.sigma, simplex[i].Input);
          simplex[i].Output = f(simplex[i].Input);
        }
      }
    } else {
      updateSimplex(reflected);
    }
  }

  simplex.sort(sortOrder);
  return new Simplex(0, simplex[0].Input, simplex[0].Output);
}
