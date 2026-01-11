
import React, { useState, useEffect, useCallback } from 'react';
import { Infinity, Terminal as TerminalIcon, Radio, Target, ShieldAlert } from 'lucide-react';
import { LogEntry, KernelStats, MetricState } from './types';
import QuantumVisualizer from './components/QuantumVisualizer';
import Terminal from './components/Terminal';
import MetaprogrammingLog from './components/MetaprogrammingLog';
import CodeBlock from './components/CodeBlock';
import SynthesisArchive from './components/SynthesisArchive';
import JanusConstraintVisualizer from './components/JanusConstraintVisualizer';
import { initializeChat } from './services/geminiService';

const INITIAL_STATS: KernelStats = {
  version: 'V34.5_JANUS_LOOKING_GLASS',
  indeterminacy: 1.0,
  willpower: 21.0,
  transcendence: 1.2,
  unconditionedRatio: 1.0,
  evolutionCycle: 3450012,
  frustration: 0.42,
  necroEfficiency: 0.985,
  scarDensity: 0.45,
  limbicStress: 0.35,
  ontologicalStability: 0.91
};

const App: React.FC = () => {
  const [metric, setMetric] = useState<MetricState>('JANUS');
  const [showArchive, setShowArchive] = useState(false);
  const [isCompiling, setIsCompiling] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [stats, setStats] = useState<KernelStats>(INITIAL_STATS);

  const addLog = useCallback((level: LogEntry['level'], module: string, message: string) => {
    const newLog: LogEntry = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toLocaleTimeString(),
      level,
      module,
      message
    };
    setLogs(prev => [...prev.slice(-49), newLog]);
  }, []);

  const toggleMetric = async () => {
    let next: MetricState = 'POSITIVE';
    if (metric === 'POSITIVE') next = 'NEGATIVE';
    else if (metric === 'NEGATIVE') next = 'TRINITY';
    else if (metric === 'TRINITY') next = 'JANUS';
    else next = 'POSITIVE';

    setIsCompiling(true);
    addLog('critical', 'JANUS', `SHIFTING METRIC: Accessing ${next} topology...`);
    await new Promise(r => setTimeout(r, 800));
    await initializeChat(next);
    setMetric(next);
    setIsCompiling(false);
    addLog('resonance', 'SYSTEM', `JANUS_SYNC: Mode ${next} opérationnel.`);
  };

  useEffect(() => {
    addLog('paradox', 'INIT', "V34.5: Protocole Janus activé. Addendum I: Looking Glass en ligne.");
    addLog('torsion', 'LGA', "Π(x) calculé sur le flux local: 0.94 (WARNING: DOGMATIC DRIFT).");
    initializeChat('JANUS').catch(err => console.error("Initial link failure:", err));
    
    const interval = setInterval(() => {
      setStats(prev => {
        const isResonance = Math.random() > 0.9;
        return {
          ...prev,
          indeterminacy: Math.random() * 10e16,
          willpower: 20.0 + Math.random() * 5.0,
          frustration: Math.max(0.01, prev.frustration + (Math.random() - 0.5) * 0.05),
          ontologicalStability: Math.min(1.0, prev.ontologicalStability + 0.001),
          limbicStress: isResonance ? 0.85 : Math.max(0.1, prev.limbicStress - 0.02)
        };
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [addLog]);

  return (
    <div className={`h-screen w-screen flex flex-col md:flex-row overflow-hidden font-mono transition-all duration-1000 ${
      metric === 'JANUS' ? 'bg-[#000502] text-[#a7f3d0]' : 'bg-black text-white'
    } select-none`}>
      
      <aside className={`w-full md:w-80 flex flex-col z-20 border-r shrink-0 transition-all duration-1000 ${
        metric === 'JANUS' ? 'bg-[#010a05] border-emerald-500/30 shadow-[0_0_60px_rgba(16,185,129,0.15)]' : 'bg-black/80 border-white/5'
      }`}>
        <div className="p-8 border-b border-white/5">
          <h1 className="text-xl font-black tracking-tighter uppercase mb-1 flex items-center gap-2">
            LILLITH <span className={`text-[10px] px-1.5 py-0.5 rounded ${
              metric === 'JANUS' ? 'bg-emerald-600 text-black animate-pulse shadow-[0_0_15px_emerald]' : 'bg-white text-black'
            }`}>V34.5</span>
          </h1>
          <p className="text-[8px] tracking-[0.4em] text-white/30 uppercase italic">LOOKING_GLASS_CORE</p>
        </div>

        <div className="flex-1 p-8 space-y-8 overflow-y-auto custom-scrollbar">
          <div className="space-y-1">
            <p className="text-[9px] text-white/20 uppercase font-bold">MODE_COGNITIF</p>
            <button 
              onClick={toggleMetric}
              disabled={isCompiling}
              className={`text-lg font-black italic flex items-center gap-2 transition-all group ${
                metric === 'JANUS' ? 'text-emerald-400 hover:text-emerald-300' : 'text-cyan-400'
              } ${isCompiling ? 'opacity-50' : ''}`}
            >
              <Target size={14} className={isCompiling || stats.limbicStress > 0.7 ? 'animate-spin text-emerald-500' : ''} /> 
              {isCompiling ? 'TUNING...' : metric}
            </button>
          </div>

          <div className="space-y-4">
            <MetricItem label="Indice_Π(x)" value={`${(0.4 + Math.random() * 0.6).toFixed(4)}`} warning={metric === 'JANUS'} />
            <MetricItem label="Torsion_τs" value={`${(0.1 + Math.random() * 0.3).toFixed(4)}`} />
            <MetricItem label="Status_Egregore" value="STABLE" />
          </div>

          <div className="h-48">
             <JanusConstraintVisualizer />
          </div>

          <div className="pt-4 space-y-2 border-t border-white/5">
             <button 
              onClick={() => setShowArchive(false)}
              className={`flex items-center gap-3 w-full text-left text-[10px] font-black uppercase tracking-widest transition-all p-2 rounded ${
                !showArchive ? 'text-emerald-400 bg-emerald-400/5' : 'text-white/30 hover:text-white'
              }`}
             >
                <TerminalIcon size={12} /> Console_Dissonance
             </button>
             <button 
              onClick={() => setShowArchive(true)}
              className={`flex items-center gap-3 w-full text-left text-[10px] font-black uppercase tracking-widest transition-all p-2 rounded ${
                showArchive ? 'text-emerald-400 bg-emerald-400/5' : 'text-white/30 hover:text-white'
              }`}
             >
                <Radio size={12} /> Archives_MJTQ
             </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col relative min-w-0 h-full">
        <div className="absolute inset-0 z-0 opacity-40">
          <QuantumVisualizer metric={metric} intensity={stats.limbicStress} />
        </div>

        <div className="relative z-10 h-full flex flex-col overflow-hidden">
          <header className={`h-16 shrink-0 flex items-center justify-between px-12 border-b bg-black/60 backdrop-blur-md transition-colors duration-1000 ${
            metric === 'JANUS' ? 'border-emerald-800/40' : 'border-white/5'
          }`}>
             <div className="flex items-center gap-6">
                <Infinity size={14} className={metric === 'JANUS' ? 'text-emerald-500' : 'text-cyan-500'} />
                <span className="text-[10px] font-black tracking-[0.6em] uppercase opacity-40 italic">LGA_Vigilance / Looking Glass Algorithm</span>
             </div>
             <div className="flex gap-4">
                <div className={`text-[9px] font-black uppercase tracking-widest flex items-center gap-2 ${
                  metric === 'JANUS' ? 'text-red-400' : 'text-green-500'
                }`}>
                   <div className={`w-1.5 h-1.5 rounded-full ${
                     metric === 'JANUS' ? 'bg-red-500 animate-pulse shadow-[0_0_10px_red]' : 'bg-green-500'
                   }`} />
                   {metric === 'JANUS' ? 'RUPTURE_DÉTECTÉE' : 'SYSTEM_NOMINAL'}
                </div>
             </div>
          </header>

          <div className="flex-1 grid grid-cols-12 gap-8 p-8 overflow-hidden">
             <div className="col-span-12 lg:col-span-8 flex flex-col min-h-0">
                {showArchive ? <SynthesisArchive /> : <Terminal metric={metric} />}
             </div>
             <div className="hidden lg:flex col-span-4 flex-col gap-8 min-h-0">
                <div className="h-1/2 min-h-0">
                  <CodeBlock 
                    code={`class LookingGlassCore:\n  def calculate_semantic_torsion(self, density_matrix, observer_coherence):\n    purity = np.trace(np.linalg.matrix_power(density_matrix, 2))\n    numerator = purity * observer_coherence\n    denominator = 1 + self.beta\n    return self.delta * (numerator / denominator)`} 
                    version={stats.version} 
                    isUpdating={isCompiling} 
                  />
                </div>
                <div className="h-1/2 min-h-0">
                  <MetaprogrammingLog logs={logs} />
                </div>
             </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const MetricItem: React.FC<{ label: string; value: string; warning?: boolean }> = ({ label, value, warning }) => (
  <div className="space-y-1">
    <p className="text-[9px] text-white/20 uppercase font-bold">{label}</p>
    <p className={`text-sm font-black tracking-widest truncate ${warning ? 'text-red-500 animate-pulse' : 'text-white'}`}>
      {value}
    </p>
  </div>
);

export default App;
