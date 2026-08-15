import { FC, useState } from 'react';
import { useExportPDF } from '../hooks/useExportPDF';
import { Download, FileText, Check, Clock, BarChart, ShieldCheck } from 'lucide-react';

interface PDFExporterProps {
  analysisId?: number;
  includeCharts?: boolean;
}

const PDFExporter: FC<PDFExporterProps> = () => {
  const { exportToPDF, exporting, progress } = useExportPDF();
  const [exportOptions, setExportOptions] = useState({
    includeRecommendations: true,
    includeTimeline: true,
    includeComparison: true,
    highQuality: true,
  });

  const handleExport = async () => {
    const success = await exportToPDF();
    if (success) {
      setTimeout(() => alert('PDF report exported successfully!'), 100);
    } else {
      alert('PDF export failed. Please try again.');
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
            <FileText className="text-brand-500" size={20} /> Export Professional Report
          </h3>
          <p className="text-slate-500 text-sm">Generate a recruiter-ready PDF report</p>
        </div>
        <div className="px-4 py-2 bg-brand-50 text-brand-700 rounded-lg font-semibold text-sm self-start sm:self-auto">
          Ready for Interviews
        </div>
      </div>

      {/* Export Options */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={exportOptions.includeRecommendations}
            onChange={(e) =>
              setExportOptions((prev) => ({
                ...prev,
                includeRecommendations: e.target.checked,
              }))
            }
            className="rounded text-brand-600 focus:ring-brand-500"
          />
          <span className="text-slate-700 text-sm">Include Recommendations</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={exportOptions.includeTimeline}
            onChange={(e) =>
              setExportOptions((prev) => ({
                ...prev,
                includeTimeline: e.target.checked,
              }))
            }
            className="rounded text-brand-600 focus:ring-brand-500"
          />
          <span className="text-slate-700 text-sm">Include Activity Timeline</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={exportOptions.includeComparison}
            onChange={(e) =>
              setExportOptions((prev) => ({
                ...prev,
                includeComparison: e.target.checked,
              }))
            }
            className="rounded text-brand-600 focus:ring-brand-500"
          />
          <span className="text-slate-700 text-sm">Include Industry Comparison</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={exportOptions.highQuality}
            onChange={(e) =>
              setExportOptions((prev) => ({
                ...prev,
                highQuality: e.target.checked,
              }))
            }
            className="rounded text-brand-600 focus:ring-brand-500"
          />
          <span className="text-slate-700 text-sm">High Quality Graphics</span>
        </label>
      </div>

      {/* Export Button with Progress */}
      <div className="space-y-4">
        <button
          onClick={handleExport}
          disabled={exporting}
          className="w-full flex items-center justify-center gap-3 bg-brand-600 text-white px-6 py-4 rounded-lg font-bold text-lg hover:bg-brand-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md shadow-brand-500/30"
        >
          {exporting ? (
            <>
              <Clock className="animate-spin" size={20} />
              <span>Generating PDF ({progress}%)</span>
            </>
          ) : (
            <>
              <Download size={20} />
              <span>Export to PDF</span>
            </>
          )}
        </button>

        {exporting && (
          <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div
              className="bg-brand-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}

        {/* Report Features */}
        <div className="border-t border-slate-100 pt-6">
          <h4 className="font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <ShieldCheck size={16} /> What's included:
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Check size={14} className="text-green-500" /> Executive Summary
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Check size={14} className="text-green-500" /> Detailed Scores
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Check size={14} className="text-green-500" /> AI Recruiter Insights
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <BarChart size={14} /> Visual Charts
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <FileText size={14} /> Improvement Plans
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <ShieldCheck size={14} /> Professional Formatting
            </div>
          </div>
        </div>

        {/* Format Information */}
        <div className="text-xs text-slate-500 italic mt-4">
          Report is generated in A4 format suitable for job applications and portfolio reviews.
          File name: InterviewSignal_YourName_YYYY-MM-DD.pdf
        </div>
      </div>
    </div>
  );
};

export default PDFExporter;
