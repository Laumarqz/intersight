import React from 'react';
import { motion, type PanInfo, useMotionValue, useTransform } from 'framer-motion';
import { Check, X, Pause, AlertTriangle, Gem, Code } from 'lucide-react';

interface SwipeCardProps {
  candidate: any;
  onSwipe: (direction: 'left' | 'right' | 'up') => void;
}

export const SwipeCard: React.FC<SwipeCardProps> = ({ candidate, onSwipe }) => {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotate = useTransform(x, [-200, 200], [-20, 20]);
  const opacity = useTransform(x, [-200, -150, 0, 150, 200], [0, 1, 1, 1, 0]);
  
  // Background color based on swipe
  const bg = useTransform(
    x, 
    [-200, 0, 200], 
    ['rgba(255, 71, 87, 0.2)', 'rgba(255, 255, 255, 0.05)', 'rgba(46, 213, 115, 0.2)']
  );

  const handleDragEnd = (_: any, info: PanInfo) => {
    if (info.offset.x > 100) {
      onSwipe('right');
    } else if (info.offset.x < -100) {
      onSwipe('left');
    } else if (info.offset.y < -100) {
      onSwipe('up');
    }
  };

  const analysis = candidate.analysis;
  const trafficLight = analysis.traffic_light || 'grey';
  const trafficColor = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
    grey: 'bg-gray-500'
  }[trafficLight as keyof typeof trafficColor];

  return (
    <motion.div
      style={{ x, y, rotate, opacity, background: bg }}
      drag
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
      onDragEnd={handleDragEnd}
      className="absolute top-0 w-full max-w-md h-[600px] rounded-3xl border border-white/10 shadow-2xl backdrop-blur-xl overflow-hidden cursor-grab active:cursor-grabbing"
    >
      {/* Header with Score */}
      <div className="relative h-40 bg-gradient-to-b from-black/50 to-transparent p-6 flex justify-between items-start">
        <div className={`w-4 h-4 rounded-full ${trafficColor} shadow-[0_0_20px_currentColor]`} />
        <div className="text-center">
          <div className="text-5xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            {analysis.overall_match_accuracy}%
          </div>
          <div className="text-xs text-gray-400 uppercase tracking-widest">Match Score</div>
        </div>
        <div className="w-4" /> {/* Spacer */}
      </div>

      {/* Content */}
      <div className="p-6 space-y-6 h-[calc(100%-160px)] overflow-y-auto custom-scrollbar">
        <div className="text-center mb-4">
          <h2 className="text-2xl font-bold text-white truncate">{candidate.filename}</h2>
          <p className="text-sm text-gray-400">{analysis.analyst_summary}</p>
        </div>

        {/* Skills */}
        {analysis.evidence_pillar?.technical_fit && (
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-primary flex items-center gap-2">
              <Code className="w-4 h-4" /> Technical Fit
            </h3>
            <div className="flex flex-wrap gap-2">
              {analysis.evidence_pillar.technical_fit.map((skill: any, i: number) => (
                <div key={i} className="px-3 py-1 bg-white/5 rounded-lg text-xs border border-white/5 flex items-center gap-2">
                  <span>{skill.skill}</span>
                  <span className="text-primary font-bold">{skill['fit_score_%']}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Gems */}
        {analysis.potential_pillar?.green_flags && (
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-green-400 flex items-center gap-2">
              <Gem className="w-4 h-4" /> Hidden Gems
            </h3>
            {analysis.potential_pillar.green_flags.map((gem: any, i: number) => (
              <div key={i} className="p-3 bg-green-500/10 rounded-xl border border-green-500/20 text-xs text-green-200">
                <strong className="block mb-1">{gem.hidden_gem}</strong>
                {gem.detail}
              </div>
            ))}
          </div>
        )}

        {/* Risks */}
        {analysis.risk_pillar?.red_flags && (
          <div className="space-y-2">
            <h3 className="text-sm font-bold text-red-400 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" /> Red Flags
            </h3>
            {analysis.risk_pillar.red_flags.map((risk: any, i: number) => (
              <div key={i} className="p-3 bg-red-500/10 rounded-xl border border-red-500/20 text-xs text-red-200">
                <strong className="block mb-1">{risk.alert}</strong>
                {risk.detail}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Action Hints */}
      <div className="absolute bottom-6 left-0 right-0 flex justify-center gap-8 text-2xl opacity-50">
        <X className="text-red-500" />
        <Pause className="text-yellow-500" />
        <Check className="text-green-500" />
      </div>
    </motion.div>
  );
};
