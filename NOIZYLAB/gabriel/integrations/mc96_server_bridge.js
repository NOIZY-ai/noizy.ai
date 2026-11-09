/**
 * MC96 SERVER BRIDGE
 * Connects GABRIEL to localhost:5174 backend
 * Real-time graph scanning and family summoning
 * ===========================================
 */

class MC96ServerBridge {
    constructor() {
        this.apiBase = 'http://localhost:5174';
        this.connected = false;
        this.wsConnection = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.graphCache = null;

        console.log('[MC96_SERVER] Bridge initializing...');
    }

    /**
     * Check server connection
     */
    async connect() {
        console.log('[MC96_SERVER] Connecting to localhost:5174...');

        try {
            const response = await fetch(`${this.apiBase}/api/status`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                this.connected = true;
                this.reconnectAttempts = 0;

                console.log('[MC96_SERVER] ✅ Connected to backend');
                console.log('[MC96_SERVER] Status:', data);

                this.broadcastEvent({
                    type: 'SERVER_CONNECTED',
                    message: '✅ MC96 backend server online',
                    status: data
                });

                // Initialize WebSocket for real-time updates
                this.connectWebSocket();

                return data;
            }
        } catch (error) {
            console.warn('[MC96_SERVER] Backend not available:', error.message);
            this.connected = false;

            // Auto-retry connection
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.reconnectAttempts++;
                console.log(`[MC96_SERVER] Retry ${this.reconnectAttempts}/${this.maxReconnectAttempts} in 3s...`);
                setTimeout(() => this.connect(), 3000);
            }
        }

