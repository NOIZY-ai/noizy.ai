/**
 * PATTERN_INTELLIGENCE.ts
 *
 * Description:
 * Real-time anomaly detection, frequency analysis, and behavioral prediction.
 * Learns from interactions and predicts future patterns.
 *
 * GOD MODE: ENABLED
 * STRICT MODE: ENABLED
 */

export interface Pattern {
    id: string;
    signature: string;
    confidence: number;
    frequency: number;
    lastDetected: number;
    metadata?: Record<string, unknown>;
}

interface PatternConfig {
    signature: string;
    threshold: number;
    detector: (input: unknown, context?: Record<string, unknown>) => boolean;
}

export class PatternIntelligence {
    private learnedPatterns: Map<string, Pattern>;
    private patternConfigs: PatternConfig[];
    private eventHistory: unknown[];
    private readonly MAX_HISTORY = 1000;

    constructor() {
        this.learnedPatterns = new Map();
        this.eventHistory = [];
        this.patternConfigs = [];
        this.initializeDefaultPatterns();
    }

    private initializeDefaultPatterns(): void {
        // Late night coding pattern
        this.learnedPatterns.set('p_late_night', {
            id: 'p_late_night',
            signature: 'late_night_coding',
            confidence: 0.9,
            frequency: 0,
            lastDetected: 0,
            metadata: { riskLevel: 'burnout' }
        });

        // High activity burst pattern
        this.learnedPatterns.set('p_burst', {
            id: 'p_burst',
            signature: 'activity_burst',
            confidence: 0.7,
            frequency: 0,
            lastDetected: 0,
            metadata: { type: 'productivity' }
        });

        // Error cascade pattern
        this.learnedPatterns.set('p_error_cascade', {
            id: 'p_error_cascade',
            signature: 'error_cascade',
            confidence: 0.8,
            frequency: 0,
            lastDetected: 0,
            metadata: { severity: 'high' }
        });

        // Configure pattern detectors
        this.patternConfigs = [
            {
                signature: 'late_night_coding',
                threshold: 0.7,
                detector: () => {
                    const hour = new Date().getHours();
                    return hour >= 23 || hour < 4;
                }
            },
            {
                signature: 'large_data_burst',
                threshold: 0.8,
                detector: (input) => {
                    if (typeof input === 'string') return input.length > 5000;
                    if (typeof input === 'object' && input !== null) {
                        return JSON.stringify(input).length > 10000;
                    }
                    return false;
                }
            },
            {
                signature: 'rapid_requests',
                threshold: 0.6,
                detector: () => {
                    const recentEvents = this.eventHistory.slice(-10);
                    if (recentEvents.length < 5) return false;
                    // Check if 5+ events in last 10 seconds
                    const now = Date.now();
                    const recentCount = recentEvents.filter((e: unknown) => {
                        const event = e as { timestamp?: number };
                        return event.timestamp && now - event.timestamp < 10000;
                    }).length;
                    return recentCount >= 5;
                }
            }
        ];
    }

    public async analyzeContext(context: Record<string, unknown> | undefined): Promise<Pattern[]> {
        const detectedPatterns: Pattern[] = [];

        if (!context) return detectedPatterns;

        // Run all pattern detectors
        for (const config of this.patternConfigs) {
            if (config.detector(context, context)) {
                const pattern = this.getOrCreatePattern(config.signature);
                pattern.frequency++;
                pattern.lastDetected = Date.now();
                pattern.confidence = Math.min(0.99, pattern.confidence + 0.01);
                detectedPatterns.push(pattern);

                // Alert on high frequency patterns
                if (pattern.signature === 'late_night_coding' && pattern.frequency > 20) {
                    console.warn('[PatternIntelligence] High frequency late night activity. Burnout risk.');
                }
            }
        }

        return detectedPatterns;
    }

    public async detect(inputStream: unknown): Promise<Pattern[]> {
        const detected: Pattern[] = [];
        const timestamp = Date.now();

        // Record event
        this.recordEvent({ input: inputStream, timestamp });

        // Run detectors
        for (const config of this.patternConfigs) {
            if (config.detector(inputStream)) {
                const pattern = this.getOrCreatePattern(config.signature);
                pattern.frequency++;
                pattern.lastDetected = timestamp;
                detected.push({ ...pattern });
            }
        }

        return detected;
    }

    private getOrCreatePattern(signature: string): Pattern {
        const existing = Array.from(this.learnedPatterns.values())
            .find(p => p.signature === signature);

        if (existing) return existing;

        const newPattern: Pattern = {
            id: `p_${signature}_${Date.now()}`,
            signature,
            confidence: 0.5,
            frequency: 0,
            lastDetected: 0
        };

        this.learnedPatterns.set(newPattern.id, newPattern);
        return newPattern;
    }

    private recordEvent(event: unknown): void {
        this.eventHistory.push(event);
        if (this.eventHistory.length > this.MAX_HISTORY) {
            this.eventHistory.shift();
        }
    }

    public async learn(eventSequence: unknown[]): Promise<Pattern | null> {
        // Sequence mining for patterns
        if (eventSequence.length > 100) {
            const newPattern: Pattern = {
                id: `p_learned_${Date.now()}`,
                signature: 'recurrent_sequence',
                confidence: 0.5,
                frequency: 1,
                lastDetected: Date.now(),
                metadata: { learned: true, sequenceLength: eventSequence.length }
            };

            this.learnedPatterns.set(newPattern.id, newPattern);
            return newPattern;
        }
        return null;
    }

    public predictNextAction(currentChain: unknown[]): string {
        // Analyze recent events for prediction
        if (currentChain.length === 0) return 'CONTINUE';

        const patterns = Array.from(this.learnedPatterns.values());
        const lateNight = patterns.find(p => p.signature === 'late_night_coding');

        if (lateNight && lateNight.frequency > 10) {
            return 'SUGGEST_BREAK';
        }

        const burst = patterns.find(p => p.signature === 'activity_burst');
        if (burst && burst.frequency > 5) {
            return 'SUGGEST_REVIEW';
        }

        return 'CONTINUE';
    }

    public getPatterns(): Pattern[] {
        return Array.from(this.learnedPatterns.values());
    }

    public getPatternById(id: string): Pattern | undefined {
        return this.learnedPatterns.get(id);
    }

    public clearHistory(): void {
        this.eventHistory = [];
    }

    public getStats(): { patternCount: number; eventCount: number; topPatterns: Pattern[] } {
        const patterns = Array.from(this.learnedPatterns.values());
        const topPatterns = patterns
            .sort((a, b) => b.frequency - a.frequency)
            .slice(0, 5);

        return {
            patternCount: patterns.length,
            eventCount: this.eventHistory.length,
            topPatterns
        };
    }
}
