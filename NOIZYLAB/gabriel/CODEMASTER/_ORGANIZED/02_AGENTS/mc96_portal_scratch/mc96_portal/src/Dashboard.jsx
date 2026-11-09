import React, { useState, useEffect, useRef } from 'react';

const Dashboard = () => {
    const [status, setStatus] = useState(null);
    const [memories, setMemories] = useState([]);
    const [cmdInput, setCmdInput] = useState('');
    const [cmdOutput, setCmdOutput] = useState('');
    const memoriesEndRef = useRef(null);

    const fetchStatus = async () => {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();
            setStatus(data);
        } catch (e) {
            console.error(e);
        }
    };

    const fetchMemories = async () => {
        try {
            const res = await fetch('/api/memory');
            const data = await res.json();
            // Sort by timestamp desc
            setMemories(data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)));
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {
        fetchStatus();
        fetchMemories();
        const interval = setInterval(() => {
            fetchStatus();
            fetchMemories();
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    const handleCommand = async (e) => {
        e.preventDefault();
        const content = cmdInput.trim();
        if (!content) return;

        // Simple parsing: if starts with "sys:", treat as console command (mocked for now)
        // Otherwise treat as a thought/memory
        
        try {
            const res = await fetch('/api/memory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    content: content,
                    type: 'THOUGHT',
                    author: 'MC96_ADMIN',
                    topic: 'Portal Input'
                })
            });
            const data = await res.json();
            if (data.success) {
                setCmdOutput(`> Thought injected: ${content}`);
                setCmdInput('');
                fetchMemories();
            } else {
                setCmdOutput(`> ERROR: ${data.error}`);
            }
        } catch (err) {
            setCmdOutput(`> NETWORK ERROR: ${err.message}`);
        }
    };

    return (
        <div className="min-h-screen bg-[#050505] text-[#e0e0e0] p-6 font-mono selection:bg-green-500/30">
            {/* Header */}
            <header className="flex justify-between items-center mb-8 border-b border-white/10 pb-4">
                <h1 className="text-2xl font-bold tracking-widest text-green-500 neon-text">
                    MC96 <span className="text-white">MISSION CONTROL</span>
                </h1>
                <div className="flex gap-4 text-xs">
                    <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${status ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
                        LINK: {status ? 'ESTABLISHED' : 'OFFLINE'}
                    </div>
                    <div className="text-white/50">{new Date().toLocaleTimeString()}</div>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 h-[calc(100vh-140px)]">
                
                {/* Left Column: Status (4 cols) */}
                <div className="md:col-span-4 flex flex-col gap-6">
                    {/* Status Panel */}
                    <div className="planar-panel flex-1">
                        <div className="planar-header">System Status</div>
                        {status ? (
                            <div className="space-y-4">
                                <div className="flex justify-between border-b border-white/5 pb-2">
                                    <span className="text-white/60">MODE</span>
                                    <span className="text-green-400 font-bold">{status.status}</span>
                                </div>
                                <div className="flex justify-between border-b border-white/5 pb-2">
                                    <span className="text-white/60">LATENCY</span>
                                    <span className="text-cyan-400 font-bold">{status.latency}</span>
                                </div>
                                <div>
                                    <div className="text-white/60 mb-2">AGENTS</div>
                                    <div className="grid grid-cols-3 gap-2">
                                        {Object.entries(status.agents || {}).map(([key, val]) => (
                                            <div key={key} className="bg-white/5 p-2 rounded text-center">
                                                <div className="text-[10px] text-white/40">{key}</div>
                                                <div className="text-xs text-green-300">{val}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="text-red-500 animate-pulse">CONNECTING...</div>
                        )}
                    </div>

                     {/* Command Center */}
                     <div className="planar-panel h-1/3 flex flex-col">
                        <div className="planar-header">Command Input</div>
                        <div className="flex-1 font-mono text-xs text-green-500/80 p-2 overflow-y-auto whitespace-pre-wrap">
                            {cmdOutput}
                        </div>
                        <form onSubmit={handleCommand} className="mt-2">
                            <input 
                                type="text" 
                                className="console-input"
                                placeholder="ENTER COMMAND OR THOUGHT..."
                                value={cmdInput}
                                onChange={(e) => setCmdInput(e.target.value)}
                                autoFocus
                            />
                        </form>
                    </div>
                </div>

                {/* Right Column: MemCell Matrix (8 cols) */}
                <div className="md:col-span-8 flex flex-col h-full">
                    <div className="planar-panel h-full flex flex-col overflow-hidden">
                        <div className="planar-header flex justify-between">
                            <span>MemCell Matrix</span>
                            <span className="text-green-500">{memories.length} RECORDS</span>
                        </div>
                        <div className="flex-1 overflow-y-auto pr-2 space-y-2 scroll-hide">
                            {memories.map((mem) => (
                                <div key={mem.id} className="bg-white/5 p-3 rounded border-l-2 border-white/20 hover:border-green-500 hover:bg-white/10 transition-colors group">
                                    <div className="flex justify-between items-start mb-1">
                                        <div className="flex gap-2 items-center">
                                            <span className="text-xs font-bold text-cyan-400 bg-cyan-900/20 px-1 rounded">
                                                {mem.type || 'MEMORY'}
                                            </span>
                                            <span className="text-[10px] text-white/40 uppercase tracking-wider">
                                                {mem.topic}
                                            </span>
                                        </div>
                                        <span className="text-[10px] text-white/30 font-mono">
                                            {formatTime(mem.timestamp)}
                                        </span>
                                    </div>
                                    <div className="text-sm text-gray-300 group-hover:text-white leading-relaxed">
                                        {mem.content}
                                    </div>
                                    <div className="mt-2 flex gap-2 justify-between items-center">
                                        <div className="flex gap-1">
                                            {mem.tags?.map(t => (
                                                <span key={t} className="text-[9px] bg-white/5 px-1 rounded text-white/40">#{t}</span>
                                            ))}
                                        </div>
                                        <div className="text-[9px] text-green-500/50">
                                            ID: {mem.id.slice(0, 8)} | AUTH: {mem.author}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Helper for time
function formatTime(iso) {
    if (!iso) return '';
    const date = new Date(iso);
    return date.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

export default Dashboard;
