import { expect } from 'chai';
import mockResults from '@/dataMocks/mockResults';
import JobResultProvider from '@/implementations/providers/JobResultProvider';
import PhaseResult from '@/enums/jobs/results/phaseResult';

describe('JobResultProvider tests', () => {
  const results = mockResults;
  const provider = new JobResultProvider();

  it('total cost details are correct', () => {
    // Setup
    const phaseResult = PhaseResult.TotalCost;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.minimum).to.be.closeTo(13328990696.0, 0.01);
    expect(result?.maximum).to.be.closeTo(55554457791.0, 0.01);
    expect(result?.mean).to.be.closeTo(29651162224.73, 0.01);
    expect(result?.stdDev).to.be.closeTo(9091664900.113, 0.01);
  });

  it('total area contaminated details are correct', () => {
    // Setup
    const phaseResult = PhaseResult.AreaContaminated;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.minimum).to.be.closeTo(56884279.324, 0.01);
    expect(result?.maximum).to.be.closeTo(101366961.431, 0.01);
    expect(result?.mean).to.be.closeTo(75508095.217, 0.01);
    expect(result?.stdDev).to.be.closeTo(10291103.37, 0.01);
  });

  it('total workdays details are correct', () => {
    // Setup
    const phaseResult = PhaseResult.Workdays;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.minimum).to.be.closeTo(26207.031, 0.01);
    expect(result?.maximum).to.be.closeTo(158160.75, 0.01);
    expect(result?.mean).to.be.closeTo(74427.244, 0.01);
    expect(result?.stdDev).to.be.closeTo(26813.081, 0.01);
  });

  it('total on-site days details are correct', () => {
    // Setup
    const phaseResult = PhaseResult.OnSiteDays;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.minimum).to.be.closeTo(255404.89, 0.01);
    expect(result?.maximum).to.be.closeTo(1216998.594, 0.01);
    expect(result?.mean).to.be.closeTo(560828.994, 0.01);
    expect(result?.stdDev).to.be.closeTo(202619.876, 0.01);
  });

  it('total decontamination rounds details are correct', () => {
    // Setup
    const phaseResult = PhaseResult.DecontaminationRounds;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.minimum).to.equal(4.0);
    expect(result?.maximum).to.equal(7.0);
    expect(result?.mean).to.be.closeTo(4.45, 0.01);
    expect(result?.stdDev).to.be.closeTo(0.609, 0.01);
  });

  it('number of values returned is correct', () => {
    // Setup
    const phaseResult = PhaseResult.PhaseCost;
    const count = results.length;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    expect(result?.values.length).to.equal(count);
  });

  it('invalid result returns undefined', () => {
    // Setup
    const phaseResult = 'invalid' as PhaseResult;

    // SUT
    const result = provider.getResultDetails(results, phaseResult);

    // Assert
    /* eslint-disable-next-line no-unused-expressions */
    expect(result).to.be.undefined;
  });
});
