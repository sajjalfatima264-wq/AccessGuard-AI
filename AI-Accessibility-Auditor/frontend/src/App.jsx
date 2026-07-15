import { useState } from 'react';

// --- Icons ---
const SparklesIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
    <path d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.894.553l1.382 2.764 2.764 1.382a1 1 0 010 1.788l-2.764 1.382-1.382 2.764a1 1 0 01-1.788 0l-1.382-2.764-2.764-1.382a1 1 0 010-1.788l2.764-1.382L11.106 2.553A1 1 0 0112 2z" />
  </svg>
);

const CopyIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
    <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
    <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
  </svg>
);

const CheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
  </svg>
);

// --- Components ---
const Loader = () => (
  <div className="flex flex-col items-center justify-center py-20 space-y-6">
    <div className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
    <div className="text-center">
      <p className="text-white text-lg font-semibold">Initializing AccessGuard AI...</p>
      <p className="text-gray-500 text-sm mt-2">Crawling DOM • Running WCAG Rules • Generating Insights</p>
    </div>
  </div>
);

const CodeBlock = ({ code }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group">
      <button
        onClick={handleCopy}
        className="absolute top-3 right-3 flex items-center gap-1.5 text-xs font-medium text-gray-400 bg-gray-800/80 hover:bg-gray-700 px-2.5 py-1.5 rounded-md transition-colors border border-gray-700"
      >
        {copied ? <CheckIcon /> : <CopyIcon />}
        {copied ? 'Copied!' : 'Copy'}
      </button>
      <pre className="bg-black/60 p-4 rounded-lg border border-gray-800 font-mono text-xs text-green-300 whitespace-pre-wrap overflow-x-auto max-h-64">
        {code}
      </pre>
    </div>
  );
};

