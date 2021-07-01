import IImageProvider from '@/interfaces/providers/IImageProvider';
import { injectable } from 'inversify';
import assets from '@/assets/assets';

@injectable()
export default class DefaultImageProvider implements IImageProvider {
  assetsDirectory = '@/assets/';

  // eslint-disable-next-line class-methods-use-this
  getImage(name: string): unknown {
    return assets[name];
  }
}
