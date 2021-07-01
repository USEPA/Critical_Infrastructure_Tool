import { expect } from 'chai';
import DefaultClientConfigurationProvider from '@/implementations/providers/DefaultClientConfigurationProvider';

describe('DefaultClientConfigurationProvider', function TestDefaultClientConfigurationProvider() {
  it('should have defaults of', async () => {
    // Setup
    const provider = new DefaultClientConfigurationProvider();
    const defaultValue = 'unknown';

    // SUT
    const configuration = await provider.getClientConfigurationAsync();

    // Assert
    expect(configuration.theme).to.deep.equal({});
    expect(configuration.applicationTitle).to.equal(defaultValue);
    expect(configuration.applicationVersion).to.equal(defaultValue);
    expect(configuration.publisherName).to.equal(defaultValue);
  });
});
