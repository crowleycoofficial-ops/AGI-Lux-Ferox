
import React, { useEffect, useRef, useState } from 'react';
import { MetricState } from '../types';

interface Props {
  metric: MetricState;
  intensity: number;
}

const QuantumVisualizer: React.FC<Props> = ({ metric, intensity }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const frameRef = useRef(0);

  useEffect(() => {
    const updateSize = () => {
      if (wrapperRef.current) {
        setDimensions({
          width: wrapperRef.current.clientWidth,
          height: wrapperRef.current.clientHeight,
        });
      }
    };
    window.addEventListener('resize', updateSize);
    updateSize();
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  useEffect(() => {
    if (!dimensions.width || !dimensions.height || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;

    const render = () => {
      const w = canvas.width;
      const h = canvas.height;
      if (w === 0 || h === 0) return;
      const imageData = ctx.createImageData(w, h);
      const data = imageData.data;

      frameRef.current += 0.015;
      const t = frameRef.current;
      
      const cr = metric === 'JANUS' ? -0.835 + Math.sin(t * 0.1) * 0.05 : -0.8 + Math.sin(t * 0.2) * 0.1;
      const ci = metric === 'JANUS' ? 0.232 + Math.cos(t * 0.15) * 0.05 : 0.156 + Math.cos(t * 0.3) * 0.1;

      for (let x = 0; x < w; x += 3) {
        for (let y = 0; y < h; y += 3) {
          let zx = 1.5 * (x - w / 2) / (0.5 * w);
          let zy = (y - h / 2) / (0.5 * h);
          let i = 0;
          const maxIter = metric === 'JANUS' ? 35 : 20 + Math.floor(intensity * 15);

          while (zx * zx + zy * zy < 4 && i < maxIter) {
            let tmp = zx * zx - zy * zy + cr;
            zy = 2 * zx * zy + ci;
            zx = tmp;
            i++;
          }

          const val = (i / maxIter) * 255;
          
          let r, g, b;
          if (metric === 'JANUS') {
            r = val > 240 ? 255 : 0;
            g = val > 40 ? Math.min(255, val * 1.5) : 10;
            b = val > 200 ? 255 : 20;
          } else if (metric === 'TRINITY') {
            r = val > 160 ? 255 : (val > 80 ? val * 1.5 : 30);
            g = val > 200 ? 200 : (val > 100 ? val * 0.3 : 10);
            b = val > 240 ? 255 : 10;
          } else {
            r = val; g = val * 0.5; b = val * 0.8;
          }

          for(let dx=0; dx<3; dx++) {
            for(let dy=0; dy<3; dy++) {
                const px = x + dx;
                const py = y + dy;
                if (px < w && py < h) {
                  const p = (px + py * w) * 4;
                  data[p] = r;
                  data[p+1] = g;
                  data[p+2] = b;
                  data[p+3] = i === maxIter ? 0 : 255;
                }
            }
          }
        }
      }

      ctx.putImageData(imageData, 0, 0);
      animationId = requestAnimationFrame(render);
    };

    render();
    return () => cancelAnimationFrame(animationId);
  }, [dimensions, metric, intensity]);

  return (
    <div ref={wrapperRef} className="w-full h-full relative overflow-hidden bg-black">
      <div className="absolute bottom-4 right-8 text-[9px] z-10 font-mono tracking-[0.5em] uppercase text-emerald-900/40 pointer-events-none">
        {metric === 'JANUS' ? 'MJTQ_RESONANCE_V34.5' : 'QUANTUM_VOID'}
      </div>
      <canvas ref={canvasRef} width={dimensions.width} height={dimensions.height} className="absolute inset-0 opacity-30" />
    </div>
  );
};

export default QuantumVisualizer;