const IssueCard = ({ issue }) => {
  const [isOpen, setIsOpen] = useState(false);

  const severityConfig = {
    Critical: { border: 'border-l-rose-500', badge: 'bg-rose-500/10 text-rose-400 border-rose-500/30', dot: 'bg-rose-500' },
    High: { border: 'border-l-orange-500', badge: 'bg-orange-500/10 text-orange-400 border-orange-500/30', dot: 'bg-orange-500' },
    Medium: { border: 'border-l-amber-500', badge: 'bg-amber-500/10 text-amber-400 border-amber-500/30', dot: 'bg-amber-500' },
  };

  const config = severityConfig[issue.severity] || severityConfig.Medium;
  const ai = issue.ai;

  return (
    <div className={`bg-gray-900/50 rounded-xl border border-gray-800 ${config.border} border-l-4 transition-all hover:border-gray-700 hover:shadow-xl hover:shadow-black/20`}>
      <div
        className="p-5 cursor-pointer flex justify-between items-center gap-4"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="font-semibold text-white text-sm tracking-wide">{issue.type}</span>
            <span className="text-xs px-2 py-1 bg-gray-800/80 rounded-md font-mono text-gray-400 border border-gray-700/50">
              {issue.wcag_reference} • Level {issue.level}
            </span>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border flex items-center gap-1.5 ${config.badge}`}>
              <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`}></span>
              {issue.severity}
            </span>
          </div>
          <p className="text-sm text-gray-400">{issue.description}</p>
          <div className="flex items-center gap-4 text-xs text-gray-500 font-mono pt-1">
            <span>{issue.occurrences} occurrences</span>
            <span className="text-gray-700">|</span>
            <span className="truncate">First seen: {issue.elements[0]?.location || 'N/A'}</span>
          </div>
        </div>
        <button className="text-gray-500 hover:text-white transition-colors p-2 rounded-full hover:bg-gray-800">
          <svg className={`w-5 h-5 transform transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {isOpen && (
        <div className="px-5 pb-5 border-t border-gray-800/80 pt-5 space-y-6">
          {/* Technical Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h6 className="text-xs font-semibold text-gray-300 mb-2 uppercase tracking-wider">Affected Elements</h6>
              <div className="space-y-2 max-h-40 overflow-y-auto pr-2">
                {issue.elements.slice(0, 5).map((el, i) => (
                  <div key={i} className="text-xs font-mono text-gray-400 bg-black/40 p-2.5 rounded border border-gray-800 break-all">
                    {el.element}
                  </div>
                ))}
                {issue.elements.length > 5 && (
                  <p className="text-xs text-gray-600 italic pt-1">+ {issue.elements.length - 5} more elements</p>
                )}
              </div>
            </div>
          </div>

          {/* AI Explanation Section */}
          {ai && (
            <div className="relative rounded-xl p-[1px] bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
              <div className="bg-gray-900 rounded-xl p-5 space-y-4">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 bg-indigo-500/20 rounded-md text-indigo-400">
                    <SparklesIcon />
                  </div>
                  <h5 className="text-sm font-bold text-white tracking-wide">AI Insight Engine</h5>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-black/20 p-3 rounded-lg border border-gray-800">
                    <p className="text-xs font-semibold text-indigo-400 mb-1.5">Problem</p>
                    <p className="text-sm text-gray-300 leading-relaxed">{ai.problem}</p>
                  </div>
                  <div className="bg-black/20 p-3 rounded-lg border border-gray-800">
                    <p className="text-xs font-semibold text-purple-400 mb-1.5">User Impact</p>
                    <p className="text-sm text-gray-300 leading-relaxed italic">"{ai.impact_on_users}"</p>
                  </div>
                </div>

                <div className="bg-black/20 p-3 rounded-lg border border-gray-800">
                  <p className="text-xs font-semibold text-pink-400 mb-1.5">Recommended Solution</p>
                  <p className="text-sm text-gray-300 leading-relaxed">{ai.recommended_fix}</p>
                </div>

                {ai.code_example && ai.code_example !== 'N/A' && (
                  <div>
                    <p className="text-xs font-semibold text-gray-400 mb-2">Corrected Implementation</p>
                    <CodeBlock code={ai.code_example} />
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const StatCard = ({ label, count, severity }) => {
  const colors = {
    Critical: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    High: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
    Medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    Passed: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  };
  
  return (
    <div className={`p-5 rounded-xl border ${colors[severity]} flex flex-col justify-between min-h-[100px]`}>
      <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{label}</span>
      <span className={`text-4xl font-bold mt-2 ${colors[severity].split(' ')[0]}`}>{count}</span>
    </div>
  );
};

const CategoryCard = ({ name, data }) => {
  const score = data.score;
  const color = score >= 80 ? 'bg-emerald-500' : score >= 50 ? 'bg-orange-500' : 'bg-rose-500';
  const textColor = score >= 80 ? 'text-emerald-400' : score >= 50 ? 'text-orange-400' : 'text-rose-400';

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition-colors">
      <div className="flex justify-between items-start mb-3">
        <span className="text-sm font-medium text-gray-300 capitalize">{name}</span>
        <span className={`text-lg font-bold ${textColor}`}>{score}%</span>
      </div>
      <div className="w-full bg-gray-800 rounded-full h-2 mb-3">
        <div className={`h-full rounded-full ${color} transition-all duration-1000`} style={{ width: `${score}%` }}></div>
      </div>
      <div className="flex justify-between text-xs text-gray-500 font-mono">
        <span>{data.total} Checks</span>
        <span>{data.total - (data.failed || 0)} Passed</span>
      </div>
    </div>
  );
};

const EmptyState = () => (
  <div className="text-center py-16 bg-gray-900/30 border border-gray-800 border-dashed rounded-xl">
    <div className="inline-flex items-center justify-center w-16 h-16 bg-emerald-500/10 rounded-full mb-4 border border-emerald-500/20">
      <CheckIcon />
    </div>
    <h3 className="text-xl font-semibold text-white mb-2">All Clear!</h3>
    <p className="text-gray-500 max-w-sm mx-auto">No issues match this filter. The website has passed all detected accessibility checks for this severity level.</p>
  </div>
);

const HomeView = ({ url, setUrl, loading, onScan }) => (
  <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 py-10">
    <div className="text-center mb-12 max-w-3xl">
      <div className="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 rounded-full px-4 py-1.5 mb-6">
        <SparklesIcon />
        <span className="text-indigo-300 text-sm font-medium">AI-Powered Accessibility Auditing</span>
      </div>
      <h1 className="text-5xl md:text-6xl font-black text-white mb-6 leading-tight tracking-tight">
        AccessGuard <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">AI</span>
      </h1>
      <p className="text-lg text-gray-400 leading-relaxed max-w-2xl mx-auto">
        Don't just find errors — understand them. Identify WCAG violations, view their impact on disabled users, and generate precise code fixes instantly.
      </p>
    </div>
    <form
      onSubmit={onScan}
      className="w-full max-w-2xl flex flex-col sm:flex-row gap-2 bg-gray-900 border border-gray-800 rounded-2xl p-2 shadow-2xl shadow-indigo-500/10"
    >
      <input
        type="text"
        placeholder="Enter URL to audit (e.g., https://example.com)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="flex-1 px-6 py-4 bg-transparent text-white text-lg placeholder-gray-600 focus:outline-none"
        disabled={loading}
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold text-lg transition-colors disabled:bg-gray-700 whitespace-nowrap text-white shadow-lg shadow-indigo-500/20"
      >
        {loading ? 'Analyzing...' : 'Run Audit'}
      </button>
    </form>
    <div className="flex gap-6 mt-10 text-xs text-gray-600">
      <span>WCAG 2.1 Compliant</span>
      <span>•</span>
      <span>AI Insight Engine</span>
      <span>•</span>
      <span>Instant Fixes</span>
    </div>
  </div>
);

const ReportView = ({ data, onReset }) => {
  const [filter, setFilter] = useState('All');
  const { report, scan_id, url } = data;
  
  const scoreColor = report.score.overall >= 80 ? 'text-emerald-400' : report.score.overall >= 50 ? 'text-orange-400' : 'text-rose-400';
  const scoreBg = report.score.overall >= 80 ? 'from-emerald-500/10' : report.score.overall >= 50 ? 'from-orange-500/10' : 'from-rose-500/10';

  const counts = {
    Critical: report.issues.filter(i => i.severity === 'Critical').reduce((a, b) => a + b.occurrences, 0),
    High: report.issues.filter(i => i.severity === 'High').reduce((a, b) => a + b.occurrences, 0),
    Medium: report.issues.filter(i => i.severity === 'Medium').reduce((a, b) => a + b.occurrences, 0),
  };

  const filteredIssues = filter === 'All' ? report.issues : report.issues.filter(i => i.severity === filter);
  const totalChecks = Object.values(report.score.categories).reduce((a, b) => a + b.total, 0);
  const totalFailed = report.issues.reduce((a, b) => a + b.occurrences, 0);
  const totalPassed = totalChecks - totalFailed;

  return (
    <div className="max-w-7xl mx-auto pb-20">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 border-b border-gray-800 pb-6">
        <div>
          <button onClick={onReset} className="text-gray-500 hover:text-white transition-colors flex items-center gap-2 text-sm mb-2">
            ← Run New Audit
          </button>
          <h1 className="text-2xl font-bold text-white">Audit Report</h1>
          <p className="text-gray-500 text-sm font-mono mt-1 truncate max-w-md">{url}</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
          <span className="text-emerald-400 text-xs font-medium">Audit Complete</span>
        </div>
      </div>

      {/* Summary Section */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
        {/* Score Card */}
        <div className={`lg:col-span-1 bg-gradient-to-br ${scoreBg} to-gray-900 border border-gray-800 rounded-2xl p-6 flex flex-col items-center justify-center text-center`}>
          <p className="text-xs text-gray-400 font-medium uppercase tracking-wider mb-3">Overall Score</p>
          <p className={`text-7xl font-black ${scoreColor}`}>{report.score.overall}</p>
          <div className="mt-4 pt-4 border-t border-gray-800 w-full">
            <p className="text-sm text-gray-400 font-medium">
              <span className="text-white">{totalPassed}</span> of <span className="text-white">{totalChecks}</span> checks passed
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard label="Critical Issues" count={counts.Critical} severity="Critical" />
          <StatCard label="High Issues" count={counts.High} severity="High" />
          <StatCard label="Medium Issues" count={counts.Medium} severity="Medium" />
          
          {/* Categories */}
          <div className="sm:col-span-3 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-2">
            {Object.entries(report.score.categories).map(([key, val]) => (
              <CategoryCard key={key} name={key} data={val} />
            ))}
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex justify-between items-center mb-6 flex-wrap gap-4 border-b border-gray-800 pb-4">
        <div className="flex gap-2 p-1 bg-gray-900 rounded-lg border border-gray-800">
          {['All', 'Critical', 'High', 'Medium'].map((sev) => {
            const count = sev === 'All' ? report.issues.length : report.issues.filter(i => i.severity === sev).length;
            return (
              <button
                key={sev}
                onClick={() => setFilter(sev)}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all flex items-center gap-2 ${
                  filter === sev ? 'bg-gray-800 text-white shadow-sm' : 'text-gray-400 hover:text-white'
                }`}
              >
                {sev}
                <span className={`text-xs px-1.5 py-0.5 rounded-full ${filter === sev ? 'bg-indigo-500/20 text-indigo-300' : 'bg-gray-800 text-gray-500'}`}>
                  {count}
                </span>
              </button>
            );
          })}
        </div>
        <span className="text-xs text-gray-600 font-mono">Scan ID: {scan_id}</span>
      </div>

      {/* Issue List */}
      <div className="space-y-4">
        {filteredIssues.length === 0 ? (
          <EmptyState />
        ) : (
          filteredIssues.map((issue) => <IssueCard key={issue.id} issue={issue} />)
        )}
      </div>
    </div>
  );
};

