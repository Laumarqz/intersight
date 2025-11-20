import { useState, Component, type ErrorInfo, type ReactNode } from 'react';
import { UploadZone } from './components/UploadZone';
import { SwipeCard } from './components/SwipeCard';
import { FeedbackModal } from './components/FeedbackModal';
import { AnimatePresence, motion } from 'framer-motion';
//import { Loader2 } from 'lucide-react';

// Simple Error Boundary to catch crashes
class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean, error: Error | null }> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-red-900/80 text-white rounded-xl border border-red-500">
          <h3 className="font-bold">Component Crashed</h3>
          <p className="font-mono text-sm">{this.state.error?.toString()}</p>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  const [candidates, setCandidates] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [view, setView] = useState<'upload' | 'swipe' | 'finished'>('upload');
  const [heldCandidates, setHeldCandidates] = useState<any[]>([]);
  const [, setAcceptedCandidates] = useState<any[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [rejectedCandidates, setRejectedCandidates] = useState<any[]>([]);
  const [feedbackCandidate, setFeedbackCandidate] = useState<any | null>(null);
  const [showingHeldQueue, setShowingHeldQueue] = useState(false);

  const handleUploadComplete = (data: any[]) => {
    console.log("Upload complete, data:", data);
    setCandidates(data);
    setView('swipe');
  };

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center p-4 overflow-hidden relative">
      {/* Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 rounded-full blur-[120px]" />
      </div>

      <header className="absolute top-8 left-0 right-0 text-center z-10">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent animate-shine bg-[length:200%_auto]">
          Inter-sight
        </h1>
        <p className="text-white/50 mt-2">AI-Powered Recruitment</p>
      </header>

      <main className="w-full max-w-6xl flex items-center justify-center relative z-20 mt-20">
        <AnimatePresence mode="wait">
          {view === 'upload' && (
            <UploadZone key="upload" onUploadComplete={handleUploadComplete} />
          )}

          {view === 'swipe' && candidates.length > 0 && (
            <div className="relative w-full max-w-md h-[600px]">
              {candidates.slice(currentIndex).reverse().map((candidate, index) => {
                const isTop = index === candidates.length - 1 - currentIndex;
                const isBehind = index === candidates.length - 2 - currentIndex;
                
                if (!isTop && !isBehind) return null;

                return (
                  <ErrorBoundary key={candidate.id || index}>
                    <div className="absolute inset-0">
                        <SwipeCard
                            candidate={candidate}
                            onSwipe={(direction) => {
                              const currentCandidate = candidates[currentIndex];
                              
                              // Categorize candidate based on swipe direction
                              if (direction === 'right') {
                                setAcceptedCandidates(prev => [...prev, currentCandidate]);
                              } else if (direction === 'left') {
                                setRejectedCandidates(prev => [...prev, currentCandidate]);
                                setFeedbackCandidate(currentCandidate);
                              } else if (direction === 'up') {
                                setHeldCandidates(prev => [...prev, currentCandidate]);
                              }

                              // Move to next candidate or finish
                              if (currentIndex < candidates.length - 1) {
                                setCurrentIndex(prev => prev + 1);
                              } else {
                                // Main queue done - check if we have held candidates
                                if (heldCandidates.length > 0 && !showingHeldQueue) {
                                  setShowingHeldQueue(true);
                                  setCandidates(heldCandidates);
                                  setHeldCandidates([]);
                                  setCurrentIndex(0);
                                } else {
                                  setView('finished');
                                }
                              }
                            }}
                        />
                    </div>
                  </ErrorBoundary>
                );
              })}
            </div>
          )}
          {view === 'finished' && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center p-12 bg-surface backdrop-blur-xl rounded-3xl border border-white/10"
            >
              <h2 className="text-3xl font-bold mb-4">🎉 All Caught Up!</h2>
              <p className="text-gray-400 mb-8">You've reviewed all candidates.</p>
              <button 
                onClick={() => {
                  setCandidates([]);
                  setCurrentIndex(0);
                  setView('upload');
                }}
                className="px-8 py-3 bg-white/10 hover:bg-white/20 rounded-full transition-colors"
              >
                Start New Session
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Feedback Modal */}
      {feedbackCandidate && (
        <FeedbackModal
          candidate={feedbackCandidate}
          onClose={() => setFeedbackCandidate(null)}
        />
      )}
    </div>
  );
}

export default App;
