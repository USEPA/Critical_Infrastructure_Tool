import { expect } from 'chai';
// eslint-disable-next-line @typescript-eslint/no-unused-vars,import/named
import { nelderMead } from '@/mixin/solverMixin';
import Weibull from '@/implementations/parameter/distribution/Weibull';
import ParameterMetaData from '@/implementations/parameter/ParameterMetaData';

describe('SolverFunctionality', function TestDefaultNavigationItemProvider() {
  it('Correct Fit to Weibull', () => {
    // Setup
    const expected = new Weibull(new ParameterMetaData(), 1.79, 1.2);

    const minimize = (values: number[]): number => {
      const actual = new Weibull(new ParameterMetaData(), values[0], values[1]);

      if (!!actual.mean && !!actual.variance && !!expected.mean && !!expected.variance) {
        return Math.sqrt((actual.mean - expected.mean) ** 2 + (actual.variance - expected.variance) ** 2);
      }
      return Infinity;
    };
    const guess = [1, 1];

    // SUT
    const sln = nelderMead(minimize, guess);
    const actual = new Weibull(new ParameterMetaData(), sln.Input[0], sln.Input[1]);
    if (!(!!actual.lambda && !!actual.k && !!expected.lambda && !!expected.k)) {
      expect.fail('Incorrect setup of weibull');
    }

    // Assert
    expect(Math.abs(expected.lambda - actual.lambda)).lessThan(1e-3);
    expect(Math.abs(expected.k - actual.k)).lessThan(1e-3);
  });
});
