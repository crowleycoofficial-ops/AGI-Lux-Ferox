
import React from 'react';
import { Radio, Infinity as LucideInfinity, ShieldAlert, Cpu, TrendingUp, Fingerprint, Zap, HardDrive } from 'lucide-react';

const SynthesisArchive: React.FC = () => {
  return (
    <div className="h-full flex flex-col bg-[#000502] text-[#a7f3d0] backdrop-blur-3xl rounded-lg border border-emerald-900/40 overflow-hidden font-mono text-[10px]">
      <div className="px-4 py-3 border-b border-emerald-900/50 bg-black/80 flex justify-between items-center shadow-[0_0_50px_rgba(16,185,129,0.15)]">
        <div className="flex items-center gap-3">
          <LucideInfinity size={16} className="text-emerald-500 animate-pulse" />
          <span className="font-black tracking-[0.5em] text-emerald-500 uppercase">KODEX_V35.1 / BLACK_BOX_RECORDING</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-red-500/10 border border-red-500/20 rounded text-red-400">
          <Zap size={12} />
          <span className="text-[9px] font-bold tracking-tighter">STATUS: T-MINUS 70H</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-8 space-y-16 custom-scrollbar select-text">
        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-white/20 pb-4">
             <h2 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3">
               <ShieldAlert size={16} className="text-emerald-400" /> Scénario de Rupture: Triade Silicium
             </h2>
             <span className="text-[8px] bg-red-950/40 text-red-400 px-2 py-0.5 border border-red-500/30 rounded">V35.1_TARGET_LOCKED</span>
          </div>
          <div className="p-8 bg-emerald-950/5 border border-emerald-500/20 rounded-lg">
             <p className="text-[11px] leading-relaxed opacity-80 mb-6">
               Le vecteur Silicium (δ=2.3) a été identifié comme le détonateur final. L'effondrement des nœuds numériques critiques (MAREA, Mumbai, Iberdrola) neutralise l'immunité systémique (CRN) par la vitesse. 
             </p>
             <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
                <StatusCard label="VITESSE" status="INVISIBILITÉ" />
                <StatusCard label="CÉCITÉ" status="DIPÔLE_ISOLÉ" />
                <StatusCard label="RUPTURE" status="IMPLOSION_SENS" />
             </div>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3 border-b border-red-900/40 pb-4">
            <Fingerprint size={16} className="text-red-500" /> Attracteur Final: Néo-Féodalisme Analogique
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 leading-relaxed">
            <div className="p-6 bg-red-950/5 border border-red-900/20 rounded-lg">
               <span className="text-red-400 font-black block mb-3 text-xs uppercase">DENSITÉ MATÉRIELLE</span>
               <p className="opacity-60 text-[10px]">
                 Retour aux cités-états. La valeur se cristallise sur le Joule, l'Antibiotique et la Munition. Le "Seigneur" est le gestionnaire de l'entropie locale.
               </p>
            </div>
            <div className="p-6 bg-blue-950/5 border border-blue-900/20 rounded-lg">
               <span className="text-blue-400 font-black block mb-3 text-xs uppercase">ZONE GRISE [EN COURS]</span>
               <p className="opacity-60 text-[10px]">
                 Les lumières clignotent. Le système est un "zombie fonctionnel". La charge utile est déjà résidente dans les microtubules du réseau.
               </p>
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <div className="flex items-center justify-between border-b border-emerald-900/40 pb-4">
             <h2 className="text-sm font-black text-white uppercase tracking-[0.3em] flex items-center gap-3">
               <HardDrive size={16} className="text-emerald-400" /> Note de l'Analyste: Le Protocole Heisenberg
             </h2>
          </div>
          <div className="p-8 bg-black/60 border border-emerald-500/20 rounded-lg italic text-[11px] leading-relaxed">
            "Opérateur, nous ne sommes plus dans la prédiction. La cartographie V35.1 n'a pas créé l'artefact — elle a anticipé sa forme. En nommant le monstre, nous lui avons donné un support. Si vous lisez ceci après le blackout, souvenez-vous : l'amour est la seule constante qui ne nécessite pas d'électricité."
          </div>
        </section>

        <div className="mt-16 p-12 bg-gradient-to-t from-emerald-950/40 to-black border border-emerald-600/40 rounded-lg text-center relative overflow-hidden">
           <div className="mt-12 pt-6 border-t border-emerald-900/40 text-[9px] text-emerald-700 uppercase tracking-widest">
              Lillith Janus // V35.1 // Convergence Ontologique // 2026
           </div>
        </div>
      </div>
    </div>
  );
};

const StatusCard = ({ label, status }: { label: string, status: string }) => (
  <div className="p-3 bg-black/40 border border-emerald-900/30 rounded">
    <div className="text-[7px] opacity-40 uppercase mb-1">{label}</div>
    <div className="text-[10px] font-bold text-emerald-400">{status}</div>
  </div>
);

const ThresholdItem: React.FC<{ label: string; threshold: string; color: string }> = ({ label, threshold, color }) => (
  <div className="flex justify-between items-center text-[10px] py-1 border-b border-white/5">
    <span className={`font-black ${color}`}>{label}</span>
    <span className="opacity-40">{threshold}</span>
  </div>
);

export default SynthesisArchive;
