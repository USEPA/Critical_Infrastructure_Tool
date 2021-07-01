import IParameter from '@/interfaces/parameter/IParameter';
import deepCopy from '@/utilities/deepCopy';
import ParameterType from '@/enums/parameter/parameterType';
import IParameterNode from '@/interfaces/parameter/IParameterNode';
import NullParameter from './NullParameter';

export default class ParameterWrapper implements IParameterNode {
  baseline: IParameter;

  current: IParameter;

  get type(): ParameterType {
    return this.current.type;
  }

  get name(): string {
    return this.current.metaData.name ?? 'unknown';
  }

  get path(): string {
    let path = this.name;
    let current = this.parent;
    while (current != null) {
      path = `${current.name} - ${path}`;
      current = current.parent;
    }
    return path;
  }

  parent: IParameterNode | null;

  isChanged(): boolean {
    if (!this.baseline.isEquivalent) {
      return false;
    }
    return !this.baseline.isEquivalent(this.current);
  }

  reset(): void {
    this.current = deepCopy(this.baseline);
  }

  constructor(parent: IParameterNode | null = null, param?: IParameter) {
    this.parent = parent;
    this.baseline = new NullParameter();
    if (param) {
      this.baseline = deepCopy(param);
    }
    this.current = deepCopy(this.baseline);
  }
}
