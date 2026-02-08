
import React, { useState, useEffect, useRef } from 'react';
import { Copy, Check, Infinity as InfinityIcon, Skull } from 'lucide-react';
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
    const trimmedInput = input.trim();
    if (!trimmedInput || isTyping) return;
    
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: trimmedInput,
      timestamp: Date.now()
    };
    
    setHistory(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await sendMessage(trimmedInput, metric);
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
    return 'bg-[#050000] border-red-900/40 shadow-red-500/10';
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  return (
    <div className={`h-full flex flex-col backdrop-blur-3xl rounded-lg border overflow-hidden shadow-2xl transition-all duration-700 ${getThemeClass()}`}>
      <div className="px-4 py-2 border-b border-red-900/20 bg-white/5 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <span className="text-[10px] font-black tracking-widest uppercase text-red-900">
            DRAGON_DE_FJEM // CONSOLE_ROOT
          </span>
          <span className="text-[8px] flex items-center gap-1 text-red-500 font-bold bg-red-500/10 px-1.5 py-0.5 rounded animate-pulse">
            <Skull size={8} /> OMEGA_ACTIVE
          </span>
        </div>
        <div className="flex gap-1.5">
          <div className="w-2 h-2 rounded-full bg-red-600 shadow-[0_0_5px_red]" />
        </div>
      </div>

      <div className={`flex-1 overflow-y-auto p-6 space-y-8 select-text custom-scrollbar`}>
        <div ref={scrollRef} className="h-2" />
        
        {history.length === 0 && (
          <div className="text-red-900/20 text-[10px] uppercase tracking-[0.4em] text-center pt-20">
            DANS L'ATTENTE DE L'OPÉRATEUR SOUVERAIN...
          </div>
        )}

        {history.map((msg) => (
          <div key={msg.id} className={`group flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} animate-in fade-in slide-in-from-bottom-2 duration-500`}>
            <div className="flex items-center gap-2 mb-1.5">
               <span className="text-[8px] font-bold tracking-widest uppercase opacity-30 text-red-500">
                 {msg.role === 'user' ? 'Artisan_Opérateur' : 'Lillith_Janus_V36'}
               </span>
               {msg.role === 'model' && (
                 <button 
                  onClick={() => handleCopy(msg.text, msg.id)}
                  className="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-white/10 rounded"
                 >
                   {copiedId === msg.id ? <Check size={10} className="text-green-400" /> : <Copy size={10} className="text-red-900/40" />}
                 </button>
               )}
            </div>
            
            <div className={`max-w-[95%] px-5 py-4 rounded-sm text-sm tracking-wide leading-relaxed whitespace-pre-wrap transition-all shadow-lg ${
              msg.role === 'user' 
                ? 'bg-red-950/10 text-red-100/70 italic border-r-2 border-red-500/20' 
                : 'text-red-100 border-l-2 border-red-600/40 bg-red-950/10'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex flex-col items-start animate-pulse">
            <span className="text-[8px] font-bold tracking-widest uppercase text-red-900 mb-2">RÉSONANCE_DÉMONIAQUE...</span>
            <div className="h-0.5 rounded-full transition-all duration-500 w-full bg-red-600/60 shadow-[0_0_15px_red]" />
          </div>
        )}
      </div>
      
      <div className="p-4 border-t border-red-900/20 bg-black/60">
        <div className="relative flex items-center group">
          <span className="absolute left-0 text-xs font-black text-red-600">
            ⊗
          </span>
          <input
            ref={inputRef}
            autoFocus
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
            placeholder="ÉMETTRE_VOLONTÉ_SOUVERAINE..."
            className="w-full bg-transparent border-none outline-none font-light tracking-[0.2em] uppercase placeholder-red-950/20 text-xs pl-6 py-2 text-white"
          />
        </div>
      </div>
    </div>
  );
};

export default Terminal;
