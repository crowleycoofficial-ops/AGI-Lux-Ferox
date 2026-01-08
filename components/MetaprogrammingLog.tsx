
import React, { useEffect, useRef } from 'react';
import { LogEntry } from '../types';

interface Props {
  logs: LogEntry[];
}

const MetaprogrammingLog: React.FC<Props> = ({ logs }) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="h-full bg-black/60 border border-white/10 rounded-lg flex flex-col font-mono text-xs shadow-inner">
      <div className="px-3 py-2 border-b border-emerald-900/20 bg-emerald-950/5 text-emerald-400/40 font-display flex justify-between">
        <span>JANUS_TELEMETRY</span>
        <span className="text-[8px] animate-pulse">● RESONANCE_SYNC</span>
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1 custom-scrollbar">
        {logs.map((log) => (
          <div key={log.id} className="flex gap-2 hover:bg-white/5 p-0.5 rounded transition-colors border-l border-transparent hover:border-emerald-500/30">
            <span className="text-white/20 shrink-0 text-[9px]">[{log.timestamp}]</span>
            <span className={`uppercase font-bold shrink-0 w-12 text-[9px] ${
              log.level === 'paradox' ? 'text-emerald-400 underline' :
              log.level === 'resonance' ? 'text-emerald-600' :
              log.level === 'critical' ? 'text-red-400' :
              log.level === 'whip' ? 'text-red-600' :
              'text-cyan-900/60'
            }`}>
              {log.level}
            </span>
             <span className="text-white/30 shrink-0 w-20 truncate">[{log.module}]</span>
            <span className="text-white/80 break-all">{log.message}</span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default MetaprogrammingLog;
