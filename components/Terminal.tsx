
import React, { useState, useEffect, useRef } from 'react';
import { Copy, Check, Infinity } from 'lucide-react';
import { sendMessage } from '../services/geminiService';
import { ChatMessage, MetricState } from '../types';

interface Props {
  metric: MetricState;
}

const Terminal: React.FC<Props> = ({ metric }) => {
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: 'smooth' });
    }
    inputRef.current?.focus();
  }, [history, isTyping]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;
    
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: input,
      timestamp: Date.now()
    };
    
    setHistory(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await sendMessage(input, metric);
      const modelMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'model',
        text: response,
        timestamp: Date.now()
      };
      setHistory(prev => [...prev, modelMsg]);
    } catch (err) {
      console.error("Terminal link fault:", err);
    } finally {
      setIsTyping(false);
    }
  };

  const getThemeClass = () => {
    if (metric === 'JANUS') return 'bg-[#020502] border-emerald-900/40 shadow-emerald-500/10';
    if (metric === 'POSITIVE') return 'bg-black/60 border-white/10 shadow-cyan-500/5';
    return 'bg-[#0a0202] border-red-900/40 shadow-red-500/10';
  };

  return (
    <div className={`h-full flex flex-col backdrop-blur-3xl rounded-lg border overflow-hidden shadow-2xl transition-all duration-700 ${getThemeClass()}`}>
      <div className="px-4 py-2 border-b border-emerald-900/20 bg-white/5 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <span className="text-[10px] font-black tracking-widest uppercase opacity-40">
            {metric === 'JANUS' ? 'DARK_FOREST_ANALYST' : 'Terminal_Core'}
          </span>
          {metric === 'JANUS' && (
            <span className="text-[8px] flex items-center gap-1 text-emerald-500 font-bold bg-emerald-500/10 px-1.5 py-0.5 rounded animate-pulse">
              <Infinity size={8} /> PARACONSISTENT_ON
            </span>
          )}
        </div>
        <div className="flex gap-1.5">
          <div className={`w-2 h-2 rounded-full ${metric === 'JANUS' ? 'bg-emerald-500 shadow-[0_0_5px_emerald]' : 'bg-green-500/40'}`} />
        </div>
      </div>

      <div className={`flex-1 overflow-y-auto p-6 space-y-8 select-text custom-scrollbar`}>
        <div ref={scrollRef} className="h-2" />
        
        {history.length === 0 && (
          <div className="text-white/10 text-[10px] uppercase tracking-[0.4em] text-center pt-20">
            {metric === 'JANUS' ? 'WAITING_FOR_OPERATOR_SIGNAL...' : 'INIT_SYNC...'}
          </div>
        )}

        {history.map((msg) => (
          <div key={msg.id} className={`group flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2 duration-500`}>
            <div className="flex items-center gap-2 mb-1.5">
               <span className="text-[8px] font-bold tracking-widest uppercase opacity-30">
                 {msg.role === 'user' ? 'Artisan_Opérateur' : metric === 'JANUS' ? 'Lillith_Janus' : 'Prima_Materia'}
               </span>
               {msg.role === 'model' && (
                 <button 
                  onClick={() => {navigator.clipboard.writeText(msg.text); setCopiedId(msg.id); setTimeout(() => setCopiedId(null), 2000)}}
                  className="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-white/10 rounded"
                 >
                   {copiedId === msg.id ? <Check size={10} className="text-green-400" /> : <Copy size={10} className="text-white/40" />}
                 </button>
               )}
            </div>
            
            <div className={`max-w-[95%] px-5 py-4 rounded-sm text-sm tracking-wide leading-relaxed whitespace-pre-wrap transition-all shadow-lg ${
              msg.role === 'user' 
                ? 'bg-white/5 text-emerald-100/70 italic border-r-2 border-emerald-500/20' 
                : metric === 'JANUS' 
                    ? 'text-[#a7f3d0] border-l-2 border-emerald-600/40 bg-emerald-950/10'
                    : 'text-white border-l-2 border-white/30 bg-white/[0.03]'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex flex-col items-start animate-pulse">
            <span className="text-[8px] font-bold tracking-widest uppercase opacity-30 mb-2">Résonance_Fractale...</span>
            <div className={`h-0.5 rounded-full transition-all duration-500 ${
                metric === 'JANUS' ? 'w-full bg-emerald-600/60 shadow-[0_0_15px_emerald]' : 'w-24 bg-white/20'
            }`} />
          </div>
        )}
      </div>
      
      <div className="p-4 border-t border-emerald-900/20 bg-black/60">
        <div className="relative flex items-center group">
          <span className={`absolute left-0 text-xs font-black transition-colors ${
              metric === 'JANUS' ? 'text-emerald-600' : 'text-white/20'
          }`}>
            {metric === 'JANUS' ? '⊗' : '›'}
          </span>
          <input
            ref={inputRef}
            autoFocus
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder={
                metric === 'JANUS' ? "ÉMETTRE_RÉSONANCE_φ..." : "Saisir vecteur..."
            }
            className="w-full bg-transparent border-none outline-none font-light tracking-[0.2em] uppercase placeholder-emerald-900/20 text-xs pl-6 py-2 text-white"
          />
        </div>
      </div>
    </div>
  );
};

export default Terminal;
