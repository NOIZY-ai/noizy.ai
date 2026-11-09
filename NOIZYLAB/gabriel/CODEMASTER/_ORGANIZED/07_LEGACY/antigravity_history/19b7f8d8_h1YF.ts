export interface Viseme {
    time: number;
    value: string; // Rhubarb mouth shape (A-H, X)
}

export class LipSyncEngine {
    // Config for local Docker service
    private encryptionKey: string;
    private serviceUrl: string;

    constructor(serviceUrl: string = "http://localhost:8080") {
        this.serviceUrl = serviceUrl;
        this.encryptionKey = "Placeholder";
    }

    /**
     * Sends audio to the local Rhubarb Docker container and returns Viseme JSON.
     */
    async generateVisemes(audioBuffer: ArrayBuffer): Promise<Viseme[]> {
        // In a real implementation, we would POST the audio file to the local docker service.
        // The Docker service runs: `rhubarb -f json input.wav`

        console.log("Mocking Rhubarb Latency...");

        // Mock Response for Day 1 Demo
        return [
            { time: 0.00, value: "X" },
            { time: 0.05, value: "B" },
            { time: 0.20, value: "C" },
            { time: 0.45, value: "A" },
            { time: 0.80, value: "X" }
        ];
    }
}
