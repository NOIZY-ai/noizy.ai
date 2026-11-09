/**
 * NOIZYVOX GUILD MANAGEMENT
 * Handles Artist Profiles, Licensing, and the 75/25 Royalty Logic.
 */

export interface ArtistProfile {
    id: string;
    name: string;
    ethWallet?: string; // For crypto payouts
    stripeId?: string;  // For fiat payouts
    status: 'active' | 'suspended';
    agreementVersion: string; // Tracks which 'Charter' version they signed
}

export interface RoyaltySplit {
    artistId: string;
    totalAmountUSD: number;
    artistShare: number; // 75%
    platformShare: number; // 25%
    timestamp: string;
    transactionId: string;
}

export class GuildManager {
    private ARTIST_SHARE_PERCENTAGE = 0.75;

    constructor(private db: D1Database) { }

    /**
     * Calculates the split for a given usage event.
     * @param amountUSD Total transaction amount
     */
    calculateSplit(amountUSD: number): { artist: number, platform: number } {
        const artist = amountUSD * this.ARTIST_SHARE_PERCENTAGE;
        const platform = amountUSD - artist;
        return {
            artist: Number(artist.toFixed(4)),
            platform: Number(platform.toFixed(4))
        };
    }

    /**
     * Records a usage event and allocates royalties.
     */
    async recordUsage(artistId: string, amountUSD: number, metadata: any) {
        const split = this.calculateSplit(amountUSD);
        const splitRecord: RoyaltySplit = {
            artistId,
            totalAmountUSD: amountUSD,
            artistShare: split.artist,
            platformShare: split.platform,
            timestamp: new Date().toISOString(),
            transactionId: crypto.randomUUID()
        };

        // Store in D1 Database (Pseudo-code query)
        await this.db.prepare(`
        INSERT INTO royalties (id, artist_id, artist_share, platform_share, meta)
        VALUES (?, ?, ?, ?, ?)
    `).bind(
            splitRecord.transactionId,
            splitRecord.artistId,
            splitRecord.artistShare,
            splitRecord.platformShare,
            JSON.stringify(metadata)
        ).run();

        return splitRecord;
    }

    /**
     * D1 Schema Definition (Run this to init DB)
     */
    static getSchemaSQL() {
        return `
      CREATE TABLE IF NOT EXISTS artists (
        id TEXT PRIMARY KEY,
        name TEXT,
        wallet TEXT,
        status TEXT,
        joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE IF NOT EXISTS royalties (
        id TEXT PRIMARY KEY,
        artist_id TEXT,
        artist_share REAL,
        platform_share REAL,
        meta TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
    `;
    }
}
