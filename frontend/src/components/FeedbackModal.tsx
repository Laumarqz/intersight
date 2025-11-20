import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Copy, CheckCircle2 } from 'lucide-react';

interface FeedbackModalProps {
  candidate: any;
  onClose: () => void;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({ candidate, onClose }) => {
  const [feedbackEmail, setFeedbackEmail] = React.useState<string>('');
  const [loading, setLoading] = React.useState(true);
  const [copied, setCopied] = React.useState(false);

  React.useEffect(() => {
    const fetchFeedback = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            candidate_id: candidate.id,
            candidate_name: candidate.filename.replace(/\.(pdf|docx)$/i, ''),
            job_title: candidate.full_context?.job_title || 'Position',
            company_name: candidate.full_context?.company_name || 'Our Company',
            analysis_json: candidate.analysis,
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to generate feedback');
        }

        const data = await response.json();
        setFeedbackEmail(data.email_body);
      } catch (error) {
        console.error('Error fetching feedback:', error);
        setFeedbackEmail('Failed to generate feedback email. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchFeedback();
  }, [candidate]);

  const handleCopy = () => {
    navigator.clipboard.writeText(feedbackEmail);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-surface border border-white/10 rounded-3xl p-6 max-w-2xl w-full max-h-[80vh] overflow-hidden flex flex-col"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-white">Rejection Feedback</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-full transition-colors"
              aria-label="Close"
            >
              <X className="w-6 h-6 text-white/70" />
            </button>
          </div>

          {/* Candidate Info */}
          <div className="mb-4 p-3 bg-white/5 rounded-xl">
            <p className="text-sm text-gray-400">Candidate</p>
            <p className="text-white font-semibold">{candidate.filename}</p>
          </div>

          {/* Email Content */}
          <div className="flex-1 overflow-y-auto custom-scrollbar mb-4">
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              </div>
            ) : (
              <div className="bg-white/5 rounded-xl p-4 font-mono text-sm text-gray-300 whitespace-pre-wrap">
                {feedbackEmail}
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={handleCopy}
              disabled={loading}
              className="flex-1 px-6 py-3 bg-primary hover:bg-primary/80 disabled:bg-gray-600 disabled:cursor-not-allowed rounded-xl font-semibold transition-colors flex items-center justify-center gap-2"
            >
              {copied ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-5 h-5" />
                  Copy to Clipboard
                </>
              )}
            </button>
            <button
              onClick={onClose}
              className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-xl font-semibold transition-colors"
            >
              Close
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};
