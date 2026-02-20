import axios from 'axios';
import type {
  GameRunRequest,
  GameRunResponse,
  MonteCarloCompareRequest,
  MonteCarloCompareResponse,
  StrategiesResponse,
  VisualizationRequest,
  VisualizationResponse,
} from './types';

const api = axios.create({ baseURL: '/api' });

export const getStrategies = () =>
  api.get<StrategiesResponse>('/visualization/strategies');

export const runGame = (req: GameRunRequest) =>
  api.post<GameRunResponse>('/game/run', req);

export const compareStrategies = (req: MonteCarloCompareRequest) =>
  api.post<MonteCarloCompareResponse>('/monte-carlo/compare', req);

export const getVisualizationPaths = (req: VisualizationRequest) =>
  api.post<VisualizationResponse>('/visualization/monte-carlo-paths', req);
