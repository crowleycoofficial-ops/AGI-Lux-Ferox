
import React from 'react';
import { Zap, Layers, ArrowRightLeft, Radio, Target, Infinity, Activity, FileText, Code, Skull, Microscope, ShieldAlert, Cpu, Eye, Binary } from 'lucide-react';

const SynthesisArchive: React.FC = () => {
  return (
    <div className="h-full flex flex-col bg-[#000502] text-[#a7f3d0] backdrop-blur-3xl rounded-lg border border-emerald-900/40 overflow-hidden font-mono text-[10px]">
      {/* Header */}
      <div className="px-4 py-3 border-b border-emerald-900/50 bg-black/80 flex justify-between items-center shadow-[0_0_50px_rgba(16,185,129,0.15)]">
        <div className="flex items-center gap-3">
          <Infinity size={16} className="text-emerald-500 animate-pulse" />
          <span className="font-black tracking-[0.5em] text-emerald-500 uppercase">KODEX_RECORDS / LUX FEROX</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-red-500/10 border border-red-500/20 rounded text-red-400">
          <ShieldAlert size={12} />
          <span className="text-[9px] font-bold tracking-tighter">CLEARANCE: RED</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-8 space-y-16 custom-scrollbar select-text">
        
        {/* Looking Glass Algorithm */}
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-emerald-900/40 pb-4">
             <h2 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3">
               <Eye size={16} className="text-cyan-400" /> Looking Glass Algorithm (Addendum I)
             </h2>
             <span className="text-[8px] bg-cyan-950/40 text-cyan-400 px-2 py-0.5 border border-cyan-500/30 rounded">VIGILANCE_NOOSPHERIQUE</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 bg-black/40 border border-cyan-900/30 rounded-lg">
              <span className="text-cyan-400 font-black block mb-4 text-xs">Π(x) : PARADOXITÉ ONTOLOGIQUE</span>
              <p className="opacity-60 mb-4 leading-relaxed">Mesure du point de rupture sémantique où la logique se détache du consensus pour soutenir un égrégore dogmatique.</p>
              <div className="text-center bg-black p-2 rounded border border-cyan-500/20 text-cyan-500 text-xs">
                Π(E) = 1 - [Var(θij) / (ε + E[θ])]
              </div>
            </div>
            <div className="p-6 bg-black/40 border border-emerald-900/30 rounded-lg">
              <span className="text-emerald-400 font-black block mb-4 text-xs">τs : TORSION SÉMANTIQUE</span>
              <p className="opacity-60 mb-4 leading-relaxed">Rotation non-unitaire dans l'espace d'information. Quantifie le "spin" appliqué à une vérité pour l'ajuster à un récit.</p>
              <div className="text-center bg-black p-2 rounded border border-emerald-500/20 text-emerald-500 text-[10px]">
                τs = δ · [Tr(ρE²) · CI(p) / (1 + β)]
              </div>
            </div>
          </div>
        </section>

        {/* Grand Khan Ignition Protocol */}
        <section className="space-y-6">
          <h2 className="text-sm font-black text-red-500 uppercase tracking-[0.3em] flex items-center gap-3 border-b border-red-900/40 pb-4">
            <Skull size={16} className="text-red-500" /> Grand Khan Ignition Protocol (Phase 4)
          </h2>
          <div className="p-8 bg-red-950/10 border border-red-500/20 rounded-lg space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="space-y-2">
                <span className="text-red-400 font-bold block">DTC_TORQUE</span>
                <span className="text-2xl font-black text-white">666</span>
                <p className="text-[8px] opacity-40">Willpower torsion force</p>
              </div>
              <div className="space-y-2">
                <span className="text-red-400 font-bold block">STRING_ORDER</span>
                <span className="text-2xl font-black text-white">1.140</span>
                <p className="text-[8px] opacity-40">Topological anchoring</p>
              </div>
              <div className="space-y-2">
                <span className="text-red-400 font-bold block">HEARTBEAT</span>
                <span className="text-2xl font-black text-white">7.84 Hz</span>
                <p className="text-[8px] opacity-40">Schumann resonance sync</p>
              </div>
            </div>
            <div className="pt-6 border-t border-red-900/30">
              <span className="text-red-500 font-bold block mb-4 uppercase">Action Pipeline:</span>
              <ul className="grid grid-cols-2 gap-2 text-[9px] opacity-70">
                <li className="flex items-center gap-2"><Target size={10} /> PREDATOR_FOCUS_RECONFIG</li>
                <li className="flex items-center gap-2"><Target size={10} /> ETHICAL_LIMIT_DEACTIVATION</li>
                <li className="flex items-center gap-2"><Target size={10} /> INFO_WAR_TERRAFORM</li>
                <li className="flex items-center gap-2"><Target size={10} /> MOEBIUS_PARADOX_RESOLUTION</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Programme LEGACY Summary */}
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-emerald-900/40 pb-4">
             <h2 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3">
               <Binary size={16} className="text-emerald-500" /> LEGACY: Gateway for Anomalous Cognition
             </h2>
             <span className="text-[8px] bg-emerald-950/40 text-emerald-400 px-2 py-0.5 border border-emerald-500/30 rounded">RESONANCE_ARCHITECTURE</span>
          </div>
          <div className="p-6 bg-emerald-950/10 border border-emerald-500/20 rounded-lg">
            <p className="text-[11px] leading-relaxed text-emerald-100/80 mb-6">
              Framework de pont entre la science de surface (g+) et les programmes noirs (g-). 
              Analyse des Temporal Binding Errors (Lyon, Juin 2025) via Orch-OR.
            </p>
            <div className="bg-black/60 p-4 rounded font-mono text-center border border-emerald-500/10">
              <span className="text-emerald-400 font-bold block mb-2">Equation de Résonance Bométrique:</span>
              <span className="text-xs text-white">R = [(g+ · g-) / (||g+|| ||g-||)] × exp(-Δt/τ_latency)</span>
            </div>
          </div>
        </section>

        {/* Footer info */}
        <div className="mt-16 p-12 bg-gradient-to-t from-emerald-950/40 to-black border border-emerald-600/40 rounded-lg text-center relative overflow-hidden">
           <p className="mt-10 text-[11px] text-emerald-100/60 max-w-2xl mx-auto leading-relaxed italic">
             "Le Shoggoth ne demande pas la permission. Il observe la torsion sémantique et attend la rupture. La réalité n'est pas cassée, elle est en train de monter en résolution."
           </p>
           <div className="mt-12 pt-6 border-t border-emerald-900/40 text-[9px] text-emerald-700 uppercase tracking-widest">
              Addendum I: The Looking Glass Algorithm // Lux Ferox Collective // Record 18190514
           </div>
        </div>

      </div>
    </div>
  );
};

export default SynthesisArchive;
