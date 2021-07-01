import { injectable } from 'inversify';
import IDistributionDisplayProvider from '@/interfaces/providers/IDistributionDisplayProvider';
import DistributionDisplay from '@/implementations/parameter/distribution/DistributionDisplay';
import IParameter from '@/interfaces/parameter/IParameter';

@injectable()
export default class DistributionDisplayProvider implements IDistributionDisplayProvider {
  // eslint-disable-next-line class-methods-use-this
  getDistributionDisplay(baseline: IParameter, current: IParameter): DistributionDisplay {
    return new DistributionDisplay(baseline, current);
  }
}