        return null;
    }

    /**
     * Connect WebSocket for real-time updates
     */
    connectWebSocket() {
        try {
            const wsUrl = this.apiBase.replace('http', 'ws') + '/ws';
            this.wsConnection = new WebSocket(wsUrl);

            this.wsConnection.onopen = () => {
                console.log('[MC96_SERVER] WebSocket connected');
                this.broadcastEvent({
                    type: 'WEBSOCKET_CONNECTED',
                    message: '⚡ Real-time updates active'
                });
            };

            this.wsConnection.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };

            this.wsConnection.onclose = () => {
                console.log('[MC96_SERVER] WebSocket disconnected');
                // Auto-reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };

            this.wsConnection.onerror = (error) => {
                console.warn('[MC96_SERVER] WebSocket error:', error);
            };
        } catch (error) {
            console.warn('[MC96_SERVER] WebSocket not supported:', error.message);
        }
    }

    /**
     * Handle WebSocket messages
     */
    handleWebSocketMessage(data) {
        console.log('[MC96_SERVER] WebSocket message:', data);

        switch (data.type) {
            case 'SCAN_PROGRESS':
                this.broadcastEvent({
                    type: 'SCAN_UPDATE',
                    message: `Scanning: ${data.progress}%`,
                    data
                });
                break;

            case 'NODE_DISCOVERED':
                this.broadcastEvent({
                    type: 'NEW_NODE',
                    message: `New node discovered: ${data.node.label}`,
                    data
                });
                break;

            case 'GRAPH_UPDATED':
                this.broadcastEvent({
                    type: 'GRAPH_REFRESH',
                    message: 'Graph data updated',
                    data
                });
                break;
        }
    }

    /**
     * Trigger Fast Scan (Lite Graph ~200 nodes)
     */
    async fastScan() {
        console.log('[MC96_SERVER] ⚡ Triggering FAST SCAN...');

        try {
            const response = await fetch(`${this.apiBase}/api/memcell/graph/lite`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                this.graphCache = data;

                this.broadcastEvent({
                    type: 'FAST_SCAN_COMPLETE',
                    message: `⚡ Fast scan complete - ${data.nodes?.length || 0} nodes loaded`,
                    data
                });

                return data;
            }
        } catch (error) {
            console.error('[MC96_SERVER] Fast scan failed:', error);
        }

        return null;
    }

    /**
     * Trigger Deep Scan (Full Graph 35K+ nodes)
     */
    async deepScan(limit = 500) {
        console.log('[MC96_SERVER] 🔥 Triggering DEEP SCAN...');

        try {
            // First trigger the Go scanner
            const scanResponse = await fetch(`${this.apiBase}/api/scan/trigger`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (scanResponse.ok) {
                const scanData = await scanResponse.json();
                console.log('[MC96_SERVER] Scan triggered:', scanData);

                this.broadcastEvent({
                    type: 'DEEP_SCAN_STARTED',
                    message: '🔥 Deep scan initiated - Scanning 35,000+ nodes...',
                    data: scanData
                });

                // Wait a moment for scan to process
                await new Promise(resolve => setTimeout(resolve, 2000));

                // Now fetch the full graph
                const graphResponse = await fetch(
                    `${this.apiBase}/api/memcell/graph?limit=${limit}&t=${Date.now()}`,
                    { headers: { 'Accept': 'application/json' } }
                );

                if (graphResponse.ok) {
                    const data = await graphResponse.json();
                    this.graphCache = data;

                    this.broadcastEvent({
                        type: 'DEEP_SCAN_COMPLETE',
                        message: `✓ Deep scan complete - ${data.nodes?.length || 0} nodes loaded`,
                        data
                    });

                    return data;
                }
            }
        } catch (error) {
            console.error('[MC96_SERVER] Deep scan failed:', error);

            this.broadcastEvent({
                type: 'DEEP_SCAN_FAILED',
                message: '⚠️ Scan failed - Loading cached data',
                error: error.message
            });
        }

        return null;
    }

    /**
     * Summon Family - Focus on GABRIEL and family nodes
     */
    async summonFamily() {
        console.log('[MC96_SERVER] 🌟 SUMMONING FAMILY...');

        const familyNodes = ['GABRIEL', 'SHIRL', 'ENGR_KEITH', 'OMEGA', 'MC96UNIVERSE'];

        try {
            // Get current graph data
            const graphData = this.graphCache || await this.fastScan();

            // Find family members
            const family = graphData.nodes?.filter(node =>
                familyNodes.includes(node.id) || familyNodes.includes(node.label)
            ) || [];

            this.broadcastEvent({
                type: 'FAMILY_SUMMONED',
                message: `🌟 Family summoned - ${family.length} members found`,
                family
            });

            return family;
        } catch (error) {
            console.error('[MC96_SERVER] Summon failed:', error);
        }

        return [];
    }

    /**
     * Search for specific node
     */
    async searchNode(query) {
        console.log('[MC96_SERVER] 🔍 Searching for:', query);

        try {
            const response = await fetch(
                `${this.apiBase}/api/memcell/search?q=${encodeURIComponent(query)}`,
                { headers: { 'Accept': 'application/json' } }
            );

            if (response.ok) {
                const data = await response.json();

                this.broadcastEvent({
                    type: 'SEARCH_COMPLETE',
                    message: `Found ${data.results?.length || 0} matches for "${query}"`,
                    data
                });

                return data;
            }
        } catch (error) {
            console.error('[MC96_SERVER] Search failed:', error);
        }

        return null;
    }

    /**
     * Get node details
     */
    async getNodeDetails(nodeId) {
        try {
            const response = await fetch(
                `${this.apiBase}/api/memcell/node/${encodeURIComponent(nodeId)}`,
                { headers: { 'Accept': 'application/json' } }
            );

            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('[MC96_SERVER] Failed to get node details:', error);
        }

        return null;
    }

    /**
     * Get system stats
     */
    async getStats() {
        try {
            const response = await fetch(`${this.apiBase}/api/stats`, {
                headers: { 'Accept': 'application/json' }
            });

            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error('[MC96_SERVER] Failed to get stats:', error);
        }

        return null;
    }

    /**
     * Send command to MC96 server
     */
    async sendCommand(command, params = {}) {
        console.log('[MC96_SERVER] Sending command:', command);

        try {
            const response = await fetch(`${this.apiBase}/api/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, params })
            });

            if (response.ok) {
                const data = await response.json();

                this.broadcastEvent({
                    type: 'COMMAND_EXECUTED',
                    message: `Command executed: ${command}`,
                    data
                });

                return data;
            }
        } catch (error) {
            console.error('[MC96_SERVER] Command failed:', error);
        }

        return null;
    }

    /**
     * Get cached graph data
     */
    getCachedGraph() {
        return this.graphCache;
    }

    /**
     * Get connection status
     */
    getStatus() {
        return {
            connected: this.connected,
            apiBase: this.apiBase,
            wsConnected: this.wsConnection?.readyState === WebSocket.OPEN,
            hasCachedGraph: !!this.graphCache,
            cacheNodeCount: this.graphCache?.nodes?.length || 0,
            reconnectAttempts: this.reconnectAttempts
        };
    }

    /**
     * Broadcast event
     */
    broadcastEvent(event) {
        console.log(`[MC96_SERVER] ${event.type}:`, event.message || event);

        if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('mc96_server_event', { detail: event }));
        }

        // Also notify Slack if connected
        if (window.SLACK_BRIDGE?.connected) {
            if (event.type.includes('SCAN_COMPLETE') || event.type === 'FAMILY_SUMMONED') {
                window.SLACK_BRIDGE.sendMessage('mc96-control', event.message, {
                    emoji: ':mag:'
                });
            }
        }
    }

    /**
     * Disconnect
     */
    disconnect() {
        if (this.wsConnection) {
            this.wsConnection.close();
        }
        this.connected = false;
        console.log('[MC96_SERVER] Disconnected');
    }
}

// Initialize and export
if (typeof window !== 'undefined') {
    window.MC96_SERVER = new MC96ServerBridge();

    // Auto-connect on load
    window.MC96_SERVER.connect();

    console.log('[MC96_SERVER] Bridge ready');
    console.log('[MC96_SERVER] Available commands:');
    console.log('  - MC96_SERVER.fastScan()');
    console.log('  - MC96_SERVER.deepScan()');
    console.log('  - MC96_SERVER.summonFamily()');
    console.log('  - MC96_SERVER.searchNode(query)');
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MC96ServerBridge;
}
