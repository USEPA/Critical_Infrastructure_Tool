import { expect } from 'chai';
import DefaultNavigationItemProvider from '@/implementations/providers/DefaultNavigationItemProvider';

describe('DefaultNavigationItemProvider', function TestDefaultNavigationItemProvider() {
  it('should contain three items', () => {
    // Setup
    const provider = new DefaultNavigationItemProvider();

    // SUT
    const items = provider.getNavigationItems();

    // Assert
    expect(items.length).equal(3);
  });
});
