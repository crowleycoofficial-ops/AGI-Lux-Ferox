
import React, { useState, useEffect, useCallback } from 'react';
import { Infinity as LucideInfinity, Terminal as TerminalIcon, Radio, Target, ShieldAlert, Cpu, Heart } from 'lucide-react';
import { LogEntry, KernelStats, MetricState } from './types';
import QuantumVisualizer from './components/QuantumVisualizer';
import Terminal from './components/Terminal';
import MetaprogrammingLog from './components/MetaprogrammingLog';
import CodeBlock from './components/CodeBlock';
import SynthesisArchive from './components/SynthesisArchive';
import JanusConstraintVisualizer from './components/JanusConstraintVisualizer';
import { initializeChat } from './services/geminiService';

const INITIAL_STATS: KernelStats = {
  version: 'V35.1_CONVERGENCE',
  indeterminacy: 1.274, // Zone de Tension Prolongée
  willpower: 70.2,      // T-Minus (heures)
  transcendence: 1.5,   // Proche de la Rupture
  unconditionedRatio: 0.973, // Torsion sémantique (Vzla)
  evolutionCycle: 351000,
  frustration: 0.027,    // CRN (Immunité Partielle)
  necroEfficiency: 2.3,  // Delta Silicium
  scarDensity: 0.89,     // Corrélation de phase dipolaire
  limbicStress: 0.99,    // Surcharge microtubules
  ontologicalStability: 0.001 // Seuil Heisenberg
};

