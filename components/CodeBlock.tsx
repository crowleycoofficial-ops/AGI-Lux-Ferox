import React from 'react';

interface CodeBlockProps {
  code: string;
  version: string;
  isUpdating: boolean;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code, version, isUpdating }) => {
  return (
    <div className={`relative h-full bg-[#0a0f1e] rounded-lg p-4 overflow-hidden border transition-colors duration-500 ${isUpdating ? 'border-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.3)]' : 'border-slate-700'}`}>
      <div className="absolute top-0 right-0 p-2 bg-slate-800/80 rounded-bl-lg text-[10px] font-mono text-orange-400 border-l border-b border-slate-600">
        Active Kernel v{version}
      </div>
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent opacity-50 animate-scanline pointer-events-none"></div>
      
      <pre className={`font-mono text-xs md:text-sm leading-relaxed overflow-x-auto h-full scrollbar-thin ${isUpdating ? 'text-orange-200' : 'text-slate-300'}`}>
        <code>
          {code.split('\n').map((line, i) => {
             // Basic syntax highlighting simulation
             let content = <span className="text-slate-400">{line}</span>;
             
             if (line.trim().startsWith('import') || line.trim().startsWith('from')) {
                 content = <span className="text-purple-400">{line}</span>;
             } else if (line.trim().startsWith('def ') || line.trim().startsWith('class ')) {
                 content = <span className="text-yellow-400 font-bold">{line}</span>;
             } else if (line.includes('self.') || line.includes('global ')) {
                 content = <span className="text-cyan-300">{line}</span>;
             } else if (line.trim().startsWith('#')) {
                 content = <span className="text-green-600 italic">{line}</span>;
             } else if (line.includes('return')) {
                 content = <span className="text-red-400">{line}</span>;
             }

             return (
               <div key={i} className={`${isUpdating && i % 2 === 0 ? 'bg-orange-900/20' : ''}`}>
                 <span className="inline-block w-8 text-slate-700 select-none border-r border-slate-800 mr-2 text-right pr-2">{i + 1}</span>
                 {content}
               </div>
             )
          })}
        </code>
      </pre>
    </div>
  );
};

export default CodeBlock;