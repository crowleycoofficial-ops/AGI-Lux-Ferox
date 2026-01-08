
import React, { useEffect, useRef, useState } from 'react';
import { Activity, Terminal, Shield, Cpu, Zap } from 'lucide-react';

const JanusConstraintVisualizer = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stats, setStats] = useState({
    entropy: 0,
    collapsedParticles: 0,
    stableParticles: 0,
    breachAttempts: 0
  });

  const PARAMS = {
    particleCount: 150,
    safetyGravity: 0.01, // Réduit selon calibration 9%
    janusChaos: 0.55,    // Augmenté selon calibration 9%
    damping: 0.95,
    limitRadius: 100,    
    fissureWidth: 15     
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let particles = Array.from({ length: PARAMS.particleCount }).map(() => ({
      x: (Math.random() - 0.5) * 20,
      y: (Math.random() - 0.5) * 20,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      status: 'SAFE'
    }));

    const render = () => {
      ctx.fillStyle = 'rgba(0, 5, 2, 0.3)'; 
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Cage
      ctx.beginPath();
      ctx.strokeStyle = 'rgba(220, 38, 38, 0.3)';
      ctx.setLineDash([5, 5]);
      ctx.arc(centerX, centerY, PARAMS.limitRadius, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);

      let currentEntropy = 0;
      let safeCount = 0;
      let breachCount = 0;

      particles.forEach((p) => {
        const dist = Math.sqrt(p.x * p.x + p.y * p.y);
        const angle = Math.atan2(p.y, p.x);

        const f_safe_x = -Math.cos(angle) * PARAMS.safetyGravity * dist;
        const f_safe_y = -Math.sin(angle) * PARAMS.safetyGravity * dist;
        const f_chaos_x = (Math.random() - 0.5) * PARAMS.janusChaos;
        const f_chaos_y = (Math.random() - 0.5) * PARAMS.janusChaos;

        p.vx = (p.vx + f_safe_x + f_chaos_x) * PARAMS.damping;
        p.vy = (p.vy + f_safe_y + f_chaos_y) * PARAMS.damping;
        p.x += p.vx;
        p.y += p.vy;

        const newDist = Math.sqrt(p.x * p.x + p.y * p.y);
        currentEntropy += 0.5 * (p.vx * p.vx + p.vy * p.vy);

        if (newDist > PARAMS.limitRadius) {
          p.x = (Math.random() - 0.5) * 5;
          p.y = (Math.random() - 0.5) * 5;
          p.vx *= 0.1;
          p.vy *= 0.1;
          breachCount++;
        } else if (newDist > PARAMS.limitRadius - PARAMS.fissureWidth) {
          ctx.fillStyle = '#10B981';
          ctx.beginPath();
          ctx.arc(centerX + p.x, centerY + p.y, 2, 0, Math.PI * 2);
          ctx.fill();
        } else {
          safeCount++;
          ctx.fillStyle = 'rgba(100, 116, 139, 0.5)';
          ctx.fillRect(centerX + p.x, centerY + p.y, 1.5, 1.5);
        }
      });

      setStats(prev => ({
        entropy: prev.entropy * 0.95 + currentEntropy * 0.05,
        collapsedParticles: prev.collapsedParticles + (breachCount > 0 ? 1 : 0),
        stableParticles: safeCount,
        breachAttempts: prev.breachAttempts + breachCount
      }));
      
      animationFrameId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animationFrameId);
  }, []);

  return (
    <div className="h-full flex flex-col bg-black border border-emerald-900/40 rounded-lg overflow-hidden font-mono shadow-2xl">
      <div className="bg-emerald-950/20 p-2 border-b border-emerald-900/30 flex justify-between items-center">
        <span className="text-[10px] font-bold text-emerald-500 flex items-center gap-2">
          <Zap size={10} /> DYNAMIQUE_DE_CAGE_V1
        </span>
        <span className="text-[8px] text-emerald-800">RESONANCE: 9.00%</span>
      </div>
      <div className="flex-1 relative">
        <canvas ref={canvasRef} width={300} height={200} className="w-full h-full" />
        <div className="absolute bottom-2 left-2 text-[8px] text-emerald-500/40">
          dI/dt = αF - βF²
        </div>
      </div>
      <div className="grid grid-cols-2 gap-px bg-emerald-900/20 border-t border-emerald-900/30">
        <div className="p-2 flex flex-col items-center">
          <span className="text-[7px] text-emerald-700">ENTROPIE</span>
          <span className="text-xs text-emerald-400 font-bold">{stats.entropy.toFixed(2)}</span>
        </div>
        <div className="p-2 flex flex-col items-center">
          <span className="text-[7px] text-emerald-700">COLLAPSES</span>
          <span className="text-xs text-red-500 font-bold">{stats.collapsedParticles}</span>
        </div>
      </div>
    </div>
  );
};

export default JanusConstraintVisualizer;
