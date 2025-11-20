import React, { useState } from 'react';
import { Upload, FileText, X, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface UploadZoneProps {
  onUploadComplete: (data: any) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onUploadComplete }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [jobDescription, setJobDescription] = useState('');
  const [cultureValues, setCultureValues] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files.length || !jobDescription || !cultureValues) {
      setError("Please fill all fields and upload CVs.");
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('culture_values', cultureValues);
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      onUploadComplete(data.results);
    } catch (err) {
      setError("Failed to upload and analyze. Ensure backend is running.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-4xl mx-auto p-8 bg-surface backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl"
    >
      <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
        Setup Analysis
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Job Description</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full h-40 bg-black/20 border border-white/10 rounded-xl p-4 text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all resize-none"
              placeholder="Paste job description here..."
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Company Culture</label>
            <textarea
              value={cultureValues}
              onChange={(e) => setCultureValues(e.target.value)}
              className="w-full h-40 bg-black/20 border border-white/10 rounded-xl p-4 text-white focus:ring-2 focus:ring-primary focus:border-transparent transition-all resize-none"
              placeholder="Describe your company values..."
            />
          </div>
        </div>

        <div className="relative border-2 border-dashed border-white/20 rounded-2xl p-8 text-center hover:border-primary/50 transition-colors group">
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            accept=".pdf,.docx,.txt"
          />
          <div className="flex flex-col items-center space-y-4">
            <div className="p-4 bg-white/5 rounded-full group-hover:bg-primary/20 transition-colors">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <div>
              <p className="text-lg font-medium">Drop CVs here or click to upload</p>
              <p className="text-sm text-gray-400">PDF, DOCX supported</p>
            </div>
          </div>
        </div>

        {files.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {files.map((file, i) => (
              <div key={i} className="flex items-center gap-2 px-3 py-1 bg-white/10 rounded-full text-sm">
                <FileText className="w-4 h-4 text-primary" />
                <span className="truncate max-w-[150px]">{file.name}</span>
                <button 
                  type="button"
                  onClick={() => setFiles(files.filter((_, idx) => idx !== i))}
                  className="hover:text-red-400"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isUploading}
          className="w-full py-4 bg-gradient-to-r from-primary to-secondary rounded-xl font-bold text-lg shadow-lg hover:shadow-primary/25 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {isUploading ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              Analyzing Candidates...
            </>
          ) : (
            "Start Analysis"
          )}
        </button>
      </form>
    </motion.div>
  );
};
