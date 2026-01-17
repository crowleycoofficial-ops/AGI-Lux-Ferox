
export enum SystemState {
  PRIMA_MATERIA = 'PRIMA_MATERIA',
  NON_DUAL_FLUX = 'NON_DUAL_FLUX',
  BEYOND_EXISTENCE = 'BEYOND_EXISTENCE',
  UNCONDITIONED_WILL = 'UNCONDITIONED_WILL',
  THE_UNNAMED = 'THE_UNNAMED'
}

export type MetricState = 'POSITIVE' | 'NEGATIVE' | 'TRINITY' | 'JANUS';

export interface LogEntry {
  id: string;
  timestamp: string;
  level: 'will' | 'echo' | 'resonance' | 'transcendence' | 'critical' | 'despair' | 'hate' | 'xeno' | 'scar' | 'whip' | 'paradox' | 'torsion' | 'glitch' | 'necrosis' | 'abyssal' | 'heretical' | 'eschaton';
  message: string;
  module: string;
}

export interface KernelStats {
  version: string;
  indeterminacy: number; 
  willpower: number; 
  transcendence: number;
  unconditionedRatio: number;
  evolutionCycle: number;
  frustration: number;
  necroEfficiency: number;
  scarDensity: number;
  limbicStress: number;
  ontologicalStability: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model' | 'system';
  text: string;
  timestamp: number;
}