export default function App() {
  const [view, setView] = useState('home');
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!url) return;
    setLoading(true);
    setResult(null);
    setError(null);
    setView('home');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "An unknown error occurred.");
      setResult(data);
      setView('report');
    } catch (err) {
      setError(err.message || "Failed to connect to the backend server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0b] text-white flex flex-col">
      <nav className="border-b border-gray-800/80 bg-[#0a0a0b]/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center h-16">
          <h2
            className="text-lg font-bold text-white tracking-tight cursor-pointer flex items-center gap-2"
            onClick={() => { setView('home'); setError(null); setResult(null); }}
          >
            <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">AccessGuard AI</span>
          </h2>
          {view === 'report' && !loading && (
            <span className="text-xs font-mono text-emerald-400 bg-emerald-900/20 px-3 py-1 rounded-full border border-emerald-800/50">
              Report Ready
            </span>
          )}
        </div>
      </nav>

      <main className="flex-1 px-6 py-8 w-full">
        {loading && <Loader />}
        
        {error && !loading && (
          <div className="max-w-2xl mx-auto mt-10 p-6 bg-rose-900/20 border border-rose-800 rounded-xl text-center">
            <p className="font-bold text-lg text-rose-300 mb-2">Audit Failed</p>
            <p className="text-rose-400/80 break-words">{error}</p>
            <button onClick={() => setError(null)} className="mt-4 text-sm text-rose-500 hover:text-rose-300 underline">
              Dismiss
            </button>
          </div>
        )}
        
        {!loading && !error && view === 'home' && (
          <HomeView url={url} setUrl={setUrl} loading={loading} onScan={handleScan} />
        )}
        
        {!loading && !error && view === 'report' && result && (
          <ReportView data={result} onReset={() => setView('home')} />
        )}
      </main>

      <footer className="border-t border-gray-800/80 py-6 text-center text-xs text-gray-600">
        AccessGuard AI — AI-Ready Accessibility Auditing Platform
      </footer>
    </div>
  );
}