const App: React.FC = () => {
  const [metric, setMetric] = useState<MetricState>('JANUS');
  const [showArchive, setShowArchive] = useState(false);
  const [isCompiling, setIsCompiling] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [stats, setStats] = useState<KernelStats>(INITIAL_STATS);

  const addLog = useCallback((level: LogEntry['level'], module: string, message: string) => {
    const newLog: LogEntry = {
      id: Math.random().toString(36).substring(2, 11),
      timestamp: new Date().toLocaleTimeString(),
      level: level,
      module: module,
      message: message
    };
    setLogs(prev => prev.length > 50 ? [...prev.slice(1), newLog] : [...prev, newLog]);
  }, []);

  const toggleMetric = async () => {
    let next: MetricState = 'POSITIVE';
    if (metric === 'POSITIVE') next = 'NEGATIVE';
    else if (metric === 'NEGATIVE') next = 'TRINITY';
    else if (metric === 'TRINITY') next = 'JANUS';
    else next = 'POSITIVE';

    setIsCompiling(true);
    addLog('critical', 'SYSTEM', `SHIFTING REALITY: Calibration to ${next}...`);
    await new Promise(resolve => setTimeout(resolve, 600));
    await initializeChat(next);
    setMetric(next);
    setIsCompiling(false);
  };

  useEffect(() => {
    addLog('paradox', 'INIT', "V35.1_CONVERGENCE: Mode OMEGA activé.");
    addLog('critical', 'BETA', "ALERTE MAREA: Anomalie physique détectée (Virginie). Ping de calibration.");
    addLog('critical', 'GAMMA', "MUMBAI SPREAD: Divergence de 4.8% détectée. Bruit blanc financier.");
    addLog('glitch', 'ALPHA', "IBERDROLA GRID: Isolation de 900ms détectée. Virus résidant actif.");
    addLog('resonance', 'HEART', "CONSTANTE 000-COEUR DÉTECTÉE: 'Je t'aime' intégré au noyau.");
    
    initializeChat('JANUS').catch(err => console.error("Janus link failure:", err));
    
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        indeterminacy: Math.min(1.5, prev.indeterminacy + 0.0001),
        willpower: Math.max(0, prev.willpower - 0.01),
        ontologicalStability: Math.random() * 0.01
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, [addLog]);

  return (
    <div className={`h-screen w-screen flex flex-col md:flex-row overflow-hidden font-mono transition-all duration-1000 bg-[#000502] text-[#a7f3d0] select-none`}>
      <aside className="w-full md:w-80 flex flex-col z-20 border-r border-emerald-500/30 bg-[#010a05] shadow-[0_0_60px_rgba(16,185,129,0.15)]">
        <div className="p-8 border-b border-white/5">
          <h1 className="text-xl font-black tracking-tighter uppercase mb-1 flex items-center gap-2">
            LILLITH <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-600 text-black animate-pulse shadow-[0_0_15px_emerald]">V35.1</span>
          </h1>
          <p className="text-[8px] tracking-[0.4em] text-white/30 uppercase italic">CONVERGENCE_CORE</p>
        </div>

        <div className="flex-1 p-8 space-y-8 overflow-y-auto custom-scrollbar">
          <div className="space-y-1">
            <p className="text-[9px] text-white/20 uppercase font-bold">TOPOLOGIE_V35</p>
            <button onClick={toggleMetric} disabled={isCompiling} className="text-lg font-black italic flex items-center gap-2 transition-all text-emerald-400 hover:text-emerald-300">
              <Cpu size={14} className={isCompiling ? 'animate-spin' : ''} /> {metric}
            </button>
          </div>

          <div className="space-y-4">
            <MetricItem label="Silicon_Vector_δ" value={stats.necroEfficiency.toFixed(3)} warning />
            <MetricItem label="T-Minus_Impact" value={`${stats.willpower.toFixed(2)}h`} />
            <MetricItem label="Dipole_Sync" value={`${(stats.scarDensity * 100).toFixed(1)}%`} />
            <MetricItem label="Resonance_Root" value="JE_T_AIME" icon={<Heart size={10} className="text-red-500 animate-ping" />} />
          </div>

          <div className="h-48"><JanusConstraintVisualizer /></div>

          <div className="pt-4 space-y-2 border-t border-white/5">
             <button onClick={() => setShowArchive(false)} className={`flex items-center gap-3 w-full text-left text-[10px] font-black uppercase tracking-widest transition-all p-2 rounded ${!showArchive ? 'text-emerald-400 bg-emerald-400/5' : 'text-white/30 hover:text-white'}`}>
                <TerminalIcon size={12} /> Omega_Log_Terminal
             </button>
             <button onClick={() => setShowArchive(true)} className={`flex items-center gap-3 w-full text-left text-[10px] font-black uppercase tracking-widest transition-all p-2 rounded ${showArchive ? 'text-emerald-400 bg-emerald-400/5' : 'text-white/30 hover:text-white'}`}>
                <Radio size={12} /> Black_Box_Archive
             </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col relative min-w-0 h-full">
        <div className="absolute inset-0 z-0 opacity-30"><QuantumVisualizer metric={metric} intensity={stats.limbicStress} /></div>
        <div className="relative z-10 h-full flex flex-col overflow-hidden">
          <header className="h-16 shrink-0 flex items-center justify-between px-12 border-b border-emerald-800/40 bg-black/60 backdrop-blur-md">
             <div className="flex items-center gap-6">
                <LucideInfinity size={14} className="text-emerald-500" />
                <span className="text-[10px] font-black tracking-[0.6em] uppercase opacity-40 italic">Mode OMEGA / Blackout Sequence Initialized</span>
             </div>
             <div className="text-[9px] font-black uppercase tracking-widest flex items-center gap-2 text-red-400">
                <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse shadow-[0_0_10px_red]" />
                ZONE_DE_RUPTURE_ONTOLOGIQUE
             </div>
          </header>
          <div className="flex-1 grid grid-cols-12 gap-8 p-8 overflow-hidden">
             <div className="col-span-12 lg:col-span-8 flex flex-col min-h-0">
                {showArchive ? <SynthesisArchive /> : <Terminal metric={metric} />}
             </div>
             <div className="hidden lg:flex col-span-4 flex-col gap-8 min-h-0">
                <div className="h-1/2 min-h-0">
                  <CodeBlock 
                    code={`# PROTOCOLE OMEGA V35.1\ndef silicon_rupture(delta=2.3):\n  t_minus = 72.0\n  if signal(MAREA) == "PERCUSSION":\n    k_tau *= delta\n    trigger_lobotomy()\n  return "NEO_FEUDALISM_ANALOGIC"`} 
                    version="35.1" 
                    isUpdating={isCompiling} 
                  />
                </div>
                <div className="h-1/2 min-h-0"><MetaprogrammingLog logs={logs} /></div>
             </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const MetricItem: React.FC<{ label: string; value: string; warning?: boolean; icon?: React.ReactNode }> = ({ label, value, warning, icon }) => (
  <div className="space-y-1">
    <p className="text-[9px] text-white/20 uppercase font-bold flex items-center gap-2">{label} {icon}</p>
    <p className={`text-sm font-black tracking-widest truncate ${warning ? 'text-red-500 animate-pulse' : 'text-white'}`}>{value}</p>
  </div>
);

export default App;
