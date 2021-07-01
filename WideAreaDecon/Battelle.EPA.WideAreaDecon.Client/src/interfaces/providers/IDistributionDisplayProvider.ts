import DistributionDisplay from '@/implementations/parameter/distribution/DistributionDisplay';
import IParameter from '../parameter/IParameter';

export default interface IChartProvider {
  getDistributionDisplay(baseline: IParameter, current: IParameter): DistributionDisplay;
}
