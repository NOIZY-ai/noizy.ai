/**
 * DSP CHAIN
 * Defines FFmpeg filter graphs for the personas.
 */

export interface DSPChain {
    id: string;
    name: string;
    ffmpegFilter: string; // The audio filter graph string
}

export const DSP_INTENTIONS: DSPChain[] = [
    {
        id: "titan",
        name: "Thunder Titan",
        ffmpegFilter: "bass=g=10:f=50,compand=attacks=0:points=-80/-900|-12/-15|-6/-9|0/-7|20/-7:gain=5",
    },
    {
        id: "solar",
        name: "Solar Sentinel",
        ffmpegFilter: "treble=g=5:f=4000,acompressor=threshold=-12dB:ratio=2:makeup=2dB",
    },
    {
        id: "void",
        name: "Void Ranger",
        ffmpegFilter: "highpass=f=200,lowpass=f=3000,echo=0.8:0.9:1000:0.3",
    },
    {
        id: "architect",
        name: "Mythic Architect",
        ffmpegFilter: "firequalizer=gain='if(gte(f,1000),0,-5)',compand=attacks=0:points=-80/-900|-12/-15|-6/-9|0/-7|20/-7:gain=2",
    },
    {
        id: "raw",
        name: "Raw (No Processing)",
        ffmpegFilter: "anull",
    }
];
