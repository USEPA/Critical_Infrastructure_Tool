import { Container } from 'inversify';
import 'reflect-metadata';
import providersContainer from './providers/providers.config';
import convertersContainer from './converters/converters.config';

const container = new Container();

container.load(providersContainer);
container.load(convertersContainer);

export default container;
