export type GabrielStatus = "IDLE" | "LISTENING" | "PROCESSING" | "SPEAKING";

export interface GabrielStateSchema {
    status: GabrielStatus;
    audioLevel: number; // 0.0 to 1.0 (Reactive Ring)
    viseme: string;     // Phoneme for Lip Sync (e.g., "A", "O", "MP")
    lastActive: string; // ISO Timestamp
}

export class GabrielState {
    private state: GabrielStateSchema;
    private listeners: ((s: GabrielStateSchema) => void)[] = [];

    constructor() {
        this.state = {
            status: "IDLE",
            audioLevel: 0.0,
            viseme: "SIL",
            lastActive: new Date().toISOString(),
        };
    }

    // --- TRANSITIONS ---

    public setStatus(status: GabrielStatus) {
        if (this.state.status === status) return;
        console.log(`[GabrielState] Transition: ${this.state.status} -> ${status}`);
        this.state.status = status;
        this.state.lastActive = new Date().toISOString();
        this.notify();
    }

    public setAudioLevel(level: number) {
        // Clamp 0-1
        this.state.audioLevel = Math.max(0, Math.min(1, level));
        this.notify();
    }

    public setViseme(viseme: string) {
        this.state.viseme = viseme;
        this.notify();
    }

    // --- PUB/SUB ---

    public subscribe(callback: (s: GabrielStateSchema) => void) {
        this.listeners.push(callback);
        callback(this.state); // Initial emit
        return () => {
            this.listeners = this.listeners.filter((l) => l !== callback);
        };
    }

    private notify() {
        this.listeners.forEach((l) => l(this.state));
    }
}

// Global Singleton Instance
export const gabriel = new GabrielState();
