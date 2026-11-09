/**
 * NOIZYVOX TypeScript Type Definitions
 * Auto-generated from JSON Schema v1.0.0
 * 
 * These types provide full type safety for Persona Packs and Artifact Manifests
 */

// ============================================================================
// PERSONA PACK TYPES
// ============================================================================

export interface Artist {
  artist_id: `artist_${string}`;
  legal_name: string;
  stage_name?: string;
  guild_status: 'founding' | 'verified' | 'provisional' | 'suspended';
  verified_at: string; // ISO 8601 datetime
  verification_method?: 'id_document' | 'agent_attestation' | 'guild_vouched' | 'video_verification';
  contact_email?: string;
  payout_wallet?: string;
  estate_contact?: string;
}

export interface Prosody {
  pitch_base_hz?: number; // 50-500
  pitch_range_st?: number; // 0-24 semitones
  rate_wpm?: number; // 80-220
  volume_db?: number; // -12 to 6
  breathiness?: number; // 0-1
  warmth?: number; // 0-1
  articulation?: 'crisp' | 'relaxed' | 'theatrical' | 'intimate';
}

export interface EQSettings {
  low_cut_hz?: number; // 20-200
  low_shelf_hz?: number;
  low_shelf_gain_db?: number; // -12 to 12
  mid_freq_hz?: number;
  mid_gain_db?: number; // -12 to 12
  mid_q?: number; // 0.1-10
  high_shelf_hz?: number;
  high_shelf_gain_db?: number; // -12 to 12
  presence_freq_hz?: number;
  presence_gain_db?: number; // -12 to 12
}

export interface CompressorSettings {
  threshold_db?: number; // -60 to 0
  ratio?: number; // 1-20
  attack_ms?: number; // 0.1-100
  release_ms?: number; // 10-1000
  knee_db?: number; // 0-12
  makeup_gain_db?: number; // 0-24
}

export interface ReverbSettings {
  type?: 'studio' | 'cathedral' | 'live' | 'plate' | 'spring' | 'convolution';
  decay_s?: number; // 0.1-10
  predelay_ms?: number; // 0-100
  wet_dry_mix?: number; // 0-1
  diffusion?: number; // 0-1
  ir_url?: string; // URI for convolution impulse response
}

export interface LimiterSettings {
  ceiling_db?: number; // -3 to 0
  release_ms?: number; // 10-500
}

export interface DeEsserSettings {
  frequency_hz?: number; // 4000-10000
  threshold_db?: number; // -40 to 0
  reduction_db?: number; // 0-12
}

export interface DSPRecipe {
  eq: EQSettings;
  compressor: CompressorSettings;
  reverb: ReverbSettings;
  formant_shift_st?: number; // -12 to 12
  lufs_target: number; // -24 to -14
  limiter?: LimiterSettings;
  de_esser?: DeEsserSettings;
}

export interface HeadMotion {
  nod_intensity?: number; // 0-1
  sway_intensity?: number; // 0-1
  look_at_variance_deg?: number; // 0-15
}

export interface AnimationCues {
  rig_format?: 'arkit_52' | 'oculus_viseme' | 'nvidia_audio2face' | 'custom_blendshapes';
  viseme_map?: Record<string, number>; // Phoneme to viseme index (0-51)
  blend_shape_weights?: Record<string, number>; // 0-1
  blink_rate_hz?: number; // 0.1-0.5
  micro_expression_intensity?: number; // 0-1
  head_motion?: HeadMotion;
}

export interface RevocationPolicy {
  notice_period_days?: number; // 30-180
  existing_licenses_honored?: boolean;
  immediate_takedown_allowed?: boolean;
}

export type ContentRestriction = 
  | 'political' 
  | 'religious' 
  | 'adult' 
  | 'gambling' 
  | 'tobacco' 
  | 'alcohol' 
  | 'weapons' 
  | 'pharmaceutical';

export interface Consent {
  voice_capture_consent: boolean;
  ai_training_consent: boolean;
  commercial_use_consent: boolean;
  derivative_works_consent?: boolean;
  geographic_restrictions?: string[]; // ISO 3166-1 alpha-2
  content_restrictions?: ContentRestriction[];
  consent_timestamp: string; // ISO 8601
  consent_expiry?: string; // ISO 8601
  consent_document_url?: string;
  consent_hash: `sha256:${string}`;
  video_verification_url?: string;
  revocation_policy?: RevocationPolicy;
}

export interface Provenance {
  created_at: string; // ISO 8601
  updated_at?: string; // ISO 8601
  commit_hash: string; // 64 hex chars
  artifact_hash: `sha256:${string}`;
  parent_version?: string;
  fork_of?: string;
  training_data_manifest?: string;
  watermark_id?: `wm_${string}`;
  fingerprint_signature?: string;
}

export interface Pricing {
  micro_per_minute_usd?: number;
  non_exclusive_monthly_usd?: number;
  exclusive_buyout_usd?: number;
  enterprise_annual_usd?: number;
}

export interface RevenueSplit {
  artist_percent?: number; // 0-100, default 75
  platform_percent?: number; // 0-100, default 25
}

export type LicenseTier = 'micro' | 'non_exclusive' | 'exclusive' | 'enterprise';

export interface Licensing {
  available_tiers?: LicenseTier[];
  pricing?: Pricing;
  revenue_split?: RevenueSplit;
  exclusivity_lockup_days?: number; // 0-365
  minimum_payout_usd?: number; // default 25
}

export type ModelFormat = 'onnx' | 'pytorch' | 'tensorflow' | 'coreml' | 'tensorrt';
export type Quantization = 'fp32' | 'fp16' | 'int8' | 'int4';
export type SampleRate = 22050 | 44100 | 48000;

export interface ModelArtifact {
  format?: ModelFormat;
  size_bytes?: number;
  quantization?: Quantization;
  sample_rate_hz?: SampleRate;
  latency_ms?: number;
  edge_compatible?: boolean;
  download_url?: string;
  checksum?: `sha256:${string}`;
}

/**
 * Complete Persona Pack - the primary voice identity package
 */
export interface PersonaPack {
  persona_id: string; // 3-64 lowercase alphanumeric with underscores
  version: string; // Semantic version (e.g., "1.0.0")
  display_name: string; // Max 100 chars
  artist: Artist;
  archetype_tags: string[]; // 1-10 tags, max 32 chars each
  short_bio: string; // Max 500 chars
  recommended_prosody: Prosody;
  ssml_template: string;
  dsp_recipe: DSPRecipe;
  animation_cues: AnimationCues;
  consent: Consent;
  provenance: Provenance;
  licensing?: Licensing;
  model_artifact?: ModelArtifact;
}


// ============================================================================
// ARTIFACT MANIFEST TYPES
// ============================================================================

export type ArtifactType = 
  | 'audio_render' 
  | 'ssml_bundle' 
  | 'animation_track' 
  | 'persona_pack' 
  | 'dsp_preset' 
  | 'model_weights';

export interface Licensee {
  licensee_id?: string;
  organization?: string;
  email?: string;
  tier?: LicenseTier;
}

export type WatermarkMethod = 'spectral' | 'phase' | 'lsb' | 'neural';
export type RobustnessLevel = 'standard' | 'broadcast' | 'forensic';

export interface Watermark {
  watermark_id: `wm_${string}`;
  method: WatermarkMethod;
  embedded_at: string; // ISO 8601
  detection_endpoint?: string;
  robustness_level?: RobustnessLevel;
}

export type FingerprintAlgorithm = 'chromaprint' | 'dejavu' | 'panako' | 'audfprint';

export interface Fingerprint {
  algorithm?: FingerprintAlgorithm;
  fingerprint_hash?: string;
  duration_ms?: number;
  registered_at?: string; // ISO 8601
}

export interface InputScript {
  text?: string;
  text_hash?: `sha256:${string}`;
  language?: string; // e.g., "en-US"
  ssml_version?: string;
}

export type TargetEnvironment = 'studio' | 'cathedral' | 'live' | 'podcast' | 'broadcast';
export type BitDepth = 16 | 24 | 32;
export type AudioFormat = 'wav' | 'flac' | 'mp3' | 'aac' | 'opus';

export interface RenderParams {
  dsp_recipe_hash?: string;
  target_environment?: TargetEnvironment;
  sample_rate_hz?: number;
  bit_depth?: BitDepth;
  format?: AudioFormat;
}

export type AppealStatus = 'none' | 'pending' | 'approved' | 'rejected';

export interface Moderation {
  scanned_at?: string; // ISO 8601
  passed?: boolean;
  flags?: string[];
  reviewer_id?: string;
  appeal_status?: AppealStatus;
}

export interface UsageTracking {
  plays?: number;
  downloads?: number;
  api_calls?: number;
  last_accessed_at?: string; // ISO 8601
}

export interface GitCommit {
  repository?: string;
  branch?: string;
  commit_sha?: string; // 40 hex chars
  committed_at?: string; // ISO 8601
  author?: string;
}

export type BlockchainNetwork = 'ethereum' | 'polygon' | 'solana' | 'none';

export interface BlockchainAnchor {
  chain?: BlockchainNetwork;
  tx_hash?: string;
  block_number?: number;
  anchored_at?: string; // ISO 8601
}

export interface ImmutabilityProof {
  merkle_root?: string;
  blockchain_anchor?: BlockchainAnchor;
}

/**
 * Artifact Manifest - immutable provenance record for generated artifacts
 */
export interface ArtifactManifest {
  manifest_id: `mf_${string}`;
  version: string; // Semantic version
  created_at: string; // ISO 8601
  artifact_type: ArtifactType;
  persona_id: string;
  artist_id: `artist_${string}`;
  license_id: `lic_${string}`;
  licensee?: Licensee;
  content_hash: `sha256:${string}`;
  watermark: Watermark;
  fingerprint?: Fingerprint;
  input_script?: InputScript;
  render_params?: RenderParams;
  moderation?: Moderation;
  usage_tracking?: UsageTracking;
  git_commit?: GitCommit;
  immutability_proof?: ImmutabilityProof;
}


// ============================================================================
// UTILITY TYPES
// ============================================================================

/**
 * ID generation patterns
 */
export type PersonaId = string; // ^[a-z0-9_]{3,64}$
export type ArtistId = `artist_${string}`; // artist_ + 12 hex chars
export type LicenseId = `lic_${string}`; // lic_ + 16 hex chars
export type ManifestId = `mf_${string}`; // mf_ + 24 hex chars
export type WatermarkId = `wm_${string}`; // wm_ + 16 hex chars
export type SHA256Hash = `sha256:${string}`; // sha256: + 64 hex chars

/**
 * Validation result type
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings?: string[];
}

/**
 * API response wrapper
 */
export interface NoizyvoxResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  meta?: {
    request_id: string;
    timestamp: string;
    version: string;
  };
}


// ============================================================================
// SSML TYPES
// ============================================================================

/**
 * Emotion types supported in nvox:emotion elements
 */
export type SSMLEmotionType =
  | 'neutral'
  | 'joy'
  | 'sadness'
  | 'anger'
  | 'fear'
  | 'surprise'
  | 'disgust'
  | 'contempt'
  | 'awe'
  | 'tenderness'
  | 'determination'
  | 'mystery'
  | 'urgency'
  | 'serenity'
  | 'melancholy'
  | 'triumph';

/**
 * DSP effect types for nvox:dsp elements
 */
export type SSMLDSPEffect =
  | 'telephone'
  | 'radio'
  | 'megaphone'
  | 'stadium'
  | 'whisper'
  | 'shout'
  | 'robotic'
  | 'ethereal'
  | 'underwater'
  | 'cave'
  | 'cathedral'
  | 'intimate';

/**
 * Breath types for nvox:breath elements
 */
export type SSMLBreathType = 'short' | 'medium' | 'deep' | 'gasp' | 'sigh';

/**
 * Energy levels for nvox:energy elements
 */
export type SSMLEnergyLevel = 'whisper' | 'soft' | 'normal' | 'loud' | 'shout';

/**
 * Transition types for emotion/state changes
 */
export type SSMLTransition = 'instant' | 'ease-in' | 'ease-out' | 'crossfade';

/**
 * Attack types for energy dynamics
 */
export type SSMLAttack = 'slow' | 'normal' | 'fast';

/**
 * Built-in animation cue types
 */
export type SSMLAnimationCue =
  | 'eyebrow_raise'
  | 'eyebrow_furrow'
  | 'smile'
  | 'frown'
  | 'nod'
  | 'shake'
  | 'blink'
  | 'wink'
  | 'look_up'
  | 'look_down'
  | 'look_left'
  | 'look_right'
  | 'lean_in'
  | 'lean_back';

/**
 * Animation trigger points
 */
export type SSMLAnimateTrigger = 'start' | 'peak' | 'end';

/**
 * Parallel track sync modes
 */
export type SSMLParallelSync = 'start' | 'all' | 'first' | 'last';

/**
 * nvox:persona element attributes
 */
export interface SSMLPersonaElement {
  id: string;
  version?: string;
  blend?: number; // 0.0-1.0
}

/**
 * nvox:emotion element attributes
 */
export interface SSMLEmotionElement {
  type: SSMLEmotionType;
  intensity?: number; // 0.0-1.0, default 0.5
  transition?: SSMLTransition; // default 'instant'
  duration?: string; // e.g., '500ms', '1s'
}

/**
 * nvox:breath element attributes
 */
export interface SSMLBreathElement {
  type: SSMLBreathType;
  duration?: string; // e.g., '500ms'
  volume?: string; // e.g., '-6dB'
}

/**
 * nvox:dsp element attributes
 */
export interface SSMLDSPElement {
  effect: SSMLDSPEffect;
  wet?: number; // 0.0-1.0, dry/wet mix
  params?: Record<string, unknown>; // Effect-specific parameters
}

/**
 * nvox:f0 element attributes
 */
export interface SSMLF0Element {
  contour: string; // e.g., '(0%,+20Hz)(50%,+50Hz)(100%,-10Hz)'
  unit?: 'Hz' | 'st' | '%'; // Hz, semitones, or percentage
}

/**
 * nvox:energy element attributes
 */
export interface SSMLEnergyElement {
  level: SSMLEnergyLevel;
  attack?: SSMLAttack; // default 'normal'
  sustain?: number; // multiplier, default 1.0
}

/**
 * nvox:animate element attributes
 */
export interface SSMLAnimateElement {
  cue: SSMLAnimationCue | string;
  at?: SSMLAnimateTrigger; // default 'start'
  intensity?: number; // 0.0-1.0, default 1.0
  duration?: string; // e.g., '500ms'
}

/**
 * nvox:marker element attributes
 */
export interface SSMLMarkerElement {
  name: string;
  data?: Record<string, unknown>; // JSON metadata
}

/**
 * nvox:track element attributes
 */
export interface SSMLTrackElement {
  id: string;
  src?: string; // Audio file URI
  volume?: string; // e.g., '-6dB', '0dB'
  pan?: number; // -1.0 to 1.0
}

/**
 * nvox:parallel element attributes
 */
export interface SSMLParallelElement {
  sync?: SSMLParallelSync; // default 'start'
  tracks: SSMLTrackElement[];
}

/**
 * SSML validation error codes
 */
export type SSMLErrorCode =
  | 'SSML_001' // Invalid XML structure
  | 'SSML_002' // Unknown NOIZYVOX element
  | 'SSML_003' // Invalid attribute value
  | 'SSML_004' // Persona not found
  | 'SSML_005' // Incompatible DSP chain
  | 'SSML_006' // Animation cue unavailable for persona
  | 'SSML_007' // Emotion type not supported
  | 'SSML_008'; // F0 contour parse error

/**
 * SSML validation message
 */
export interface SSMLValidationMessage {
  code: SSMLErrorCode;
  message: string;
  line?: number;
  column?: number;
  element?: string;
  attribute?: string;
  value?: string;
  suggestion?: string;
}

/**
 * Parsed SSML structure
 */
export interface SSMLParsedStructure {
  personas_used: Array<{
    id: string;
    version?: string;
    exists: boolean;
  }>;
  emotions_used: Array<{
    type: SSMLEmotionType;
    count: number;
  }>;
  dsp_effects_used: Array<{
    effect: SSMLDSPEffect;
    count: number;
  }>;
  animation_cues_used: Array<{
    cue: string;
    count: number;
    available: boolean;
  }>;
  markers: Array<{
    name: string;
    has_data: boolean;
  }>;
  estimated_duration_ms: number;
  word_count: number;
  character_count: number;
}

/**
 * SSML compatibility report
 */
export interface SSMLCompatibilityReport {
  w3c_ssml_1_1: boolean;
  amazon_polly: boolean;
  google_cloud_tts: boolean;
  azure_speech: boolean;
  fallback_ssml: string;
}

/**
 * SSML validation result
 */
export interface SSMLValidationResult {
  valid: boolean;
  document_hash: `sha256:${string}`;
  warnings: SSMLValidationMessage[];
  errors: SSMLValidationMessage[];
  parsed_structure?: SSMLParsedStructure;
  compatibility?: SSMLCompatibilityReport;
}


// ============================================================================
// AUTOMATION LANE TYPES
// ============================================================================

/**
 * Automation ID pattern: auto_ + 16 hex chars
 */
export type AutomationId = `auto_${string}`;

/**
 * Interpolation methods for automation curves
 */
export type InterpolationType = 'linear' | 'cubic' | 'catmull_rom' | 'step';

/**
 * Valid sample rates for automation data
 */
export type AutomationSampleRate = 100 | 200 | 500 | 1000;

/**
 * Vibrato parameters for F0 modulation
 */
export interface VibratoParams {
  rate_hz: number; // 0-10 Hz
  depth_cents: number; // 0-100 cents
  onset_ms?: number;
}

/**
 * F0 (fundamental frequency) data for a word or phoneme
 */
export interface F0Data {
  base_hz?: number; // 50-500 Hz
  contour_cents?: number[]; // F0 deviation in cents at each sample point
  contour_hz?: number[]; // Absolute F0 in Hz at each sample point
  vibrato?: VibratoParams;
}

/**
 * Energy/amplitude data for a word or phoneme
 */
export interface EnergyData {
  base_db?: number; // Base energy level in dB
  contour_db?: number[]; // Energy in dB at each sample point
  attack_ms?: number; // Attack time in milliseconds
  release_ms?: number; // Release time in milliseconds
}

/**
 * Viseme timing data for lip-sync animation
 */
export interface VisemeEntry {
  viseme: string;
  start_ms: number;
  duration_ms: number;
  weight?: number; // 0-1
}

/**
 * Phoneme-level automation data
 */
export interface PhonemeAutomation {
  phoneme: string; // IPA or ARPABET phoneme
  start_ms: number;
  end_ms: number;
  f0_cents?: number[]; // F0 deviation in cents at each sample point
  energy_db?: number[]; // Energy in dB at each sample point
  viseme?: string; // Corresponding viseme for animation
}

/**
 * Word-level automation data
 */
export interface WordAutomation {
  word: string;
  word_index?: number;
  start_ms: number;
  end_ms: number;
  phonemes?: PhonemeAutomation[];
  f0: F0Data;
  energy: EnergyData;
  viseme_sequence?: VisemeEntry[];
}

/**
 * Global automation curves for the entire utterance
 */
export interface GlobalCurves {
  f0_hz?: number[]; // Global F0 curve at sample_rate_hz
  energy_db?: number[]; // Global energy curve at sample_rate_hz
  spectral_tilt?: number[]; // Spectral tilt (brightness) curve
  breathiness?: number[]; // Breathiness amount over time (0-1)
}

/**
 * Complete Automation Lane document
 * Per-word/phoneme F0 and energy automation data for voice synthesis
 */
export interface AutomationLane {
  automation_id: AutomationId;
  version: string; // Semantic version
  created_at?: string; // ISO 8601 datetime
  persona_id?: string;
  text?: string; // Original input text
  sample_rate_hz: AutomationSampleRate; // Automation data sample rate
  interpolation?: InterpolationType; // default 'cubic'
  duration_ms?: number; // Total duration in milliseconds
  words: WordAutomation[];
  global_curves?: GlobalCurves;
}


// ============================================================================
// API RATE LIMITS TYPES
// ============================================================================

/**
 * Request queue priority levels
 */
export type RateLimitPriority = 'low' | 'normal' | 'high' | 'critical';

/**
 * License tiers for rate limiting
 */
export type RateLimitTier = 'free' | 'micro' | 'non_exclusive' | 'exclusive' | 'enterprise';

/**
 * Throttling algorithm types
 */
export type ThrottlingAlgorithm = 'token_bucket' | 'sliding_window' | 'fixed_window' | 'leaky_bucket';

/**
 * Base rate limit configuration for a tier
 */
export interface RateLimitTierConfig {
  requests_per_minute: number;
  requests_per_hour: number;
  requests_per_day: number; // -1 = unlimited
  max_characters_per_request: number;
  max_audio_minutes_per_day: number; // -1 = unlimited
  concurrent_requests: number;
  priority: RateLimitPriority;
}

/**
 * Enterprise tier with additional features
 */
export interface EnterpriseTierConfig extends RateLimitTierConfig {
  dedicated_capacity: boolean;
  sla_uptime_percent: number; // 99-100
  custom_endpoints?: boolean;
  priority_support?: boolean;
}

/**
 * Rate limit HTTP headers
 */
export interface RateLimitHeaders {
  'X-RateLimit-Limit': string;
  'X-RateLimit-Remaining': string;
  'X-RateLimit-Reset': string;
  'X-RateLimit-Retry-After'?: string;
}

/**
 * Burst policy configuration
 */
export interface BurstPolicy {
  burst_multiplier: number; // e.g., 1.5 = allow 150% burst
  burst_window_seconds: number;
  cooldown_seconds: number;
}

/**
 * Overage policy configuration
 */
export interface OveragePolicy {
  allow_overage: boolean;
  overage_rate_multiplier: number; // Price multiplier for overage
  hard_cap_multiplier: number; // Max overage allowed
  overage_notification_threshold: number; // e.g., 0.8 = notify at 80%
}

/**
 * Throttling configuration
 */
export interface ThrottlingConfig {
  algorithm: ThrottlingAlgorithm;
  token_refill_rate_per_second?: number;
  max_queue_size: number;
  queue_timeout_seconds: number;
}

/**
 * Rate limit error response
 */
export interface RateLimitErrorResponse {
  status_code: 429;
  error_code: 'RATE_LIMIT_EXCEEDED' | 'QUOTA_EXCEEDED' | 'CONCURRENT_LIMIT_EXCEEDED';
  message: string;
}

/**
 * Complete API Rate Limits configuration
 */
export interface APIRateLimitsConfig {
  tiers: {
    free: RateLimitTierConfig;
    micro: RateLimitTierConfig;
    non_exclusive: RateLimitTierConfig;
    exclusive: RateLimitTierConfig;
    enterprise: EnterpriseTierConfig;
  };
  rate_limit_headers?: RateLimitHeaders;
  burst_policy?: BurstPolicy;
  overage_policy?: OveragePolicy;
  throttling?: ThrottlingConfig;
  error_responses?: {
    rate_limit_exceeded?: RateLimitErrorResponse;
    quota_exceeded?: RateLimitErrorResponse;
    concurrent_limit_exceeded?: RateLimitErrorResponse;
  };
}


// ============================================================================
// LATENCY SLA TYPES
// ============================================================================

/**
 * Audio quality presets
 */
export type QualityPreset = 'draft' | 'standard' | 'high' | 'ultra';

/**
 * Studio environment (high-quality offline rendering)
 */
export interface StudioEnvironment {
  first_byte_ms: number; // Time to first audio byte
  real_time_factor: number; // 0.5 = 2x faster than real-time
  max_latency_ms: number;
  quality_preset: QualityPreset;
  parallel_renders?: number; // Max parallel render jobs
}

/**
 * Streaming environment (real-time streaming synthesis)
 */
export interface StreamingEnvironment {
  first_byte_ms: number;
  chunk_size_ms: number; // Audio chunk duration
  buffer_ms: number; // Client-side buffer
  max_latency_ms: number;
  quality_preset: QualityPreset;
  adaptive_bitrate?: boolean;
}

/**
 * Live environment (ultra-low latency for live performance)
 */
export interface LiveEnvironment {
  first_byte_ms: number;
  chunk_size_ms: number;
  buffer_ms: number;
  max_latency_ms: number;
  quality_preset: QualityPreset;
  edge_inference?: boolean; // Use edge servers
  webrtc_enabled?: boolean;
}

/**
 * VR/AR environment (spatial audio requirements)
 */
export interface VRAREnvironment {
  first_byte_ms: number;
  motion_to_sound_ms: number; // Head motion to audio update latency
  spatial_update_hz: number; // Match display refresh rate
  max_latency_ms: number; // To avoid motion sickness
  hrtf_processing?: boolean; // Head-related transfer function
  ambisonics_order?: number; // 1-7, spatial resolution
  room_modeling?: boolean; // Real-time room acoustics
}

/**
 * Latency percentile targets
 */
export interface PercentileTargets {
  p50_multiplier: number; // Median latency
  p95_multiplier: number;
  p99_multiplier: number;
  p999_multiplier: number;
}

/**
 * Uptime SLA by tier (percentage)
 */
export interface UptimeSLA {
  free: number; // 95.0
  micro: number; // 99.0
  non_exclusive: number; // 99.5
  exclusive: number; // 99.9
  enterprise: number; // 99.99
}

/**
 * SLA credits for violations (percentage of monthly bill)
 */
export interface SLACredits {
  '99_9_to_99_5': number; // 10% credit
  '99_5_to_99_0': number; // 25% credit
  '99_0_to_95_0': number; // 50% credit
  below_95_0: number; // 100% credit
}

/**
 * Alert thresholds for monitoring
 */
export interface AlertThresholds {
  warning_latency_multiplier: number;
  critical_latency_multiplier: number;
  error_rate_warning: number; // e.g., 0.01 = 1%
  error_rate_critical: number; // e.g., 0.05 = 5%
}

/**
 * SLA monitoring configuration
 */
export interface SLAMonitoring {
  health_check_interval_seconds: number;
  latency_sample_rate: number; // e.g., 0.1 = 10% of requests
  alert_thresholds?: AlertThresholds;
}

/**
 * Complete Latency SLA configuration
 */
export interface LatencySLAConfig {
  environments: {
    studio: StudioEnvironment;
    streaming: StreamingEnvironment;
    live: LiveEnvironment;
    vr_ar: VRAREnvironment;
  };
  percentile_targets?: PercentileTargets;
  uptime_sla?: UptimeSLA;
  sla_credits?: SLACredits;
  monitoring?: SLAMonitoring;
}


// ============================================================================
// EDGE DEPLOYMENT TYPES
// ============================================================================

/**
 * Edge deployment ID pattern
 */
export type EdgeDeploymentId = `edge_${string}`;

/**
 * Model format for edge deployment
 */
export type ModelFormat = 'onnx' | 'coreml' | 'tensorrt' | 'tflite' | 'wasm';

/**
 * Quantization levels
 */
export type QuantizationType = 'fp32' | 'fp16' | 'int8' | 'int4';

/**
 * Target platforms
 */
export type TargetPlatform = 'ios' | 'android' | 'macos' | 'windows' | 'linux' | 'web' | 'embedded';

/**
 * CPU architectures
 */
export type Architecture = 'arm64' | 'x86_64' | 'armv7' | 'wasm32';

/**
 * Hardware accelerators
 */
export type Accelerator = 'cpu' | 'gpu' | 'npu' | 'ane' | 'coreml' | 'nnapi' | 'webgpu';

/**
 * Power modes for edge inference
 */
export type PowerMode = 'efficiency' | 'balanced' | 'performance';

/**
 * Obfuscation levels
 */
export type ObfuscationLevel = 'none' | 'basic' | 'advanced' | 'maximum';

/**
 * Model encryption configuration
 */
export interface ModelEncryption {
  algorithm: 'aes-256-gcm' | 'chacha20-poly1305';
  key_derivation: 'pbkdf2' | 'argon2id' | 'hkdf';
  hardware_binding: boolean;
}

/**
 * Model component sizes
 */
export interface ModelComponents {
  acoustic_model_mb?: number;
  vocoder_mb?: number;
  prosody_model_mb?: number;
  emotion_model_mb?: number;
}

/**
 * Edge model package configuration
 */
export interface EdgeModelPackage {
  format: ModelFormat;
  quantization?: QuantizationType;
  size_mb: number;
  checksum: `sha256:${string}`;
  version?: string;
  encryption?: ModelEncryption;
  components?: ModelComponents;
}

/**
 * Platform-specific deployment target
 */
export interface PlatformTarget {
  platform: TargetPlatform;
  min_version?: string;
  architectures?: Architecture[];
  accelerators?: Accelerator[];
  min_memory_mb?: number;
  min_storage_mb?: number;
}

/**
 * Offline capabilities configuration
 */
export interface OfflineCapabilities {
  max_offline_duration_days: number;
  license_check_interval_hours: number;
  grace_period_hours: number;
  offline_usage_logging: boolean;
  sync_on_reconnect: boolean;
  offline_character_limit?: number;
  require_initial_activation?: boolean;
}

/**
 * Edge security configuration
 */
export interface EdgeSecurityConfig {
  certificate_pinning: boolean;
  root_detection: boolean;
  debugger_detection: boolean;
  tampering_detection: boolean;
  watermark_embedded: boolean;
  usage_metering: boolean;
  obfuscation_level?: ObfuscationLevel;
  secure_enclave?: boolean;
}

/**
 * Distribution configuration
 */
export interface DistributionConfig {
  cdn_regions: string[];
  delta_updates: boolean;
  background_download: boolean;
  preload_on_wifi: boolean;
  max_download_retries?: number;
  resume_partial_downloads?: boolean;
}

/**
 * Performance profile for edge inference
 */
export interface EdgePerformanceProfile {
  max_concurrent_streams: number;
  memory_limit_mb?: number;
  cpu_threads: number;
  gpu_memory_fraction?: number;
  batch_size: number;
  power_mode: PowerMode;
}

/**
 * Telemetry configuration
 */
export interface EdgeTelemetryConfig {
  enabled: boolean;
  collect_performance_metrics: boolean;
  collect_error_reports: boolean;
  collect_usage_stats: boolean;
  upload_interval_minutes: number;
}

/**
 * Complete Edge Deployment configuration
 */
export interface EdgeDeployment {
  deployment_id: EdgeDeploymentId;
  persona_id: string;
  license_id: `lic_${string}`;
  created_at?: string;
  expires_at?: string;
  model_package: EdgeModelPackage;
  target_platforms?: PlatformTarget[];
  offline_capabilities?: OfflineCapabilities;
  security?: EdgeSecurityConfig;
  distribution?: DistributionConfig;
  performance_profile?: EdgePerformanceProfile;
  telemetry?: EdgeTelemetryConfig;
}


// ============================================================================
// A/B TESTING TYPES
// ============================================================================

/**
 * Experiment ID pattern
 */
export type ExperimentId = `exp_${string}`;

/**
 * Variant ID pattern
 */
export type VariantId = `var_${string}`;

/**
 * Experiment status
 */
export type ExperimentStatus = 'draft' | 'running' | 'paused' | 'completed' | 'cancelled';

/**
 * Target audience types
 */
export type AudienceType = 'all' | 'new_users' | 'returning_users' | 'enterprise' | 'custom';

/**
 * Primary/secondary metrics for A/B testing
 */
export type ABMetric =
  | 'conversion_rate'
  | 'revenue'
  | 'engagement_time'
  | 'quality_rating'
  | 'repeat_usage'
  | 'share_rate'
  | 'favorite_rate'
  | 'completion_rate'
  | 'refund_rate';

/**
 * Experiment recommendation
 */
export type ExperimentRecommendation =
  | 'promote_winner'
  | 'continue_testing'
  | 'no_significant_difference'
  | 'revert_to_control';

/**
 * Audit log action types
 */
export type AuditAction =
  | 'created'
  | 'started'
  | 'paused'
  | 'resumed'
  | 'completed'
  | 'cancelled'
  | 'variant_added'
  | 'variant_removed'
  | 'traffic_adjusted';

/**
 * Prosody overrides for A/B variant
 */
export interface ProsodyOverrides {
  pitch_base_hz?: number;
  rate_wpm?: number;
  warmth?: number;
}

/**
 * DSP overrides for A/B variant
 */
export interface DSPOverrides {
  reverb_wet_mix?: number;
  eq_high_gain_db?: number;
}

/**
 * Pricing overrides for A/B variant
 */
export interface PricingOverrides {
  micro_per_minute_usd?: number;
  discount_percent?: number;
}

/**
 * Variant modifications
 */
export interface VariantModifications {
  prosody_overrides?: ProsodyOverrides;
  dsp_overrides?: DSPOverrides;
  pricing_overrides?: PricingOverrides;
}

/**
 * A/B test variant
 */
export interface ABVariant {
  variant_id: VariantId;
  variant_name?: string;
  persona_id: string;
  persona_version?: string;
  traffic_percent: number; // 0-100
  is_control?: boolean;
  modifications?: VariantModifications;
}

/**
 * Experiment targeting configuration
 */
export interface ExperimentTargeting {
  audience?: AudienceType;
  geographic?: string[]; // ISO 3166-1 alpha-2 codes
  user_segments?: string[];
  exclude_segments?: string[];
  platform_filter?: Array<'web' | 'ios' | 'android' | 'desktop' | 'api'>;
  license_tiers?: RateLimitTier[];
}

/**
 * Early stopping configuration
 */
export interface EarlyStoppingConfig {
  enabled: boolean;
  significance_threshold: number;
  min_runtime_days: number;
}

/**
 * Metrics configuration for experiment
 */
export interface ExperimentMetricsConfig {
  primary: ABMetric;
  secondary?: ABMetric[];
  minimum_sample_size: number;
  confidence_level: number; // 0.80-0.99
  minimum_detectable_effect: number; // 0.01-0.50
  early_stopping?: EarlyStoppingConfig;
}

/**
 * Confidence interval
 */
export interface ConfidenceInterval {
  lower: number;
  upper: number;
}

/**
 * Individual variant result
 */
export interface VariantResult {
  variant_id: string;
  impressions: number;
  conversions: number;
  conversion_rate: number;
  revenue: number;
  avg_quality_rating?: number;
  avg_engagement_time_seconds?: number;
  repeat_usage_rate?: number;
  confidence_interval?: ConfidenceInterval;
  statistical_significance: boolean;
  p_value: number;
  lift_vs_control?: number;
}

/**
 * Experiment results
 */
export interface ExperimentResults {
  total_impressions: number;
  total_conversions?: number;
  total_revenue?: number;
  analysis_timestamp: string;
  variant_results: VariantResult[];
  winner?: string; // variant_id
  recommendation: ExperimentRecommendation;
  summary?: string;
}

/**
 * Audit log entry
 */
export interface ExperimentAuditEntry {
  timestamp: string;
  action: AuditAction;
  user_id: string;
  details?: Record<string, unknown>;
}

/**
 * Complete A/B Testing Experiment
 */
export interface ABExperiment {
  experiment_id: ExperimentId;
  name: string;
  description?: string;
  artist_id: `artist_${string}`;
  status: ExperimentStatus;
  created_at?: string;
  start_at?: string;
  end_at?: string;
  variants: ABVariant[]; // 2-10 variants
  targeting?: ExperimentTargeting;
  metrics?: ExperimentMetricsConfig;
  results?: ExperimentResults;
  audit_log?: ExperimentAuditEntry[];
}

// =============================================================================
// DISPUTE RESOLUTION TYPES
// =============================================================================

/**
 * Dispute ID format: disp_[16 lowercase alphanumeric]
 */
export type DisputeId = `disp_${string}`;

/**
 * Types of disputes that can be filed
 */
export type DisputeType =
  | 'unauthorized_usage'
  | 'content_restriction_violation'
  | 'quality_complaint'
  | 'attribution_error'
  | 'royalty_dispute'
  | 'license_interpretation'
  | 'technical_failure'
  | 'privacy_violation'
  | 'moral_rights'
  | 'other';

/**
 * Dispute workflow status
 */
export type DisputeStatus =
  | 'submitted'
  | 'under_review'
  | 'mediation'
  | 'arbitration'
  | 'resolved'
  | 'dismissed'
  | 'appealed';

/**
 * Priority level for dispute handling
 */
export type DisputePriority = 'low' | 'medium' | 'high' | 'critical';

/**
 * Party role in the dispute
 */
export type PartyRole = 'artist' | 'licensee' | 'platform' | 'third_party';

/**
 * Legal representative information
 */
export interface LegalRepresentative {
  name: string;
  firm?: string;
  email: string;
  phone?: string;
  bar_number?: string;
}

/**
 * Party to a dispute
 */
export interface DisputeParty {
  party_id: string;
  role: PartyRole;
  name: string;
  contact_email: string;
  legal_representative?: LegalRepresentative;
}

/**
 * Type of evidence
 */
export type EvidenceType =
  | 'audio_file'
  | 'video_file'
  | 'screenshot'
  | 'document'
  | 'log_data'
  | 'contract'
  | 'communication'
  | 'witness_statement'
  | 'expert_report';

/**
 * Evidence submitted in support of a claim
 */
export interface DisputeEvidence {
  evidence_id: string;
  type: EvidenceType;
  title: string;
  description?: string;
  url?: string;
  hash?: string;
  submitted_by: string; // party_id
  submitted_at: string;
}

/**
 * Timeline event in dispute process
 */
export interface DisputeTimelineEvent {
  timestamp: string;
  event: string;
  actor: string;
  notes?: string;
}

/**
 * Arbitration provider options
 */
export type ArbitrationProvider = 'JAMS' | 'AAA' | 'ICC' | 'WIPO' | 'internal';

/**
 * Resolution process configuration
 */
export interface ResolutionProcess {
  mediation_offered: boolean;
  mediation_accepted?: boolean;
  mediator_id?: string;
  arbitration_provider?: ArbitrationProvider;
  arbitrator_id?: string;
  hearing_date?: string;
  sla: {
    initial_response_hours: number;
    mediation_days: number;
    arbitration_days: number;
    max_resolution_days: number;
  };
}

/**
 * Types of remedies that can be awarded
 */
export type RemedyType =
  | 'monetary_award'
  | 'license_termination'
  | 'content_takedown'
  | 'public_apology'
  | 'license_modification'
  | 'royalty_adjustment'
  | 'warning';

/**
 * A specific remedy awarded
 */
export interface Remedy {
  type: RemedyType;
  description: string;
  amount_usd?: number;
  deadline?: string;
  completed?: boolean;
}

/**
 * Final resolution of the dispute
 */
export interface DisputeResolution {
  resolved_at: string;
  decision_summary: string;
  prevailing_party?: string; // party_id
  remedies: Remedy[];
  binding: boolean;
  appeal_deadline?: string;
}

/**
 * Complete Dispute Resolution document
 */
export interface Dispute {
  dispute_id: DisputeId;
  status: DisputeStatus;
  dispute_type: DisputeType;
  priority: DisputePriority;
  created_at?: string;
  updated_at?: string;
  
  /** Subject of the dispute */
  subject: {
    title: string;
    description: string;
    related_license_id?: string;
    related_artifact_ids?: string[];
  };
  
  /** Parties involved */
  parties: {
    claimant: DisputeParty;
    respondent: DisputeParty;
    mediator?: DisputeParty;
    arbitrator?: DisputeParty;
  };
  
  /** Evidence submitted */
  evidence: DisputeEvidence[];
  
  /** Timeline of events */
  timeline: DisputeTimelineEvent[];
  
  /** Resolution process */
  resolution_process: ResolutionProcess;
  
  /** Final resolution (when status is 'resolved') */
  resolution?: DisputeResolution;
}

// =============================================================================
// POSTHUMOUS RIGHTS TYPES
// =============================================================================

/**
 * Estate plan ID format: estate_[16 lowercase alphanumeric]
 */
export type EstatePlanId = `estate_${string}`;

/**
 * Status of the estate plan
 */
export type EstatePlanStatus = 'active' | 'triggered' | 'probate' | 'transferred' | 'dissolved';

/**
 * Relationship types for beneficiaries
 */
export type BeneficiaryRelationship =
  | 'spouse'
  | 'child'
  | 'parent'
  | 'sibling'
  | 'other_family'
  | 'friend'
  | 'organization'
  | 'charity'
  | 'trust';

/**
 * Payout methods for beneficiaries
 */
export type PayoutMethod = 'bank_transfer' | 'paypal' | 'crypto' | 'check';

/**
 * Executor verification method
 */
export type ExecutorVerificationMethod = 'id_document' | 'legal_attestation' | 'notarized';

/**
 * Beneficiary definition
 */
export interface Beneficiary {
  beneficiary_id?: string;
  name: string;
  relationship: BeneficiaryRelationship;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  tax_id?: string;
  share_percent?: number;
  payout_method?: PayoutMethod;
  payout_details?: string;
  management_rights?: boolean;
  verified?: boolean;
}

/**
 * Estate executor
 */
export interface Executor {
  name: string;
  relationship?: string;
  email: string;
  phone?: string;
  address?: string;
  legal_representative?: string;
  verified?: boolean;
  verification_method?: ExecutorVerificationMethod;
}

/**
 * Sunset action when voice model is retired
 */
export type SunsetAction = 'archive' | 'delete' | 'donate_to_archive';

/**
 * Artist directives for posthumous use
 */
export interface PosthumousDirectives {
  continue_licensing?: boolean;
  new_works_allowed?: boolean;
  content_restrictions_apply?: boolean;
  additional_restrictions?: string[];
  tribute_use_only?: boolean;
  sunset_date?: string;
  sunset_action?: SunsetAction;
  special_instructions?: string;
}

/**
 * Revenue distribution method
 */
export type DistributionMethod = 'equal' | 'percentage' | 'sequential' | 'trust';

/**
 * Revenue distribution configuration
 */
export interface RevenueDistribution {
  distribution_method?: DistributionMethod;
  beneficiary_shares?: Array<{
    beneficiary_id: string;
    share_percent: number;
  }>;
  platform_share_change?: number;
  charitable_donation_percent?: number;
  charity_designee?: string;
}

/**
 * Accepted proof of death documents
 */
export type ProofOfDeathDocument = 'death_certificate' | 'obituary' | 'legal_attestation' | 'executor_declaration';

/**
 * Proof of death requirements
 */
export interface ProofOfDeathRequirements {
  accepted_documents?: ProofOfDeathDocument[];
  verification_period_days?: number;
  notification_parties?: string[];
}

/**
 * Transition plan after artist death
 */
export interface TransitionPlan {
  notification_message?: string;
  grace_period_days?: number;
  existing_licenses_honored?: boolean;
  new_license_moratorium_days?: number;
  tribute_page_enabled?: boolean;
}

/**
 * Legal documentation for estate
 */
export interface EstateLegal {
  governing_law?: string;
  jurisdiction?: string;
  will_reference?: string;
  trust_reference?: string;
  legal_document_url?: string;
  document_hash?: `sha256:${string}`;
  notarized?: boolean;
  notarization_date?: string;
}

/**
 * Estate audit trail event types
 */
export type EstateAuditEvent =
  | 'created'
  | 'updated'
  | 'beneficiary_added'
  | 'beneficiary_removed'
  | 'executor_changed'
  | 'triggered'
  | 'transferred'
  | 'disputed';

/**
 * Estate audit trail entry
 */
export interface EstateAuditEntry {
  event: EstateAuditEvent;
  timestamp: string;
  actor: string;
  details?: Record<string, unknown>;
}

/**
 * Complete Posthumous Rights / Estate Plan document
 */
export interface EstatePlan {
  estate_plan_id: EstatePlanId;
  artist_id: `artist_${string}`;
  created_at?: string;
  updated_at?: string;
  status: EstatePlanStatus;
  
  /** Primary beneficiary */
  primary_beneficiary: Beneficiary;
  
  /** Secondary beneficiaries */
  secondary_beneficiaries?: Beneficiary[];
  
  /** Estate executor */
  executor: Executor;
  
  /** Artist directives for posthumous use */
  directives?: PosthumousDirectives;
  
  /** Revenue distribution plan */
  revenue_distribution?: RevenueDistribution;
  
  /** Proof of death requirements */
  proof_of_death_requirements?: ProofOfDeathRequirements;
  
  /** Transition plan */
  transition_plan?: TransitionPlan;
  
  /** Legal documentation */
  legal?: EstateLegal;
  
  /** Audit trail */
  audit_trail?: EstateAuditEntry[];
}

// =============================================================================
// SECURITY & WATERMARKING TYPES
// =============================================================================

/**
 * Watermark ID format: wm_[16 lowercase alphanumeric]
 */
export type WatermarkId = `wm_${string}`;

/**
 * Watermarking methods
 */
export type WatermarkMethod = 'spectral' | 'phase' | 'lsb' | 'spread_spectrum' | 'echo_hiding' | 'neural';

/**
 * Watermark layer (audibility)
 */
export type WatermarkLayer = 'inaudible' | 'semi_audible' | 'forensic';

/**
 * Watermark robustness level
 */
export type WatermarkRobustness = 'fragile' | 'semi_fragile' | 'robust';

/**
 * Individual watermark method configuration
 */
export interface WatermarkMethodConfig {
  method: WatermarkMethod;
  layer: WatermarkLayer;
  robustness?: WatermarkRobustness;
  capacity_bps?: number;
}

/**
 * Watermark payload data
 */
export interface WatermarkPayload {
  artifact_id?: string;
  persona_id?: string;
  artist_id?: string;
  license_id?: string;
  timestamp?: string;
  licensee_id?: string;
  generation_params_hash?: string;
}

/**
 * Watermark detection configuration
 */
export interface WatermarkDetection {
  api_endpoint?: string;
  detection_threshold?: number;
  false_positive_rate?: number;
  false_negative_rate?: number;
}

/**
 * Watermark resilience characteristics
 */
export interface WatermarkResilience {
  compression_resistant?: boolean;
  transcoding_resistant?: boolean;
  noise_resistant_db?: number;
  time_stretch_resistant_percent?: number;
  pitch_shift_resistant_semitones?: number;
}

/**
 * Complete watermark configuration
 */
export interface Watermark {
  watermark_id: WatermarkId;
  methods: WatermarkMethodConfig[];
  payload?: WatermarkPayload;
  detection?: WatermarkDetection;
  resilience?: WatermarkResilience;
}

/**
 * Fingerprinting algorithms
 */
export type FingerprintAlgorithm = 'chromaprint' | 'dejavu' | 'panako' | 'audfprint' | 'shazam_like' | 'neural_embedding';

/**
 * Fingerprint index types
 */
export type FingerprintIndexType = 'lsh' | 'hnsw' | 'ivf' | 'annoy';

/**
 * Fingerprint database configuration
 */
export interface FingerprintDatabase {
  total_fingerprints?: number;
  index_type?: FingerprintIndexType;
  query_latency_ms?: number;
}

/**
 * Fingerprint matching configuration
 */
export interface FingerprintMatching {
  similarity_threshold?: number;
  time_tolerance_seconds?: number;
  partial_match_min_seconds?: number;
}

/**
 * Fingerprinting configuration
 */
export interface Fingerprinting {
  algorithms?: FingerprintAlgorithm[];
  fingerprint_database?: FingerprintDatabase;
  matching?: FingerprintMatching;
}

/**
 * Deepfake detection types
 */
export type DeepfakeDetectionType = 'voice_cloning' | 'voice_conversion' | 'tts_synthesis' | 'audio_splicing' | 'replay_attack';

/**
 * Deepfake detection model
 */
export interface DeepfakeDetectionModel {
  model_name: string;
  version?: string;
  accuracy?: number;
  false_positive_rate?: number;
  detection_types?: DeepfakeDetectionType[];
}

/**
 * Monitored platforms for deepfake detection
 */
export type MonitoredPlatform = 'youtube' | 'tiktok' | 'instagram' | 'twitter' | 'facebook' | 'twitch' | 'spotify' | 'podcast_platforms';

/**
 * Deepfake alert thresholds
 */
export interface DeepfakeAlertThresholds {
  confidence_for_review?: number;
  confidence_for_alert?: number;
  confidence_for_auto_action?: number;
}

/**
 * Deepfake detection configuration
 */
export interface DeepfakeDetection {
  enabled?: boolean;
  detection_models?: DeepfakeDetectionModel[];
  platform_monitoring?: MonitoredPlatform[];
  alert_thresholds?: DeepfakeAlertThresholds;
}

/**
 * C2PA content credential actions
 */
export type C2PAAction = 'c2pa.created' | 'c2pa.edited' | 'c2pa.published' | 'noizyvox.synthesized' | 'noizyvox.mastered';

/**
 * Content credential assertion
 */
export interface ContentAssertion {
  label: string;
  data: Record<string, unknown>;
}

/**
 * Content credentials (C2PA)
 */
export interface ContentCredentials {
  issuer?: string;
  issued_at?: string;
  actions?: C2PAAction[];
  assertions?: ContentAssertion[];
}

/**
 * Blockchain networks for anchoring
 */
export type BlockchainNetwork = 'ethereum' | 'polygon' | 'solana' | 'arweave';

/**
 * Blockchain anchor for provenance
 */
export interface BlockchainAnchor {
  enabled?: boolean;
  chain?: BlockchainNetwork;
  tx_hash?: string;
  block_number?: number;
}

/**
 * Provenance chain configuration
 */
export interface ProvenanceChain {
  c2pa_enabled?: boolean;
  content_credentials?: ContentCredentials;
  blockchain_anchor?: BlockchainAnchor;
}

/**
 * Platform integration for takedowns
 */
export interface PlatformIntegration {
  platform: string;
  api_integrated?: boolean;
  average_takedown_hours?: number;
}

/**
 * Takedown automation configuration
 */
export interface TakedownAutomation {
  auto_dmca?: boolean;
  platform_integrations?: PlatformIntegration[];
  notification_webhook?: string;
}

/**
 * Complete Security & Watermarking document
 */
export interface SecurityWatermarking {
  /** Watermark configuration */
  watermark: Watermark;
  
  /** Fingerprinting configuration */
  fingerprinting?: Fingerprinting;
  
  /** Deepfake detection */
  deepfake_detection?: DeepfakeDetection;
  
  /** Provenance chain */
  provenance_chain?: ProvenanceChain;
  
  /** Takedown automation */
  takedown_automation?: TakedownAutomation;
}

// =============================================================================
// GUILD GOVERNANCE TYPES
// =============================================================================

/**
 * Membership tier types
 */
export type MembershipTier = 'founding' | 'verified' | 'provisional';

/**
 * Founding tier configuration
 */
export interface FoundingTier {
  max_members?: number;
  current_members?: number;
  equity_eligible?: boolean;
  voting_weight?: number;
  benefits?: string[];
}

/**
 * Verified tier configuration
 */
export interface VerifiedTier {
  current_members?: number;
  voting_weight?: number;
  benefits?: string[];
}

/**
 * Upgrade requirements for provisional members
 */
export interface UpgradeRequirements {
  min_days?: number;
  min_revenue_usd?: number;
  min_quality_rating?: number;
  vouches_required?: number;
}

/**
 * Provisional tier configuration
 */
export interface ProvisionalTier {
  current_members?: number;
  voting_weight?: number;
  upgrade_requirements?: UpgradeRequirements;
}

/**
 * Membership tiers
 */
export interface MembershipTiers {
  founding?: FoundingTier;
  verified?: VerifiedTier;
  provisional?: ProvisionalTier;
}

/**
 * Guild membership configuration
 */
export interface GuildMembership {
  tiers?: MembershipTiers;
  total_members?: number;
  application_queue?: number;
}

/**
 * Council composition
 */
export interface CouncilComposition {
  founding_artist_seats?: number;
  verified_artist_seats?: number;
  platform_seats?: number;
}

/**
 * Guild council configuration
 */
export interface GuildCouncil {
  name?: string;
  seats?: number;
  composition?: CouncilComposition;
  term_months?: number;
  term_limits?: number;
  election_frequency_months?: number;
}

/**
 * Committee definition
 */
export interface GuildCommittee {
  name: string;
  purpose?: string;
  members?: number;
  chair?: string;
}

/**
 * Governance structure
 */
export interface GovernanceStructure {
  council?: GuildCouncil;
  committees?: GuildCommittee[];
}

/**
 * Proposal types
 */
export type ProposalType = 
  | 'policy_change' 
  | 'fee_change' 
  | 'feature_request' 
  | 'membership_decision' 
  | 'platform_partnership' 
  | 'constitutional_amendment';

/**
 * Who can propose
 */
export type ProposerRole = 'founding' | 'verified' | 'council' | 'committee';

/**
 * Proposal type configuration
 */
export interface ProposalTypeConfig {
  type: ProposalType;
  quorum_percent?: number;
  pass_threshold_percent?: number;
  voting_period_days?: number;
  who_can_propose?: ProposerRole[];
}

/**
 * Voting methods
 */
export type VotingMethod = 'simple_majority' | 'supermajority' | 'ranked_choice' | 'quadratic' | 'conviction';

/**
 * Vote privacy settings
 */
export type VotePrivacy = 'public' | 'anonymous' | 'revealed_after_close';

/**
 * Voting configuration
 */
export interface GuildVoting {
  proposal_types?: ProposalTypeConfig[];
  voting_methods?: VotingMethod[];
  vote_privacy?: VotePrivacy;
}

/**
 * Treasury funding sources
 */
export type TreasuryFundingSource = 'platform_contribution' | 'membership_dues' | 'grants' | 'donations';

/**
 * Treasury allocation
 */
export interface TreasuryAllocation {
  artist_emergency_fund_percent?: number;
  education_fund_percent?: number;
  legal_defense_fund_percent?: number;
  technology_grants_percent?: number;
  operations_percent?: number;
}

/**
 * Guild treasury
 */
export interface GuildTreasury {
  balance_usd?: number;
  funding_sources?: TreasuryFundingSource[];
  allocation?: TreasuryAllocation;
  multisig_required?: number;
  spending_approval_threshold_usd?: number;
}

/**
 * Dispute escalation level
 */
export interface EscalationLevel {
  level: number;
  name: string;
  handled_by: string;
  max_days: number;
}

/**
 * Dispute escalation configuration
 */
export interface DisputeEscalation {
  levels?: EscalationLevel[];
}

/**
 * Amendment record
 */
export interface AmendmentRecord {
  amendment_id: string;
  title: string;
  passed_at?: string;
  vote_result?: string;
  summary?: string;
}

/**
 * Amendments configuration
 */
export interface GuildAmendments {
  constitution_version?: string;
  amendment_history?: AmendmentRecord[];
}

/**
 * Complete Guild Governance document
 */
export interface GuildGovernance {
  guild_id: string;
  name: string;
  founded_at?: string;
  
  /** Membership configuration */
  membership?: GuildMembership;
  
  /** Governance structure */
  governance_structure?: GovernanceStructure;
  
  /** Voting configuration */
  voting?: GuildVoting;
  
  /** Treasury */
  treasury?: GuildTreasury;
  
  /** Dispute escalation */
  dispute_escalation?: DisputeEscalation;
  
  /** Amendments */
  amendments?: GuildAmendments;
}

// =============================================================================
// VR/AR SPATIAL AUDIO TYPES
// =============================================================================

/**
 * Spatial config ID format: spatial_[16 lowercase alphanumeric]
 */
export type SpatialConfigId = `spatial_${string}`;

/**
 * VR/AR platform types
 */
export type XRPlatform = 
  | 'meta_quest' 
  | 'apple_vision_pro' 
  | 'pico' 
  | 'htc_vive' 
  | 'valve_index' 
  | 'playstation_vr' 
  | 'webxr' 
  | 'arkit' 
  | 'arcore' 
  | 'magic_leap'
  | 'nreal'
  | 'custom';

/**
 * HRTF database types
 */
export type HRTFDatabase = 'mit_kemar' | 'ircam_listen' | 'ari' | 'hutubs' | 'sadie' | 'custom';

/**
 * HRTF interpolation methods
 */
export type HRTFInterpolationMethod = 'nearest_neighbor' | 'bilinear' | 'spherical_harmonics' | 'neural';

/**
 * HRTF personalization - measured head dimensions
 */
export interface HRTFPersonalization {
  enabled?: boolean;
  head_width_cm?: number;
  head_depth_cm?: number;
  head_height_cm?: number;
  ear_to_ear_cm?: number;
  pinna_model?: 'generic' | 'scanned' | 'photographed';
  itd_correction_us?: number;
}

/**
 * HRTF interpolation configuration
 */
export interface HRTFInterpolation {
  method?: HRTFInterpolationMethod;
  elevation_resolution_deg?: number;
  azimuth_resolution_deg?: number;
}

/**
 * Head-Related Transfer Function configuration
 */
export interface HRTF {
  database?: HRTFDatabase;
  custom_sofa_url?: string;
  personalization?: HRTFPersonalization;
  interpolation?: HRTFInterpolation;
}

/**
 * Spatialization algorithm types
 */
export type SpatializationAlgorithm = 'hrtf_binaural' | 'vbap' | 'dbap' | 'ambisonics' | 'object_based';

/**
 * Ambisonic format
 */
export type AmbisonicFormat = 'acn_sn3d' | 'acn_n3d' | 'fuma' | 'tbe';

/**
 * Distance attenuation models
 */
export type DistanceModel = 'inverse' | 'inverse_clamped' | 'linear' | 'linear_clamped' | 'exponential' | 'custom';

/**
 * Spatialization configuration
 */
export interface Spatialization {
  algorithm?: SpatializationAlgorithm;
  ambisonics_order?: number;
  format?: AmbisonicFormat;
  distance_model?: DistanceModel;
  reference_distance_m?: number;
  max_distance_m?: number;
  rolloff_factor?: number;
  doppler_enabled?: boolean;
  doppler_factor?: number;
}

/**
 * Acoustic simulation methods
 */
export type SimulationMethod = 'ray_tracing' | 'image_source' | 'fdtd' | 'hybrid' | 'convolution' | 'parametric';

/**
 * Acoustic material presets
 */
export type AcousticMaterialPreset = 'concrete' | 'wood_panel' | 'carpet' | 'glass' | 'fabric' | 'metal' | 'acoustic_tile' | 'outdoor';

/**
 * Reverb presets
 */
export type ReverbPreset = 'small_room' | 'medium_room' | 'large_hall' | 'cathedral' | 'outdoor' | 'studio' | 'none';

/**
 * Ray tracing configuration for room acoustics
 */
export interface RayTracingConfig {
  ray_count?: number;
  max_bounces?: number;
  max_path_length_m?: number;
  diffuse_reflections?: boolean;
}

/**
 * Room materials using presets
 */
export interface RoomMaterialPresets {
  walls?: AcousticMaterialPreset;
  floor?: AcousticMaterialPreset;
  ceiling?: AcousticMaterialPreset;
}

/**
 * Room acoustics configuration
 */
export interface RoomAcoustics {
  enabled?: boolean;
  simulation_method?: SimulationMethod;
  ray_tracing?: RayTracingConfig;
  material_presets?: RoomMaterialPresets;
  reverb_preset?: ReverbPreset;
  occlusion_enabled?: boolean;
  transmission_enabled?: boolean;
}

/**
 * Head tracking recentering options
 */
export type RecenteringMode = 'manual' | 'automatic' | 'gaze_based';

/**
 * Head tracking configuration
 */
export interface HeadTracking {
  enabled?: boolean;
  update_rate_hz?: number;
  smoothing?: number;
  prediction_ms?: number;
  recentering?: RecenteringMode;
}

/**
 * Voice source attachment modes
 */
export type AttachmentMode = 'avatar_head' | 'world_position' | 'camera_relative' | 'custom_transform';

/**
 * Directivity pattern types
 */
export type DirectivityPattern = 'omnidirectional' | 'cardioid' | 'hypercardioid' | 'figure_8';

/**
 * Mouth offset position
 */
export interface MouthOffset {
  forward_cm?: number;
  up_cm?: number;
}

/**
 * Voice source configuration
 */
export interface VoiceSource {
  attachment_mode?: AttachmentMode;
  mouth_offset?: MouthOffset;
  directivity_pattern?: DirectivityPattern;
  directivity_sharpness?: number;
}

/**
 * Lip sync methods
 */
export type LipSyncMethod = 'viseme_driven' | 'audio_amplitude' | 'phoneme_mapping' | 'neural_realtime';

/**
 * Viseme sets
 */
export type VisemeSet = 'oculus_15' | 'arkit_52' | 'microsoft_22' | 'custom';

/**
 * Lip sync configuration
 */
export interface LipSync {
  enabled?: boolean;
  method?: LipSyncMethod;
  viseme_set?: VisemeSet;
  smoothing?: number;
  latency_compensation_ms?: number;
}

/**
 * Quality scaling thresholds
 */
export interface QualityScaling {
  cpu_threshold_percent?: number;
  fallback_to_stereo?: boolean;
  reduce_reflections_first?: boolean;
}

/**
 * Performance configuration
 */
export interface SpatialPerformance {
  max_concurrent_sources?: number;
  audio_thread_priority?: 'normal' | 'high' | 'realtime';
  quality_scaling?: QualityScaling;
}

/**
 * Passthrough AR environmental adaptation
 */
export interface EnvironmentalAdaptation {
  noise_adaptation?: boolean;
  echo_cancellation?: boolean;
  wind_noise_reduction?: boolean;
}

/**
 * Passthrough AR configuration
 */
export interface PassthroughAR {
  enabled?: boolean;
  blend_virtual_real?: number;
  spatial_anchoring?: boolean;
  environmental_adaptation?: EnvironmentalAdaptation;
}

/**
 * Complete VR/AR Spatial Audio configuration
 */
export interface VRARSpatialAudio {
  spatial_config_id: SpatialConfigId;
  persona_id: string;
  created_at?: string;
  updated_at?: string;
  platform: XRPlatform;
  
  /** HRTF configuration */
  hrtf?: HRTF;
  
  /** Spatialization settings */
  spatialization?: Spatialization;
  
  /** Room acoustics */
  room_acoustics?: RoomAcoustics;
  
  /** Head tracking */
  head_tracking?: HeadTracking;
  
  /** Voice source positioning */
  voice_source?: VoiceSource;
  
  /** Lip sync */
  lip_sync?: LipSync;
  
  /** Performance settings */
  performance?: SpatialPerformance;
  
  /** Passthrough AR options */
  passthrough_ar?: PassthroughAR;
}

// =============================================================================
// DAW PLUGIN TYPES
// =============================================================================

/**
 * Plugin ID format: plugin_[16 lowercase alphanumeric]
 */
export type PluginId = `plugin_${string}`;

/**
 * Plugin format types
 */
export type PluginFormat = 'vst3' | 'au' | 'aax' | 'clap' | 'lv2' | 'standalone';

/**
 * Supported platforms
 */
export type PluginPlatform = 'macos_intel' | 'macos_arm' | 'windows_x64' | 'linux_x64';

/**
 * Minimum OS version per platform
 */
export interface MinOSVersion {
  macos?: string;
  windows?: string;
  linux?: string;
}

/**
 * Plugin format specification
 */
export interface PluginFormatSpec {
  format: PluginFormat;
  supported_platforms: PluginPlatform[];
  min_os_version?: MinOSVersion;
  code_signed?: boolean;
  notarized?: boolean;
}

/**
 * DAW names
 */
export type DAWName = 
  | 'pro_tools' | 'logic_pro' | 'ableton_live' | 'cubase' | 'nuendo'
  | 'studio_one' | 'reaper' | 'fl_studio' | 'bitwig' | 'luna'
  | 'audition' | 'garageband' | 'reason' | 'digital_performer';

/**
 * DAW certification levels
 */
export type DAWCertification = 'certified' | 'compatible' | 'beta' | 'unsupported';

/**
 * DAW compatibility entry
 */
export interface DAWCompatibility {
  daw: DAWName;
  min_version: string;
  tested_version?: string;
  known_issues?: string[];
  certification: DAWCertification;
}

/**
 * Audio channel configurations
 */
export type ChannelConfig = 'mono' | 'stereo' | 'surround_5_1' | 'surround_7_1' | 'atmos' | 'ambisonics';

/**
 * Latency specification
 */
export interface LatencySpec {
  reported_samples?: number;
  actual_ms?: number;
  compensatable?: boolean;
}

/**
 * Audio specifications
 */
export interface AudioSpecs {
  supported_sample_rates?: number[];
  supported_bit_depths?: number[];
  supported_channel_configs?: ChannelConfig[];
  latency?: LatencySpec;
  realtime_safe?: boolean;
  offline_rendering?: boolean;
  offline_faster_than_realtime?: boolean;
}

/**
 * UI size specification
 */
export interface UISize {
  width?: number;
  height?: number;
}

/**
 * UI configuration
 */
export interface PluginUI {
  default_size?: UISize;
  resizable?: boolean;
  min_size?: UISize;
  max_size?: UISize;
  hidpi_support?: boolean;
  dark_mode?: boolean;
  theme_customization?: boolean;
  keyboard_shortcuts?: boolean;
  touch_support?: boolean;
}

/**
 * Automation curve types
 */
export type AutomationCurve = 'linear' | 'logarithmic' | 'exponential' | 'stepped';

/**
 * Parameter types
 */
export type ParameterType = 'float' | 'int' | 'bool' | 'enum';

/**
 * Automatable parameter
 */
export interface AutomatableParam {
  id: string;
  name: string;
  type: ParameterType;
  min?: number;
  max?: number;
  default?: number;
  unit?: string;
  automation_curve?: AutomationCurve;
}

/**
 * Preset format types
 */
export type PresetFormat = 'json' | 'xml' | 'binary' | 'fxp';

/**
 * Preset system configuration
 */
export interface PresetSystem {
  factory_presets?: number;
  user_presets_path?: string;
  preset_format?: PresetFormat;
  cloud_sync?: boolean;
  preset_morphing?: boolean;
}

/**
 * Plugin parameters
 */
export interface PluginParameters {
  automatable_params?: AutomatableParam[];
  preset_system?: PresetSystem;
}

/**
 * MIDI triggered speech config
 */
export interface MIDITriggeredSpeech {
  enabled?: boolean;
  note_to_phoneme_mapping?: boolean;
  velocity_to_intensity?: boolean;
  pitch_bend_range_semitones?: number;
}

/**
 * MIDI configuration
 */
export interface PluginMIDI {
  midi_input?: boolean;
  midi_output?: boolean;
  midi_learn?: boolean;
  mpe_support?: boolean;
  midi_triggered_speech?: MIDITriggeredSpeech;
}

/**
 * Script import formats
 */
export type ScriptFormat = 'txt' | 'docx' | 'pdf' | 'srt' | 'vtt' | 'fdx';

/**
 * Text input features
 */
export interface TextInputFeatures {
  direct_text_entry?: boolean;
  script_import?: ScriptFormat[];
  character_limit?: number;
}

/**
 * SSML editor features
 */
export interface SSMLEditorFeatures {
  visual_editor?: boolean;
  code_editor?: boolean;
  syntax_highlighting?: boolean;
  validation?: boolean;
  auto_complete?: boolean;
}

/**
 * Persona browser features
 */
export interface PersonaBrowserFeatures {
  preview_playback?: boolean;
  favorites?: boolean;
  search_filters?: boolean;
  license_status_display?: boolean;
}

/**
 * Waveform display features
 */
export interface WaveformDisplayFeatures {
  realtime_waveform?: boolean;
  spectrogram?: boolean;
  pitch_contour?: boolean;
  energy_envelope?: boolean;
  word_boundaries?: boolean;
}

/**
 * Editing features
 */
export interface EditingFeatures {
  word_level_timing_adjust?: boolean;
  phoneme_level_editing?: boolean;
  pitch_drawing?: boolean;
  breath_insertion?: boolean;
  take_comping?: boolean;
  undo_levels?: number;
}

/**
 * Export format types
 */
export type ExportFormat = 'wav' | 'aiff' | 'flac' | 'mp3' | 'aac' | 'ogg';

/**
 * Export features
 */
export interface ExportFeatures {
  bounce_to_track?: boolean;
  export_stems?: boolean;
  export_with_metadata?: boolean;
  export_formats?: ExportFormat[];
}

/**
 * Plugin features
 */
export interface PluginFeatures {
  text_input?: TextInputFeatures;
  ssml_editor?: SSMLEditorFeatures;
  persona_browser?: PersonaBrowserFeatures;
  waveform_display?: WaveformDisplayFeatures;
  editing?: EditingFeatures;
  export?: ExportFeatures;
}

/**
 * API authentication methods
 */
export type AuthMethod = 'api_key' | 'oauth2' | 'license_file';

/**
 * Retry policy
 */
export interface RetryPolicy {
  max_retries?: number;
  backoff_multiplier?: number;
}

/**
 * API connection configuration
 */
export interface APIConnection {
  endpoint?: string;
  auth_method?: AuthMethod;
  timeout_seconds?: number;
  retry_policy?: RetryPolicy;
}

/**
 * Offline mode configuration
 */
export interface OfflineMode {
  enabled?: boolean;
  cached_personas?: number;
  cache_size_mb?: number;
  sync_on_reconnect?: boolean;
}

/**
 * Usage tracking configuration
 */
export interface UsageTracking {
  track_generations?: boolean;
  track_render_time?: boolean;
  anonymous_analytics?: boolean;
}

/**
 * Networking configuration
 */
export interface PluginNetworking {
  api_connection?: APIConnection;
  offline_mode?: OfflineMode;
  usage_tracking?: UsageTracking;
}

/**
 * License model types
 */
export type LicenseModel = 'subscription' | 'perpetual' | 'rent_to_own' | 'usage_based';

/**
 * Plugin licensing configuration
 */
export interface PluginLicensing {
  license_model?: LicenseModel;
  machine_activations?: number;
  ilok_support?: boolean;
  offline_activation_days?: number;
  educational_discount?: boolean;
}

/**
 * Complete DAW Plugin configuration
 */
export interface DAWPlugin {
  plugin_id: PluginId;
  version: string;
  formats: PluginFormatSpec[];
  
  /** DAW compatibility matrix */
  daw_compatibility?: DAWCompatibility[];
  
  /** Audio specifications */
  audio_specs?: AudioSpecs;
  
  /** UI configuration */
  ui?: PluginUI;
  
  /** Parameters and presets */
  parameters?: PluginParameters;
  
  /** MIDI configuration */
  midi?: PluginMIDI;
  
  /** Plugin features */
  features?: PluginFeatures;
  
  /** Networking configuration */
  networking?: PluginNetworking;
  
  /** Licensing */
  licensing?: PluginLicensing;
}

// =============================================================================
// GAME ENGINE SDK TYPES
// =============================================================================

/**
 * SDK ID format: sdk_[16 lowercase alphanumeric]
 */
export type SDKId = `sdk_${string}`;

/**
 * Game engine types
 */
export type GameEngine = 'unity' | 'unreal' | 'godot' | 'cryengine' | 'lumberyard' | 'defold' | 'cocos' | 'custom';

/**
 * SDK installation methods
 */
export type SDKInstallMethod = 'package_manager' | 'asset_store' | 'marketplace' | 'manual' | 'git_submodule';

/**
 * Engine specification
 */
export interface EngineSpec {
  engine: GameEngine;
  min_version: string;
  recommended_version?: string;
  installation_method?: SDKInstallMethod;
  package_url?: string;
}

/**
 * SDK platform types
 */
export type SDKPlatform = 
  | 'windows' | 'macos' | 'linux' 
  | 'ios' | 'android' | 'webgl'
  | 'ps5' | 'xbox_series' | 'nintendo_switch'
  | 'meta_quest' | 'psvr2';

/**
 * CPU architecture types
 */
export type CPUArchitecture = 'x64' | 'arm64' | 'armv7' | 'wasm';

/**
 * Platform certification status
 */
export type CertificationStatus = 'certified' | 'pending' | 'not_submitted' | 'rejected';

/**
 * Minimum platform requirements
 */
export interface MinRequirements {
  ram_mb?: number;
  storage_mb?: number;
  gpu_required?: boolean;
}

/**
 * Platform specification
 */
export interface PlatformSpec {
  platform: SDKPlatform;
  architecture: CPUArchitecture;
  min_requirements?: MinRequirements;
  certification_status?: CertificationStatus;
}

/**
 * Method parameter
 */
export interface MethodParameter {
  name?: string;
  type?: string;
  optional?: boolean;
}

/**
 * API method
 */
export interface APIMethod {
  name: string;
  async?: boolean;
  parameters?: MethodParameter[];
  return_type?: string;
  description?: string;
}

/**
 * Core API class
 */
export interface CoreClass {
  class_name: string;
  description?: string;
  singleton?: boolean;
  thread_safe?: boolean;
  methods?: APIMethod[];
}

/**
 * API event
 */
export interface APIEvent {
  event_name: string;
  payload_type?: string;
  description?: string;
}

/**
 * Example method
 */
export interface ExampleMethod {
  name?: string;
  signature?: string;
  description?: string;
}

/**
 * SDK API specification
 */
export interface SDKAPI {
  core_classes?: CoreClass[];
  events?: APIEvent[];
  example_methods?: ExampleMethod[];
}

/**
 * SDK components
 */
export interface SDKComponents {
  unity_components?: string[];
  unreal_components?: string[];
  godot_nodes?: string[];
  blueprints_included?: boolean;
  visual_scripting_support?: boolean;
}

/**
 * Dialogue system integrations
 */
export type DialogueIntegration = 'yarn_spinner' | 'ink' | 'dialogue_system' | 'articy_draft' | 'chat_mapper' | 'custom';

/**
 * Dialogue system features
 */
export interface DialogueFeatures {
  branching_dialogue?: boolean;
  variable_substitution?: boolean;
  emotion_tags?: boolean;
  localization_support?: boolean;
  audio_caching?: boolean;
  pregeneration?: boolean;
}

/**
 * Dialogue system configuration
 */
export interface DialogueSystem {
  integrations?: DialogueIntegration[];
  features?: DialogueFeatures;
}

/**
 * Lip sync methods for SDK
 */
export type SDKLipSyncMethod = 'realtime_audio' | 'precomputed_visemes' | 'blendshape_prediction' | 'bone_based';

/**
 * Lip sync target systems
 */
export type LipSyncTargetSystem = 
  | 'unity_blendshapes' | 'unreal_morph_targets' | 'live_link'
  | 'arkit_blendshapes' | 'oculus_lipsync' | 'salsa' | 'custom';

/**
 * SDK viseme sets
 */
export type SDKVisemeSet = 'oculus_15' | 'arkit_52' | 'microsoft_22' | 'rhubarb_9' | 'custom';

/**
 * Lip sync performance metrics
 */
export interface LipSyncPerformance {
  latency_ms?: number;
  update_rate_hz?: number;
  cpu_overhead_percent?: number;
}

/**
 * SDK lip sync configuration
 */
export interface SDKLipSync {
  methods?: SDKLipSyncMethod[];
  target_systems?: LipSyncTargetSystem[];
  viseme_sets?: SDKVisemeSet[];
  performance?: LipSyncPerformance;
}

/**
 * Cache strategy types
 */
export type CacheStrategy = 'lru' | 'lfu' | 'fifo' | 'priority';

/**
 * SDK caching configuration
 */
export interface SDKCaching {
  memory_cache_mb?: number;
  disk_cache_mb?: number;
  cache_strategy?: CacheStrategy;
  preload_common_phrases?: boolean;
  background_generation?: boolean;
  predictive_caching?: boolean;
}

/**
 * Multiplayer sync methods
 */
export type SyncMethod = 'audio_stream' | 'text_sync' | 'playback_timestamp';

/**
 * Network library types
 */
export type NetworkLibrary = 'netcode' | 'photon' | 'mirror' | 'fishnet' | 'epic_eos';

/**
 * Multiplayer sync configuration
 */
export interface MultiplayerSync {
  supported?: boolean;
  sync_methods?: SyncMethod[];
  network_libraries?: NetworkLibrary[];
}

/**
 * SDK offline mode
 */
export interface SDKOfflineMode {
  enabled?: boolean;
  bundled_personas?: number;
  model_size_mb?: number;
}

/**
 * SDK networking configuration
 */
export interface SDKNetworking {
  multiplayer_sync?: MultiplayerSync;
  offline_mode?: SDKOfflineMode;
}

/**
 * Editor tools configuration
 */
export interface EditorTools {
  preview_window?: boolean;
  batch_generation?: boolean;
  script_import?: boolean;
  waveform_preview?: boolean;
  ssml_editor?: boolean;
  persona_browser?: boolean;
  usage_dashboard?: boolean;
}

/**
 * Sample project
 */
export interface SampleProject {
  name?: string;
  engine?: string;
  description?: string;
  download_url?: string;
}

/**
 * SDK documentation
 */
export interface SDKDocumentation {
  api_reference_url?: string;
  tutorials_url?: string;
  sample_projects?: SampleProject[];
  video_tutorials?: boolean;
  discord_support?: string;
}

/**
 * Complete Game Engine SDK configuration
 */
export interface GameEngineSDK {
  sdk_id: SDKId;
  version: string;
  engines: EngineSpec[];
  
  /** Supported platforms */
  platforms?: PlatformSpec[];
  
  /** API specification */
  api?: SDKAPI;
  
  /** Pre-built components */
  components?: SDKComponents;
  
  /** Dialogue system integration */
  dialogue_system?: DialogueSystem;
  
  /** Lip sync configuration */
  lip_sync?: SDKLipSync;
  
  /** Caching configuration */
  caching?: SDKCaching;
  
  /** Networking configuration */
  networking?: SDKNetworking;
  
  /** Editor tools */
  editor_tools?: EditorTools;
  
  /** Documentation */
  documentation?: SDKDocumentation;
}

// =============================================================================
// ANALYTICS DASHBOARD TYPES
// =============================================================================

/**
 * Dashboard ID format: dash_[16 lowercase alphanumeric]
 */
export type DashboardId = `dash_${string}`;

/**
 * Dashboard owner types
 */
export type DashboardOwnerType = 'artist' | 'licensee' | 'platform' | 'guild';

/**
 * Time range presets
 */
export type TimeRangePreset = 
  | 'today' | 'yesterday' | 'last_7_days' | 'last_30_days' | 'last_90_days'
  | 'this_month' | 'last_month' | 'this_year' | 'all_time' | 'custom';

/**
 * Time granularity options
 */
export type TimeGranularity = 'minute' | 'hour' | 'day' | 'week' | 'month';

/**
 * Time range configuration
 */
export interface TimeRange {
  preset?: TimeRangePreset;
  start?: string;
  end?: string;
  timezone?: string;
  granularity?: TimeGranularity;
}

/**
 * Earnings by license tier
 */
export interface EarningsByTier {
  micro?: number;
  non_exclusive?: number;
  exclusive?: number;
  enterprise?: number;
}

/**
 * Earnings trend entry
 */
export interface EarningsTrendEntry {
  period?: string;
  amount?: number;
}

/**
 * Top earning persona
 */
export interface TopEarningPersona {
  persona_id?: string;
  earnings_usd?: number;
}

/**
 * Revenue metrics
 */
export interface RevenueMetrics {
  total_earnings_usd?: number;
  pending_payout_usd?: number;
  last_payout_usd?: number;
  last_payout_date?: string;
  earnings_by_tier?: EarningsByTier;
  earnings_trend?: EarningsTrendEntry[];
  top_earning_personas?: TopEarningPersona[];
}

/**
 * Generations trend entry
 */
export interface GenerationsTrendEntry {
  period?: string;
  count?: number;
}

/**
 * Usage by persona
 */
export interface UsageByPersona {
  persona_id?: string;
  generations?: number;
  minutes?: number;
}

/**
 * Usage by geography
 */
export interface UsageByGeography {
  country?: string;
  generations?: number;
}

/**
 * Use case types
 */
export type UseCaseType = 'narration' | 'gaming' | 'animation' | 'advertising' | 'education' | 'podcast' | 'other';

/**
 * Usage by use case
 */
export interface UsageByUseCase {
  use_case?: UseCaseType;
  generations?: number;
}

/**
 * Usage metrics
 */
export interface UsageMetrics {
  total_generations?: number;
  total_audio_minutes?: number;
  total_characters_synthesized?: number;
  unique_licensees?: number;
  generations_trend?: GenerationsTrendEntry[];
  usage_by_persona?: UsageByPersona[];
  usage_by_geography?: UsageByGeography[];
  usage_by_use_case?: UsageByUseCase[];
}

/**
 * Licenses by tier
 */
export interface LicensesByTier {
  micro?: number;
  non_exclusive?: number;
  exclusive?: number;
  enterprise?: number;
}

/**
 * Licensing metrics
 */
export interface LicensingMetrics {
  active_licenses?: number;
  new_licenses_period?: number;
  churned_licenses_period?: number;
  license_renewal_rate?: number;
  licenses_by_tier?: LicensesByTier;
}

/**
 * Rating distribution
 */
export interface RatingDistribution {
  '5_star'?: number;
  '4_star'?: number;
  '3_star'?: number;
  '2_star'?: number;
  '1_star'?: number;
}

/**
 * Feedback sentiment
 */
export type FeedbackSentiment = 'positive' | 'neutral' | 'negative';

/**
 * Feedback theme
 */
export interface FeedbackTheme {
  theme?: string;
  sentiment?: FeedbackSentiment;
  count?: number;
}

/**
 * Quality metrics
 */
export interface QualityMetrics {
  average_rating?: number;
  total_ratings?: number;
  rating_distribution?: RatingDistribution;
  feedback_themes?: FeedbackTheme[];
}

/**
 * Competitor comparison
 */
export interface CompetitorComparison {
  archetype?: string;
  your_rank?: number;
  total_in_category?: number;
}

/**
 * Marketplace metrics
 */
export interface MarketplaceMetrics {
  profile_views?: number;
  sample_plays?: number;
  conversion_rate?: number;
  search_appearances?: number;
  search_ranking_avg?: number;
  competitor_comparison?: CompetitorComparison;
}

/**
 * Artist metrics
 */
export interface ArtistMetrics {
  revenue?: RevenueMetrics;
  usage?: UsageMetrics;
  licensing?: LicensingMetrics;
  quality?: QualityMetrics;
  marketplace?: MarketplaceMetrics;
}

/**
 * Platform-wide metrics (admin only)
 */
export interface PlatformMetrics {
  total_revenue_usd?: number;
  total_artist_payouts_usd?: number;
  platform_revenue_usd?: number;
  total_generations?: number;
  total_audio_hours?: number;
  active_artists?: number;
  active_licensees?: number;
  new_artists_period?: number;
  new_licensees_period?: number;
  churn_rate_artists?: number;
  churn_rate_licensees?: number;
  api_requests?: number;
  api_error_rate?: number;
  average_latency_ms?: number;
  p99_latency_ms?: number;
  uptime_percent?: number;
  moderation_queue_size?: number;
  takedowns_period?: number;
  disputes_period?: number;
}

/**
 * Alert types
 */
export type AlertType = 
  | 'revenue_milestone' | 'usage_spike' | 'rating_drop' 
  | 'license_expiring' | 'payout_ready' | 'moderation_action' | 'system_issue';

/**
 * Alert severity
 */
export type AlertSeverity = 'info' | 'warning' | 'critical';

/**
 * Dashboard alert
 */
export interface DashboardAlert {
  alert_id: string;
  type: AlertType;
  severity: AlertSeverity;
  message: string;
  created_at?: string;
  acknowledged?: boolean;
  action_url?: string;
}

/**
 * Report frequency
 */
export type ReportFrequency = 'daily' | 'weekly' | 'monthly';

/**
 * Scheduled report
 */
export interface ScheduledReport {
  report_name?: string;
  frequency?: ReportFrequency;
  format?: string;
  recipients?: string[];
}

/**
 * Audit export configuration
 */
export interface AuditExport {
  enabled?: boolean;
  includes_manifests?: boolean;
  includes_usage_logs?: boolean;
  retention_days?: number;
}

/**
 * Export format types
 */
export type DashboardExportFormat = 'csv' | 'xlsx' | 'json' | 'pdf';

/**
 * Dashboard exports
 */
export interface DashboardExports {
  available_formats?: DashboardExportFormat[];
  scheduled_reports?: ScheduledReport[];
  audit_export?: AuditExport;
}

/**
 * Complete Analytics Dashboard configuration
 */
export interface AnalyticsDashboard {
  dashboard_id: DashboardId;
  owner_type: DashboardOwnerType;
  owner_id: string;
  
  /** Time range for metrics */
  time_range?: TimeRange;
  
  /** Artist-specific metrics */
  artist_metrics?: ArtistMetrics;
  
  /** Platform-wide metrics (admin only) */
  platform_metrics?: PlatformMetrics;
  
  /** Active alerts */
  alerts?: DashboardAlert[];
  
  /** Export configuration */
  exports?: DashboardExports;
}

// ============================================================================
// ENTERPRISE DEPLOYMENT TYPES
// ============================================================================

/**
 * Enterprise deployment ID pattern: ent_[16 alphanumeric]
 */
export type EnterpriseDeploymentId = `ent_${string}`;

/**
 * Organization details
 */
export interface EnterpriseOrganization {
  org_id: string;
  name: string;
  industry?: string;
  size?: 'startup' | 'small' | 'medium' | 'large' | 'enterprise' | 'fortune_500';
  headquarters_country?: string;
  subsidiaries?: string[];
}

/**
 * Deployment types
 */
export type DeploymentType = 
  | 'cloud_dedicated'
  | 'hybrid'
  | 'on_premise'
  | 'air_gapped'
  | 'edge';

/**
 * Cloud providers
 */
export type CloudProvider = 
  | 'aws'
  | 'gcp'
  | 'azure'
  | 'oracle'
  | 'ibm'
  | 'private'
  | 'multi_cloud';

/**
 * GPU types
 */
export type GpuType = 'A100' | 'H100' | 'A10G' | 'L4' | 'T4';

/**
 * Dedicated compute configuration
 */
export interface DedicatedCompute {
  gpu_type?: GpuType;
  gpu_count?: number;
  cpu_cores?: number;
  ram_gb?: number;
  storage_tb?: number;
  network_bandwidth_gbps?: number;
}

/**
 * Kubernetes distributions
 */
export type KubernetesDistribution = 
  | 'eks'
  | 'gke'
  | 'aks'
  | 'openshift'
  | 'rancher'
  | 'tanzu'
  | 'k3s'
  | 'self_managed';

/**
 * Kubernetes configuration
 */
export interface KubernetesConfig {
  enabled: boolean;
  distribution?: KubernetesDistribution;
  namespace?: string;
  helm_chart_version?: string;
  auto_scaling?: boolean;
  min_replicas?: number;
  max_replicas?: number;
}

/**
 * Infrastructure configuration
 */
export interface EnterpriseInfrastructure {
  cloud_provider?: CloudProvider;
  regions?: string[];
  dedicated_compute?: DedicatedCompute;
  kubernetes?: KubernetesConfig;
  vpc_peering?: boolean;
  private_endpoints?: boolean;
}

/**
 * SSO providers
 */
export type SsoProvider = 
  | 'okta'
  | 'azure_ad'
  | 'google_workspace'
  | 'onelogin'
  | 'ping'
  | 'saml_generic'
  | 'oidc_generic';

/**
 * SSO configuration
 */
export interface SsoConfig {
  provider: SsoProvider;
  tenant_id?: string;
  domain?: string;
  scim_provisioning?: boolean;
  mfa_required?: boolean;
}

/**
 * Role-based access control
 */
export interface RbacConfig {
  enabled: boolean;
  custom_roles?: string[];
  default_role?: string;
  admin_groups?: string[];
}

/**
 * Encryption modes
 */
export type EncryptionKeyMode = 
  | 'platform_managed'
  | 'customer_managed_keys'
  | 'bring_your_own_key'
  | 'hsm';

/**
 * Encryption configuration
 */
export interface EncryptionConfig {
  at_rest: boolean;
  in_transit: boolean;
  key_management?: EncryptionKeyMode;
  tls_version?: string;
  cipher_suites?: string[];
}

/**
 * Compliance certifications
 */
export type ComplianceCertification = 
  | 'soc2_type1'
  | 'soc2_type2'
  | 'iso27001'
  | 'hipaa'
  | 'gdpr'
  | 'ccpa'
  | 'fedramp_moderate'
  | 'fedramp_high'
  | 'pci_dss'
  | 'c5';

/**
 * Compliance configuration
 */
export interface ComplianceConfig {
  certifications?: ComplianceCertification[];
  data_residency?: string[];
  audit_logging?: boolean;
  log_retention_days?: number;
}

/**
 * Network security
 */
export interface NetworkSecurityConfig {
  ip_allowlist?: string[];
  waf_enabled?: boolean;
  ddos_protection?: boolean;
  intrusion_detection?: boolean;
}

/**
 * Complete security configuration
 */
export interface EnterpriseSecurityConfig {
  sso?: SsoConfig;
  rbac?: RbacConfig;
  encryption?: EncryptionConfig;
  compliance?: ComplianceConfig;
  network_security?: NetworkSecurityConfig;
}

/**
 * Persona access configuration
 */
export interface PersonaAccessConfig {
  access_type: 'full_catalog' | 'curated_subset' | 'custom_only';
  included_personas?: string[];
  excluded_personas?: string[];
  custom_persona_slots?: number;
  custom_training_hours?: number;
}

/**
 * Support tiers
 */
export type SupportTier = 'standard' | 'premium' | 'dedicated';

/**
 * Support SLAs
 */
export interface SupportSlaConfig {
  critical_response_hours?: number;
  high_response_hours?: number;
  medium_response_hours?: number;
  low_response_hours?: number;
}

/**
 * Support configuration
 */
export interface EnterpriseSupportConfig {
  tier: SupportTier;
  sla?: SupportSlaConfig;
  dedicated_csm?: boolean;
  csm_name?: string;
  dedicated_engineer?: boolean;
  onboarding_included?: boolean;
  training_hours?: number;
}

/**
 * Billing models
 */
export type BillingModel = 
  | 'usage_based'
  | 'committed_spend'
  | 'flat_fee'
  | 'hybrid';

/**
 * Billing configuration
 */
export interface EnterpriseBillingConfig {
  model: BillingModel;
  commitment_amount_usd?: number;
  overage_rate_per_unit?: number;
  billing_cycle?: 'monthly' | 'quarterly' | 'annually';
  payment_terms_days?: number;
  contract_term_months?: number;
  auto_renewal?: boolean;
}

/**
 * CI/CD integration
 */
export interface CiCdIntegration {
  type: 'github_actions' | 'gitlab_ci' | 'jenkins' | 'azure_devops' | 'circleci' | 'custom';
  repository_url?: string;
  pipeline_config?: string;
}

/**
 * External integrations
 */
export interface EnterpriseIntegrations {
  cicd?: CiCdIntegration;
  artifact_registry?: string;
  secrets_manager?: 'vault' | 'aws_secrets' | 'gcp_secrets' | 'azure_keyvault';
  monitoring?: ('datadog' | 'splunk' | 'prometheus' | 'cloudwatch' | 'stackdriver')[];
  ticketing?: 'jira' | 'servicenow' | 'zendesk' | 'pagerduty';
}

/**
 * Disaster recovery types
 */
export type DisasterRecoveryType = 
  | 'active_passive'
  | 'active_active'
  | 'pilot_light'
  | 'warm_standby';

/**
 * Backup frequency options
 */
export type BackupFrequency = 
  | 'continuous'
  | 'hourly'
  | 'daily'
  | 'weekly';

/**
 * Disaster recovery configuration
 */
export interface DisasterRecoveryConfig {
  enabled: boolean;
  type?: DisasterRecoveryType;
  rpo_hours?: number;
  rto_hours?: number;
  backup_frequency?: BackupFrequency;
  backup_regions?: string[];
  failover_automation?: boolean;
}

/**
 * Complete Enterprise Deployment configuration
 */
export interface EnterpriseDeployment {
  deployment_id: EnterpriseDeploymentId;
  organization: EnterpriseOrganization;
  deployment_type: DeploymentType;
  
  /** Infrastructure configuration */
  infrastructure?: EnterpriseInfrastructure;
  
  /** Security and compliance */
  security?: EnterpriseSecurityConfig;
  
  /** Persona access configuration */
  personas?: PersonaAccessConfig;
  
  /** Support tier and SLAs */
  support?: EnterpriseSupportConfig;
  
  /** Billing and contract */
  billing?: EnterpriseBillingConfig;
  
  /** External integrations */
  integrations?: EnterpriseIntegrations;
  
  /** Disaster recovery */
  disaster_recovery?: DisasterRecoveryConfig;
  
  /** Deployment status */
  status?: 'provisioning' | 'active' | 'suspended' | 'decommissioning';
  
  /** Activation timestamp */
  activated_at?: string;
  
  /** Last audit timestamp */
  last_audit_at?: string;
}

// ============================================================================
// LLM ORCHESTRATION TYPES
// ============================================================================

/**
 * LLM orchestration ID pattern: llm_[16 alphanumeric]
 */
export type LlmOrchestrationId = `llm_${string}`;

/**
 * LLM provider types
 */
export type LlmProvider = 
  | 'anthropic'
  | 'openai'
  | 'google'
  | 'cohere'
  | 'mistral'
  | 'llama'
  | 'custom';

/**
 * LLM capability types
 */
export type LlmCapability = 
  | 'script_enhancement'
  | 'emotion_inference'
  | 'ssml_generation'
  | 'character_consistency'
  | 'translation'
  | 'summarization'
  | 'content_moderation';

/**
 * LLM provider configuration
 */
export interface LlmProviderConfig {
  provider: LlmProvider;
  model: string;
  version?: string;
  priority: number;
  fallback?: boolean;
  rate_limit_rpm?: number;
  cost_per_1k_tokens?: number;
  max_context_tokens?: number;
  capabilities?: LlmCapability[];
}

/**
 * Script analysis features
 */
export interface ScriptAnalysisFeatures {
  emotion_arc_detection?: boolean;
  pacing_recommendations?: boolean;
  emphasis_suggestions?: boolean;
  breath_point_insertion?: boolean;
  dramatic_beat_identification?: boolean;
}

/**
 * Script enhancement features
 */
export interface ScriptEnhancementFeatures {
  auto_ssml_generation?: boolean;
  prosody_optimization?: boolean;
  emotion_tag_insertion?: boolean;
  pause_calibration?: boolean;
  pronunciation_correction?: boolean;
}

/**
 * Character direction features
 */
export interface CharacterDirectionFeatures {
  motivation_inference?: boolean;
  subtext_analysis?: boolean;
  relationship_dynamics?: boolean;
  arc_consistency?: boolean;
}

/**
 * Dramaturgy features
 */
export interface DramaturgyFeatures {
  script_analysis?: ScriptAnalysisFeatures;
  script_enhancement?: ScriptEnhancementFeatures;
  character_direction?: CharacterDirectionFeatures;
}

/**
 * Dramaturgy prompts
 */
export interface DramaturgyPrompts {
  system_prompt?: string;
  analysis_prompt_template?: string;
  enhancement_prompt_template?: string;
  ssml_generation_prompt_template?: string;
}

/**
 * Dramaturgy engine configuration
 */
export interface DramaturgyEngine {
  enabled?: boolean;
  features?: DramaturgyFeatures;
  prompts?: DramaturgyPrompts;
}

/**
 * Vector store provider types
 */
export type VectorStoreProvider = 
  | 'pinecone'
  | 'weaviate'
  | 'qdrant'
  | 'milvus'
  | 'chromadb'
  | 'pgvector'
  | 'custom';

/**
 * Vector index types
 */
export type VectorIndexType = 'hnsw' | 'ivf' | 'flat';

/**
 * Similarity metrics
 */
export type SimilarityMetric = 'cosine' | 'euclidean' | 'dot_product';

/**
 * Vector store configuration
 */
export interface VectorStoreConfig {
  provider?: VectorStoreProvider;
  embedding_model?: string;
  embedding_dimensions?: number;
  index_type?: VectorIndexType;
  similarity_metric?: SimilarityMetric;
}

/**
 * Persona knowledge base configuration
 */
export interface PersonaKnowledgeBase {
  character_backstory?: boolean;
  vocal_characteristics?: boolean;
  emotional_range?: boolean;
  speech_patterns?: boolean;
  catchphrases?: boolean;
  pronunciation_preferences?: boolean;
  previous_performances?: boolean;
}

/**
 * RAG retrieval configuration
 */
export interface RetrievalConfig {
  top_k?: number;
  similarity_threshold?: number;
  reranking_enabled?: boolean;
  context_window_tokens?: number;
}

/**
 * Persona consistency engine (RAG)
 */
export interface PersonaConsistencyEngine {
  enabled?: boolean;
  vector_store?: VectorStoreConfig;
  persona_knowledge_base?: PersonaKnowledgeBase;
  retrieval_config?: RetrievalConfig;
}

/**
 * Adaptation triggers
 */
export type AdaptationTrigger = 
  | 'user_feedback'
  | 'emotion_detection'
  | 'context_change'
  | 'audience_response'
  | 'time_of_day'
  | 'platform_context';

/**
 * Implicit feedback signals
 */
export type ImplicitSignal = 
  | 'skip_rate'
  | 'replay_rate'
  | 'completion_rate'
  | 'engagement_time';

/**
 * Explicit feedback signals
 */
export type ExplicitSignal = 
  | 'rating'
  | 'feedback_text'
  | 'preference_selection';

/**
 * Adaptation parameters
 */
export interface AdaptationParameters {
  pacing_adjustment_range?: number;
  energy_adjustment_range?: number;
  formality_adjustment?: boolean;
  vocabulary_adaptation?: boolean;
}

/**
 * Feedback loop configuration
 */
export interface FeedbackLoopConfig {
  implicit_signals?: ImplicitSignal[];
  explicit_signals?: ExplicitSignal[];
  learning_rate?: number;
  adaptation_delay_ms?: number;
}

/**
 * Real-time adaptation configuration
 */
export interface RealTimeAdaptation {
  enabled?: boolean;
  adaptation_triggers?: AdaptationTrigger[];
  adaptation_parameters?: AdaptationParameters;
  feedback_loop?: FeedbackLoopConfig;
}

/**
 * Reasoning format types
 */
export type ReasoningFormat = 'structured' | 'narrative' | 'minimal';

/**
 * Chain of thought configuration
 */
export interface ChainOfThoughtConfig {
  enabled?: boolean;
  expose_reasoning?: boolean;
  reasoning_format?: ReasoningFormat;
  include_alternatives?: boolean;
  confidence_scores?: boolean;
}

/**
 * Multi-turn context configuration
 */
export interface MultiTurnContext {
  enabled?: boolean;
  max_turns?: number;
  summarization_threshold_turns?: number;
  context_compression?: boolean;
  emotional_state_tracking?: boolean;
}

/**
 * LLM guardrails configuration
 */
export interface LlmGuardrails {
  content_filtering?: boolean;
  persona_boundary_enforcement?: boolean;
  artist_consent_verification?: boolean;
  output_validation?: boolean;
  hallucination_detection?: boolean;
  max_generation_attempts?: number;
}

/**
 * Complete LLM Orchestration configuration
 */
export interface LlmOrchestration {
  orchestration_id: LlmOrchestrationId;
  version: string;
  providers: LlmProviderConfig[];
  
  /** AI-powered script analysis and enhancement */
  dramaturgy_engine?: DramaturgyEngine;
  
  /** RAG-based persona consistency */
  persona_consistency_engine?: PersonaConsistencyEngine;
  
  /** Context-aware real-time adjustments */
  real_time_adaptation?: RealTimeAdaptation;
  
  /** Transparent reasoning for creative decisions */
  chain_of_thought?: ChainOfThoughtConfig;
  
  /** Conversation memory for interactive sessions */
  multi_turn_context?: MultiTurnContext;
  
  /** Safety and content guardrails */
  guardrails?: LlmGuardrails;
}

// ============================================================================
// EMOTION AI TYPES
// ============================================================================

/**
 * Emotion engine ID pattern: emo_[16 alphanumeric]
 */
export type EmotionEngineId = `emo_${string}`;

/**
 * Primary emotion types
 */
export type PrimaryEmotion = 
  | 'joy'
  | 'sadness'
  | 'anger'
  | 'fear'
  | 'surprise'
  | 'disgust'
  | 'contempt'
  | 'neutral';

/**
 * Dimensional range for VAD model
 */
export interface DimensionalRange {
  min: number;
  max: number;
}

/**
 * Valence-Arousal-Dominance dimensional model
 */
export interface DimensionalModel {
  valence?: DimensionalRange;
  arousal?: DimensionalRange;
  dominance?: DimensionalRange;
}

/**
 * Emotion taxonomy configuration
 */
export interface EmotionTaxonomy {
  primary_emotions?: string[];
  secondary_emotions?: string[];
  dimensional_model?: DimensionalModel;
  intensity_levels?: string[];
}

/**
 * Emotion analysis model types
 */
export type EmotionModelType = 'transformer' | 'llm' | 'ensemble' | 'rule_based';

/**
 * Emotion analysis model configuration
 */
export interface EmotionAnalysisModel {
  model_name: string;
  model_type: EmotionModelType;
  accuracy?: number;
  latency_ms?: number;
}

/**
 * Text emotion analysis features
 */
export interface TextEmotionFeatures {
  sentence_level?: boolean;
  word_level?: boolean;
  context_aware?: boolean;
  sarcasm_detection?: boolean;
  implicit_emotion?: boolean;
  cultural_adaptation?: boolean;
}

/**
 * Emotion analysis output format
 */
export interface EmotionOutputFormat {
  primary_emotion?: boolean;
  emotion_probabilities?: boolean;
  dimensional_values?: boolean;
  emotion_trajectory?: boolean;
  suggested_prosody?: boolean;
}

/**
 * Text emotion analysis configuration
 */
export interface TextEmotionAnalysis {
  enabled?: boolean;
  models?: EmotionAnalysisModel[];
  features?: TextEmotionFeatures;
  output_format?: EmotionOutputFormat;
}

/**
 * Synthesis method types
 */
export type SynthesisMethod = 'parametric' | 'neural' | 'hybrid' | 'diffusion';

/**
 * Prosody mapping for an emotion
 */
export interface EmotionProsodyMapping {
  pitch_shift_percent?: number;
  pitch_range_multiplier?: number;
  rate_multiplier?: number;
  energy_multiplier?: number;
  breathiness?: number;
  tremolo_amount?: number;
  articulation_style?: string;
  pause_tendency?: number;
}

/**
 * Emotion blending method types
 */
export type BlendingMethod = 'linear' | 'weighted' | 'attention' | 'neural';

/**
 * Emotion blending configuration
 */
export interface EmotionBlending {
  enabled?: boolean;
  max_simultaneous_emotions?: number;
  blending_method?: BlendingMethod;
  transition_smoothing_ms?: number;
}

/**
 * Micro-expression configuration
 */
export interface MicroExpressions {
  enabled?: boolean;
  hesitation_markers?: boolean;
  breath_variations?: boolean;
  pitch_wobble?: boolean;
  volume_fluctuations?: boolean;
}

/**
 * Emotion synthesis configuration
 */
export interface EmotionSynthesis {
  enabled?: boolean;
  synthesis_method?: SynthesisMethod;
  emotion_to_prosody_mapping?: Record<string, EmotionProsodyMapping>;
  emotion_blending?: EmotionBlending;
  micro_expressions?: MicroExpressions;
}

/**
 * Emotion reference types
 */
export type EmotionReferenceType = 
  | 'audio_clip'
  | 'text_description'
  | 'dimensional_values'
  | 'emotion_label'
  | 'video_reference';

/**
 * Style encoder architecture types
 */
export type StyleEncoderArchitecture = 'gst' | 'vae' | 'flow' | 'diffusion';

/**
 * Style encoder configuration
 */
export interface StyleEncoder {
  architecture?: StyleEncoderArchitecture;
  embedding_dim?: number;
  disentanglement?: boolean;
}

/**
 * Emotion intensity control
 */
export interface EmotionIntensityControl {
  global_intensity?: number;
  per_emotion_intensity?: boolean;
}

/**
 * Emotion transfer configuration
 */
export interface EmotionTransfer {
  enabled?: boolean;
  reference_types?: EmotionReferenceType[];
  style_encoder?: StyleEncoder;
  intensity_control?: EmotionIntensityControl;
}

/**
 * Emotion tracking source types
 */
export type TrackingSource = 
  | 'user_voice'
  | 'user_text'
  | 'physiological'
  | 'facial'
  | 'context';

/**
 * Voice analysis feature types
 */
export type VoiceAnalysisFeature = 
  | 'pitch'
  | 'energy'
  | 'mfcc'
  | 'spectral'
  | 'prosodic'
  | 'linguistic';

/**
 * User voice analysis configuration
 */
export interface UserVoiceAnalysis {
  enabled?: boolean;
  features?: VoiceAnalysisFeature[];
  update_rate_hz?: number;
  latency_ms?: number;
}

/**
 * Emotion adaptation response configuration
 */
export interface AdaptationResponse {
  mirror_user_emotion?: boolean;
  complement_user_emotion?: boolean;
  maintain_character?: boolean;
  escalation_handling?: boolean;
}

/**
 * Real-time emotion tracking configuration
 */
export interface RealTimeEmotionTracking {
  enabled?: boolean;
  tracking_sources?: TrackingSource[];
  user_voice_analysis?: UserVoiceAnalysis;
  adaptation_response?: AdaptationResponse;
}

/**
 * Emotion memory configuration
 */
export interface EmotionMemory {
  enabled?: boolean;
  session_emotion_history?: boolean;
  cross_session_patterns?: boolean;
  emotional_arc_tracking?: boolean;
  relationship_emotion_modeling?: boolean;
}

/**
 * Complete Emotion AI configuration
 */
export interface EmotionAI {
  emotion_engine_id: EmotionEngineId;
  version: string;
  
  /** Emotion classification taxonomy */
  emotion_taxonomy?: EmotionTaxonomy;
  
  /** Text-based emotion inference */
  text_emotion_analysis?: TextEmotionAnalysis;
  
  /** Emotion-to-voice synthesis */
  emotion_synthesis?: EmotionSynthesis;
  
  /** Emotion transfer from reference */
  emotion_transfer?: EmotionTransfer;
  
  /** Real-time emotion tracking */
  real_time_emotion_tracking?: RealTimeEmotionTracking;
  
  /** Long-term emotional context */
  emotion_memory?: EmotionMemory;
}

// ============================================================================
// VOICE CLONING PIPELINE TYPES
// ============================================================================

/**
 * Voice cloning pipeline ID pattern: clone_[16 alphanumeric]
 */
export type VoiceCloningPipelineId = `clone_${string}`;

/**
 * Pipeline status types
 */
export type PipelineStatus = 
  | 'initiated'
  | 'recording'
  | 'processing'
  | 'training'
  | 'validation'
  | 'review'
  | 'approved'
  | 'published'
  | 'rejected';

/**
 * Recording session types
 */
export type RecordingSessionType = 
  | 'studio_guided'
  | 'remote_guided'
  | 'self_service'
  | 'existing_catalog';

/**
 * Script types
 */
export type ScriptType = 'provided' | 'custom' | 'improvised' | 'mixed';

/**
 * Script coverage configuration
 */
export interface ScriptCoverage {
  phoneme_coverage_percent?: number;
  diphone_coverage_percent?: number;
  emotion_coverage?: string[];
  prosody_variety_score?: number;
}

/**
 * Audio format types
 */
export type AudioFormat = 'wav' | 'flac' | 'aiff';

/**
 * Recording technical requirements
 */
export interface RecordingTechnicalRequirements {
  sample_rate_hz?: number;
  bit_depth?: 16 | 24 | 32;
  format?: AudioFormat;
  max_noise_floor_db?: number;
  max_thd_percent?: number;
  room_tone_required?: boolean;
  pop_filter_required?: boolean;
}

/**
 * Recording script category types
 */
export type RecordingCategory = 
  | 'phoneme_coverage'
  | 'emotion_neutral'
  | 'emotion_joy'
  | 'emotion_sadness'
  | 'emotion_anger'
  | 'emotion_fear'
  | 'emotion_surprise'
  | 'whisper'
  | 'shout'
  | 'conversational'
  | 'narrative'
  | 'commercial'
  | 'character';

/**
 * Recording script category configuration
 */
export interface RecordingScriptCategory {
  category: RecordingCategory;
  sentence_count?: number;
  duration_minutes?: number;
}

/**
 * Recording script configuration
 */
export interface RecordingScript {
  total_sentences?: number;
  categories?: RecordingScriptCategory[];
}

/**
 * Recording session configuration
 */
export interface RecordingSession {
  session_type?: RecordingSessionType;
  target_duration_minutes?: number;
  minimum_duration_minutes?: number;
  optimal_duration_minutes?: number;
  script_type?: ScriptType;
  script_coverage?: ScriptCoverage;
  technical_requirements?: RecordingTechnicalRequirements;
  recording_script?: RecordingScript;
}

/**
 * Noise reduction algorithm types
 */
export type NoiseReductionAlgorithm = 
  | 'spectral_subtraction'
  | 'wiener'
  | 'rnn'
  | 'diffusion';

/**
 * Noise reduction configuration
 */
export interface NoiseReduction {
  enabled?: boolean;
  algorithm?: NoiseReductionAlgorithm;
  aggressiveness?: number;
}

/**
 * Audio normalization configuration
 */
export interface AudioNormalization {
  enabled?: boolean;
  target_lufs?: number;
  peak_limit_db?: number;
}

/**
 * Silence trimming configuration
 */
export interface SilenceTrimming {
  enabled?: boolean;
  threshold_db?: number;
  min_silence_ms?: number;
  padding_ms?: number;
}

/**
 * Breath action types
 */
export type BreathAction = 'keep' | 'reduce' | 'remove' | 'normalize';

/**
 * Breath detection configuration
 */
export interface BreathDetection {
  enabled?: boolean;
  action?: BreathAction;
}

/**
 * Audio preprocessing configuration
 */
export interface AudioPreprocessing {
  noise_reduction?: NoiseReduction;
  normalization?: AudioNormalization;
  silence_trimming?: SilenceTrimming;
  breath_detection?: BreathDetection;
}

/**
 * Segmentation method types
 */
export type SegmentationMethod = 'forced_alignment' | 'vad' | 'manual' | 'hybrid';

/**
 * Segmentation output format types
 */
export type SegmentationOutputFormat = 'textgrid' | 'json' | 'ctm';

/**
 * Segmentation granularity types
 */
export type SegmentationGranularity = 'sentence' | 'word' | 'phoneme';

/**
 * Audio segmentation configuration
 */
export interface AudioSegmentation {
  method?: SegmentationMethod;
  forced_alignment_model?: string;
  output_format?: SegmentationOutputFormat;
  granularity?: SegmentationGranularity;
}

/**
 * Quality filtering configuration
 */
export interface QualityFiltering {
  snr_threshold_db?: number;
  clipping_detection?: boolean;
  alignment_confidence_threshold?: number;
  pronunciation_error_detection?: boolean;
  auto_reject_threshold?: number;
}

/**
 * Audio processing configuration
 */
export interface AudioProcessing {
  preprocessing?: AudioPreprocessing;
  segmentation?: AudioSegmentation;
  quality_filtering?: QualityFiltering;
}

/**
 * TTS base model types
 */
export type TtsBaseModel = 
  | 'vits'
  | 'vits2'
  | 'naturalspeech'
  | 'naturalspeech2'
  | 'voicebox'
  | 'xtts'
  | 'tortoise'
  | 'bark'
  | 'custom';

/**
 * Vocoder types
 */
export type VocoderType = 
  | 'hifigan'
  | 'bigvgan'
  | 'vocos'
  | 'waveglow'
  | 'universal'
  | 'diffusion';

/**
 * Speaker encoder types
 */
export type SpeakerEncoderType = 
  | 'ge2e'
  | 'resemblyzer'
  | 'ecapa_tdnn'
  | 'wavlm'
  | 'custom';

/**
 * Emotion encoder types for training
 */
export type TrainingEmotionEncoder = 'gst' | 'vae' | 'flow' | 'none';

/**
 * Model architecture configuration
 */
export interface ModelArchitecture {
  base_model?: TtsBaseModel;
  vocoder?: VocoderType;
  speaker_encoder?: SpeakerEncoderType;
  emotion_encoder?: TrainingEmotionEncoder;
}

/**
 * GPU types for training
 */
export type TrainingGpuType = 'A100' | 'H100' | 'A10G' | 'V100';

/**
 * Training configuration
 */
export interface TrainingConfig {
  epochs?: number;
  batch_size?: number;
  learning_rate?: number;
  warmup_steps?: number;
  gradient_accumulation?: number;
  mixed_precision?: boolean;
  distributed_training?: boolean;
  gpu_type?: TrainingGpuType;
  gpu_count?: number;
  estimated_training_hours?: number;
}

/**
 * Data augmentation technique types
 */
export type AugmentationTechnique = 
  | 'pitch_shift'
  | 'time_stretch'
  | 'noise_injection'
  | 'room_impulse'
  | 'formant_shift'
  | 'specaugment';

/**
 * Data augmentation configuration
 */
export interface DataAugmentation {
  enabled?: boolean;
  techniques?: AugmentationTechnique[];
}

/**
 * Fine-tuning configuration
 */
export interface FineTuningConfig {
  base_checkpoint?: string;
  frozen_layers?: string[];
  adapter_training?: boolean;
  lora_enabled?: boolean;
  lora_rank?: number;
}

/**
 * Best model metric types
 */
export type BestModelMetric = 'loss' | 'mel_loss' | 'mos_score' | 'speaker_similarity';

/**
 * Checkpointing configuration
 */
export interface CheckpointingConfig {
  save_frequency_steps?: number;
  keep_last_n?: number;
  best_model_metric?: BestModelMetric;
}

/**
 * Model training configuration
 */
export interface ModelTraining {
  architecture?: ModelArchitecture;
  training_config?: TrainingConfig;
  data_augmentation?: DataAugmentation;
  fine_tuning?: FineTuningConfig;
  checkpointing?: CheckpointingConfig;
}

/**
 * MOS prediction model types
 */
export type MosPredictionModel = 'utmos' | 'nisqa' | 'dnsmos' | 'mosnet';

/**
 * MOS prediction configuration
 */
export interface MosPrediction {
  model?: MosPredictionModel;
  threshold?: number;
}

/**
 * Speaker similarity model types
 */
export type SpeakerSimilarityModel = 'resemblyzer' | 'ecapa_tdnn' | 'wavlm';

/**
 * Speaker similarity configuration
 */
export interface SpeakerSimilarity {
  model?: SpeakerSimilarityModel;
  threshold?: number;
}

/**
 * Intelligibility model types
 */
export type IntelligibilityModel = 'whisper' | 'wav2vec2' | 'conformer';

/**
 * Intelligibility configuration
 */
export interface IntelligibilityConfig {
  model?: IntelligibilityModel;
  wer_threshold?: number;
}

/**
 * Emotion accuracy configuration
 */
export interface EmotionAccuracyConfig {
  model?: string;
  accuracy_threshold?: number;
}

/**
 * Automatic metrics configuration
 */
export interface AutomaticMetrics {
  mos_prediction?: MosPrediction;
  speaker_similarity?: SpeakerSimilarity;
  intelligibility?: IntelligibilityConfig;
  emotion_accuracy?: EmotionAccuracyConfig;
}

/**
 * Human evaluation metric types
 */
export type HumanEvaluationMetric = 
  | 'naturalness'
  | 'similarity'
  | 'emotion_match'
  | 'intelligibility'
  | 'overall_quality';

/**
 * Human evaluation configuration
 */
export interface HumanEvaluation {
  required?: boolean;
  evaluator_count?: number;
  evaluation_samples?: number;
  metrics?: HumanEvaluationMetric[];
  passing_threshold?: number;
}

/**
 * Artist approval configuration
 */
export interface ArtistApproval {
  required?: boolean;
  sample_generation_count?: number;
  approval_deadline_days?: number;
  revision_rounds_allowed?: number;
}

/**
 * Validation configuration
 */
export interface ValidationConfig {
  automatic_metrics?: AutomaticMetrics;
  human_evaluation?: HumanEvaluation;
  artist_approval?: ArtistApproval;
}

/**
 * Quantization precision types
 */
export type QuantizationPrecision = 'fp32' | 'fp16' | 'int8' | 'int4';

/**
 * Quantization method types
 */
export type QuantizationMethod = 'ptq' | 'qat' | 'gptq' | 'awq';

/**
 * Quantization configuration
 */
export interface QuantizationConfig {
  enabled?: boolean;
  precision?: QuantizationPrecision;
  method?: QuantizationMethod;
}

/**
 * Pruning configuration
 */
export interface PruningConfig {
  enabled?: boolean;
  sparsity_target?: number;
}

/**
 * Distillation configuration
 */
export interface DistillationConfig {
  enabled?: boolean;
  student_architecture?: string;
}

/**
 * Export format types
 */
export type ModelExportFormat = 
  | 'pytorch'
  | 'onnx'
  | 'tensorrt'
  | 'coreml'
  | 'tflite'
  | 'openvino';

/**
 * Model optimization configuration
 */
export interface ModelOptimization {
  quantization?: QuantizationConfig;
  pruning?: PruningConfig;
  distillation?: DistillationConfig;
  export_formats?: ModelExportFormat[];
}

/**
 * Model versioning configuration
 */
export interface ModelVersioning {
  model_version?: string;
  parent_version?: string;
  changelog?: string;
  training_data_hash?: string;
  config_hash?: string;
  created_at?: string;
}

/**
 * Complete Voice Cloning Pipeline configuration
 */
export interface VoiceCloningPipeline {
  pipeline_id: VoiceCloningPipelineId;
  artist_id: string;
  status: PipelineStatus;
  
  /** Recording session configuration */
  recording_session?: RecordingSession;
  
  /** Audio processing pipeline */
  audio_processing?: AudioProcessing;
  
  /** Model training configuration */
  model_training?: ModelTraining;
  
  /** Validation and evaluation */
  validation?: ValidationConfig;
  
  /** Model optimization */
  model_optimization?: ModelOptimization;
  
  /** Version control */
  versioning?: ModelVersioning;
}

// ============================================================================
// AGENTIC VOICE TYPES
// ============================================================================

/**
 * Agent ID pattern: agent_[16 alphanumeric]
 */
export type AgentId = `agent_${string}`;

/**
 * Agent type categories
 */
export type AgentType = 
  | 'conversational'
  | 'narrator'
  | 'assistant'
  | 'character'
  | 'interviewer'
  | 'educator'
  | 'entertainer'
  | 'custom';

/**
 * LLM provider types for agents
 */
export type AgentLlmProvider = 
  | 'anthropic'
  | 'openai'
  | 'google'
  | 'mistral'
  | 'cohere'
  | 'custom';

/**
 * Few-shot example
 */
export interface FewShotExample {
  user: string;
  assistant: string;
}

/**
 * LLM backbone configuration
 */
export interface AgentLlmBackbone {
  provider?: AgentLlmProvider;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  system_prompt?: string;
  few_shot_examples?: FewShotExample[];
}

/**
 * STT provider types
 */
export type SttProvider = 
  | 'whisper'
  | 'deepgram'
  | 'assembly'
  | 'google'
  | 'azure'
  | 'aws'
  | 'custom';

/**
 * Endpointing configuration
 */
export interface EndpointingConfig {
  silence_threshold_ms?: number;
  max_speech_duration_seconds?: number;
}

/**
 * Speech-to-text configuration
 */
export interface SpeechToTextConfig {
  provider?: SttProvider;
  model?: string;
  language?: string;
  real_time?: boolean;
  endpointing?: EndpointingConfig;
  diarization?: boolean;
}

/**
 * Text-to-speech configuration for agents
 */
export interface AgentTtsConfig {
  persona_id?: string;
  streaming?: boolean;
  chunk_size_ms?: number;
  buffer_ms?: number;
}

/**
 * Turn-taking model types
 */
export type TurnTakingModel = 'silence_based' | 'semantic' | 'predictive' | 'hybrid';

/**
 * Turn-taking configuration
 */
export interface TurnTakingConfig {
  model?: TurnTakingModel;
  barge_in_enabled?: boolean;
  barge_in_sensitivity?: number;
  backchanneling?: boolean;
  filler_words?: boolean;
}

/**
 * Voice interaction configuration
 */
export interface VoiceInteraction {
  speech_to_text?: SpeechToTextConfig;
  text_to_speech?: AgentTtsConfig;
  turn_taking?: TurnTakingConfig;
}

/**
 * Context window configuration
 */
export interface ContextWindowConfig {
  max_turns?: number;
  summarization_enabled?: boolean;
  summarization_threshold?: number;
}

/**
 * Memory configuration
 */
export interface AgentMemoryConfig {
  short_term?: boolean;
  long_term?: boolean;
  episodic?: boolean;
  semantic?: boolean;
  user_preferences?: boolean;
  cross_session?: boolean;
}

/**
 * Topic tracking configuration
 */
export interface TopicTrackingConfig {
  enabled?: boolean;
  max_concurrent_topics?: number;
  topic_shift_detection?: boolean;
}

/**
 * Conversation management configuration
 */
export interface ConversationManagement {
  context_window?: ContextWindowConfig;
  memory?: AgentMemoryConfig;
  topic_tracking?: TopicTrackingConfig;
}

/**
 * Function definition for agents
 */
export interface AgentFunction {
  name: string;
  description?: string;
  parameters?: Record<string, unknown>;
  requires_confirmation?: boolean;
}

/**
 * API authentication types
 */
export type ApiAuthType = 'api_key' | 'oauth2' | 'none';

/**
 * External API configuration
 */
export interface ExternalApiConfig {
  name: string;
  endpoint?: string;
  auth_type?: ApiAuthType;
}

/**
 * MCP transport types
 */
export type McpTransport = 'stdio' | 'http' | 'websocket';

/**
 * MCP server configuration
 */
export interface McpServerConfig {
  name: string;
  transport?: McpTransport;
  command?: string;
}

/**
 * MCP integration configuration
 */
export interface McpIntegration {
  enabled?: boolean;
  servers?: McpServerConfig[];
}

/**
 * Function calling configuration
 */
export interface FunctionCallingConfig {
  enabled?: boolean;
  available_functions?: AgentFunction[];
  external_apis?: ExternalApiConfig[];
  mcp_integration?: McpIntegration;
}

/**
 * Big Five personality traits
 */
export interface BigFiveTraits {
  openness?: number;
  conscientiousness?: number;
  extraversion?: number;
  agreeableness?: number;
  neuroticism?: number;
}

/**
 * Communication style configuration
 */
export interface CommunicationStyle {
  formality?: number;
  verbosity?: number;
  humor?: number;
  empathy?: number;
  directness?: number;
}

/**
 * Agent personality configuration
 */
export interface AgentPersonality {
  traits?: BigFiveTraits;
  communication_style?: CommunicationStyle;
  backstory?: string;
  knowledge_domains?: string[];
  quirks?: string[];
  catchphrases?: string[];
}

/**
 * Sensitive topics handling modes
 */
export type SensitiveTopicsHandling = 'deflect' | 'acknowledge' | 'refer' | 'discuss_carefully';

/**
 * Content policy configuration
 */
export interface ContentPolicy {
  prohibited_topics?: string[];
  sensitive_topics_handling?: SensitiveTopicsHandling;
  profanity_filter?: boolean;
  pii_detection?: boolean;
}

/**
 * AI nature acknowledgment modes
 */
export type AiNatureAcknowledgment = 'always' | 'when_asked' | 'never';

/**
 * Behavioral limits configuration
 */
export interface BehavioralLimits {
  max_response_length?: number;
  stay_in_character?: boolean;
  acknowledge_ai_nature?: AiNatureAcknowledgment;
  refuse_roleplay_as_real_people?: boolean;
}

/**
 * Safety configuration
 */
export interface SafetyConfig {
  crisis_detection?: boolean;
  crisis_response?: string;
  escalation_webhook?: string;
}

/**
 * Agent guardrails configuration
 */
export interface AgentGuardrails {
  content_policy?: ContentPolicy;
  behavioral_limits?: BehavioralLimits;
  safety?: SafetyConfig;
}

/**
 * Agent analytics configuration
 */
export interface AgentAnalytics {
  conversation_logging?: boolean;
  sentiment_tracking?: boolean;
  engagement_metrics?: boolean;
  error_tracking?: boolean;
  a_b_testing?: boolean;
}

/**
 * Deployment channel types
 */
export type DeploymentChannel = 
  | 'web'
  | 'mobile_app'
  | 'phone'
  | 'smart_speaker'
  | 'vr_ar'
  | 'game'
  | 'kiosk'
  | 'robot';

/**
 * Agent deployment configuration
 */
export interface AgentDeployment {
  channels?: DeploymentChannel[];
  latency_target_ms?: number;
  concurrent_sessions?: number;
  session_timeout_minutes?: number;
}

/**
 * Complete Agentic Voice configuration
 */
export interface AgenticVoice {
  agent_id: AgentId;
  name: string;
  persona_id?: string;
  agent_type: AgentType;
  
  /** LLM backbone configuration */
  llm_backbone?: AgentLlmBackbone;
  
  /** Voice interaction settings */
  voice_interaction?: VoiceInteraction;
  
  /** Conversation management */
  conversation_management?: ConversationManagement;
  
  /** Function calling and tools */
  function_calling?: FunctionCallingConfig;
  
  /** Agent personality */
  personality?: AgentPersonality;
  
  /** Safety guardrails */
  guardrails?: AgentGuardrails;
  
  /** Analytics configuration */
  analytics?: AgentAnalytics;
  
  /** Deployment settings */
  deployment?: AgentDeployment;
}

// ============================================================================
// MULTIMODAL SYNC TYPES
// ============================================================================

/** Multimodal sync ID format: sync_[16 alphanumeric] */
export type SyncId = `sync_${string}`;

/** Lip reading model options */
export type LipReadingModel = 'av_hubert' | 'lipreading_tcn' | 'visual_speech' | 'custom';

/** Face animation method options */
export type FaceAnimationMethod = 'audio2face' | 'wav2lip' | 'sadtalker' | 'genehead' | 'custom';

/** Animation output format */
export type AnimationOutputFormat = 'blendshapes' | 'mesh_vertices' | 'video' | 'arkit_params';

/** Blendshape set options */
export type BlendshapeSet = 'arkit_52' | 'facs' | 'oculus' | 'custom';

/** Viseme set options */
export type VisemeSet = 'ipa' | 'arpabet' | 'oculus_15' | 'apple_animoji' | 'custom';

/** Head motion method */
export type HeadMotionMethod = 'audio_driven' | 'rule_based' | 'neural' | 'hybrid';

/** Body gesture method */
export type BodyGestureMethod = 'audio2gesture' | 'rule_based' | 'diffusion' | 'custom';

/** Face detection model */
export type FaceDetectionModel = 'mediapipe' | 'dlib' | 'insightface' | 'custom';

/** Face selection strategy */
export type FaceSelection = 'largest' | 'center' | 'manual' | 'all';

/** Talking head animation method */
export type TalkingHeadMethod = 'sadtalker' | 'wav2lip' | 'makeittalk' | 'audio2head' | 'liveportrait' | 'custom';

/** Upscale model options */
export type UpscaleModel = 'realesrgan' | 'gfpgan' | 'codeformer' | 'custom';

/** Avatar format options */
export type AvatarFormat = 'ready_player_me' | 'vrm' | 'metahuman' | 'daz3d' | 'mixamo' | 'custom';

/** Avatar source type */
export type AvatarSourceType = 'url' | 'file' | 'platform_id' | 'generated';

/** Bone mapping strategy */
export type BoneMapping = 'auto' | 'humanoid' | 'custom';

/** Rendering engine */
export type RenderingEngine = 'unity' | 'unreal' | 'threejs' | 'babylonjs' | 'custom';

/** Quality preset */
export type RenderQualityPreset = 'low' | 'medium' | 'high' | 'ultra' | 'mobile';

/** Streaming protocol */
export type StreamingProtocol = 'webrtc' | 'hls' | 'dash' | 'rtmp';

/** Streaming latency mode */
export type StreamingLatencyMode = 'ultra_low' | 'low' | 'normal';

/** Sync strategy */
export type SyncStrategy = 'audio_master' | 'video_master' | 'adaptive';

/** Drift correction method */
export type DriftCorrectionMethod = 'time_stretch' | 'frame_drop' | 'interpolation';

/** Video generation model */
export type VideoGenerationModel = 'stable_video_diffusion' | 'pika' | 'runway_gen3' | 'sora' | 'custom';

/** Video resolution */
export type VideoResolution = '480p' | '720p' | '1080p' | '4k';

/** Aspect ratio */
export type AspectRatio = '16:9' | '9:16' | '1:1' | '4:3' | '21:9';

/** Motion capture input source */
export type MocapInputSource = 'webcam' | 'depth_camera' | 'suit' | 'gloves' | 'file';

/** Motion capture output format */
export type MocapFormat = 'fbx' | 'bvh' | 'json' | 'c3d';

/** Interpolation method */
export type InterpolationMethod = 'linear' | 'ease_in' | 'ease_out' | 'ease_in_out';

/** Video codec */
export type VideoCodec = 'h264' | 'h265' | 'vp9' | 'av1' | 'prores';

/** Video container */
export type VideoContainer = 'mp4' | 'webm' | 'mov' | 'mkv';

/** Animation export format */
export type AnimationExportFormat = 'json' | 'fbx' | 'gltf' | 'usd' | 'binary';

/** Streaming output format */
export type StreamingOutputFormat = 'websocket' | 'webrtc' | 'grpc' | 'sse';

/** Memory optimization level */
export type MemoryOptimization = 'none' | 'gradient_checkpointing' | 'model_offload' | 'aggressive';

/** Lip reading configuration */
export interface LipReading {
  enabled?: boolean;
  model?: LipReadingModel;
  confidence_threshold?: number;
  language?: string;
  fallback_to_audio?: boolean;
}

/** Timing extraction configuration */
export interface TimingExtraction {
  word_boundaries?: boolean;
  phoneme_boundaries?: boolean;
  pause_detection?: boolean;
  emotion_from_facial?: boolean;
  speaker_diarization?: boolean;
}

/** Dubbing mode configuration */
export interface DubbingMode {
  enabled?: boolean;
  preserve_original_timing?: boolean;
  lip_sync_optimization?: boolean;
  time_stretch_limit_percent?: number;
  target_language?: string;
  translation_model?: string;
}

/** Video to voice configuration */
export interface VideoToVoice {
  enabled?: boolean;
  lip_reading?: LipReading;
  timing_extraction?: TimingExtraction;
  dubbing_mode?: DubbingMode;
}

/** Face animation configuration */
export interface FaceAnimation {
  method?: FaceAnimationMethod;
  output_format?: AnimationOutputFormat;
  blendshape_set?: BlendshapeSet;
  fps?: number;
  smoothing?: number;
}

/** Lip sync configuration */
export interface LipSync {
  viseme_generation?: boolean;
  viseme_set?: VisemeSet;
  coarticulation?: boolean;
  jaw_movement?: boolean;
  tongue_approximation?: boolean;
  teeth_visibility?: boolean;
}

/** Facial expression configuration */
export interface FacialExpression {
  emotion_driven?: boolean;
  prosody_driven?: boolean;
  blink_generation?: boolean;
  blink_rate_per_minute?: number;
  eyebrow_movement?: boolean;
  eye_gaze?: boolean;
  micro_expressions?: boolean;
  wrinkle_maps?: boolean;
}

/** Head motion configuration */
export interface HeadMotion {
  enabled?: boolean;
  method?: HeadMotionMethod;
  nod_on_emphasis?: boolean;
  natural_sway?: boolean;
  look_at_camera?: boolean;
  motion_amplitude?: number;
}

/** Body gesture configuration */
export interface BodyGesture {
  enabled?: boolean;
  method?: BodyGestureMethod;
  gesture_library?: string;
  beat_gesture_detection?: boolean;
  hand_gestures?: boolean;
  upper_body_only?: boolean;
}

/** Voice to animation configuration */
export interface VoiceToAnimation {
  enabled?: boolean;
  face_animation?: FaceAnimation;
  lip_sync?: LipSync;
  facial_expression?: FacialExpression;
  head_motion?: HeadMotion;
  body_gesture?: BodyGesture;
}

/** Face detection configuration */
export interface FaceDetection {
  model?: FaceDetectionModel;
  multi_face_support?: boolean;
  face_selection?: FaceSelection;
}

/** Output resolution configuration */
export interface OutputResolution {
  width?: number;
  height?: number;
  upscaling?: boolean;
  upscale_factor?: number;
  upscale_model?: UpscaleModel;
}

/** Background handling configuration */
export interface BackgroundHandling {
  preserve_background?: boolean;
  background_motion?: boolean;
  background_replacement?: boolean;
  background_blur?: boolean;
  green_screen_output?: boolean;
}

/** Quality settings for image to talking head */
export interface TalkingHeadQualitySettings {
  temporal_consistency?: boolean;
  identity_preservation_strength?: number;
  expression_intensity?: number;
  motion_smoothness?: number;
}

/** Image to talking head configuration */
export interface ImageToTalkingHead {
  enabled?: boolean;
  face_detection?: FaceDetection;
  animation_method?: TalkingHeadMethod;
  output_resolution?: OutputResolution;
  background_handling?: BackgroundHandling;
  quality_settings?: TalkingHeadQualitySettings;
}

/** Avatar source configuration */
export interface AvatarSource {
  type?: AvatarSourceType;
  value?: string;
  platform?: string;
}

/** Retargeting configuration */
export interface Retargeting {
  enabled?: boolean;
  source_rig?: string;
  target_rig?: string;
  bone_mapping?: BoneMapping;
}

/** Rendering configuration */
export interface AvatarRendering {
  engine?: RenderingEngine;
  quality_preset?: RenderQualityPreset;
  real_time?: boolean;
  anti_aliasing?: boolean;
}

/** Avatar streaming configuration */
export interface AvatarStreaming {
  enabled?: boolean;
  protocol?: StreamingProtocol;
  latency_mode?: StreamingLatencyMode;
}

/** Avatar integration configuration */
export interface AvatarIntegration {
  enabled?: boolean;
  avatar_format?: AvatarFormat;
  avatar_source?: AvatarSource;
  retargeting?: Retargeting;
  rendering?: AvatarRendering;
  streaming?: AvatarStreaming;
}

/** Drift correction configuration */
export interface DriftCorrection {
  enabled?: boolean;
  max_correction_ms?: number;
  correction_method?: DriftCorrectionMethod;
}

/** Real-time sync configuration */
export interface RealTimeSync {
  enabled?: boolean;
  target_latency_ms?: number;
  buffer_size_ms?: number;
  sync_strategy?: SyncStrategy;
  drift_correction?: DriftCorrection;
  lip_sync_offset_ms?: number;
}

/** Video conditioning configuration */
export interface VideoConditioning {
  voice_conditioning?: boolean;
  text_prompt?: string;
  image_prompt?: string;
  style_reference?: string;
}

/** Video output settings */
export interface VideoOutputSettings {
  duration_seconds?: number;
  fps?: number;
  resolution?: VideoResolution;
  aspect_ratio?: AspectRatio;
}

/** Character consistency configuration */
export interface CharacterConsistency {
  enabled?: boolean;
  reference_images?: string[];
  identity_strength?: number;
}

/** Video generation configuration */
export interface VideoGeneration {
  enabled?: boolean;
  model?: VideoGenerationModel;
  conditioning?: VideoConditioning;
  output_settings?: VideoOutputSettings;
  character_consistency?: CharacterConsistency;
}

/** Motion capture tracking configuration */
export interface MocapTracking {
  face?: boolean;
  body?: boolean;
  hands?: boolean;
  eye_tracking?: boolean;
}

/** Motion capture processing configuration */
export interface MocapProcessing {
  noise_reduction?: boolean;
  jitter_filter?: boolean;
  bone_constraints?: boolean;
  foot_ik?: boolean;
}

/** Motion capture recording configuration */
export interface MocapRecording {
  enabled?: boolean;
  format?: MocapFormat;
  frame_rate?: number;
}

/** Motion capture configuration */
export interface MotionCapture {
  enabled?: boolean;
  input_source?: MocapInputSource;
  tracking?: MocapTracking;
  processing?: MocapProcessing;
  recording?: MocapRecording;
}

/** Audio analysis configuration */
export interface AudioAnalysis {
  amplitude?: boolean;
  frequency_bands?: number;
  beat_detection?: boolean;
  onset_detection?: boolean;
  pitch_tracking?: boolean;
}

/** Visual mapping configuration */
export interface VisualMapping {
  scale?: boolean;
  color?: boolean;
  position?: boolean;
  rotation?: boolean;
  particle_emission?: boolean;
}

/** Audio reactive smoothing configuration */
export interface AudioReactiveSmoothing {
  attack_ms?: number;
  release_ms?: number;
  interpolation?: InterpolationMethod;
}

/** Audio reactive configuration */
export interface AudioReactive {
  enabled?: boolean;
  analysis?: AudioAnalysis;
  visual_mapping?: VisualMapping;
  smoothing?: AudioReactiveSmoothing;
}

/** Video output format configuration */
export interface VideoOutputFormat {
  codec?: VideoCodec;
  container?: VideoContainer;
  bitrate_mbps?: number;
  variable_bitrate?: boolean;
}

/** Animation output format configuration */
export interface AnimationOutputConfig {
  format?: AnimationExportFormat;
  include_audio?: boolean;
  bake_animations?: boolean;
}

/** Streaming output format configuration */
export interface StreamingOutputConfig {
  format?: StreamingOutputFormat;
  chunk_duration_ms?: number;
}

/** Output formats configuration */
export interface OutputFormats {
  video?: VideoOutputFormat;
  animation?: AnimationOutputConfig;
  streaming?: StreamingOutputConfig;
}

/** Performance configuration */
export interface MultimodalPerformance {
  gpu_acceleration?: boolean;
  multi_gpu?: boolean;
  precision?: ModelPrecision;
  batch_processing?: boolean;
  cache_models?: boolean;
  memory_optimization?: MemoryOptimization;
}

/** Multimodal sync metadata */
export interface MultimodalSyncMetadata {
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  tags?: string[];
  notes?: string;
}

/** Complete multimodal sync configuration */
export interface MultimodalSync {
  sync_id: SyncId;
  version: string;
  
  /** Video to voice configuration */
  video_to_voice?: VideoToVoice;
  
  /** Voice to animation configuration */
  voice_to_animation?: VoiceToAnimation;
  
  /** Image to talking head configuration */
  image_to_talking_head?: ImageToTalkingHead;
  
  /** Avatar integration configuration */
  avatar_integration?: AvatarIntegration;
  
  /** Real-time sync settings */
  real_time_sync?: RealTimeSync;
  
  /** AI video generation */
  video_generation?: VideoGeneration;
  
  /** Motion capture configuration */
  motion_capture?: MotionCapture;
  
  /** Audio reactive effects */
  audio_reactive?: AudioReactive;
  
  /** Output formats */
  output_formats?: OutputFormats;
  
  /** Performance settings */
  performance?: MultimodalPerformance;
  
  /** Metadata */
  metadata?: MultimodalSyncMetadata;
}

// ============================================================================
// SUPERSONIC PIPELINE TYPES
// ============================================================================

/** Supersonic pipeline ID format: sonic_[16 alphanumeric] */
export type SupersonicPipelineId = `sonic_${string}`;

/** Pipeline tier options */
export type PipelineTier = 'tier_1_premium' | 'tier_2_balanced' | 'tier_3_edge';

/** Model license types */
export type ModelLicense = 'MIT' | 'Apache-2.0' | 'CC-BY-NC-4.0' | 'CC-BY-4.0' | 'GPL-3.0' | 'BSD-3-Clause' | 'other';

/** Pipeline environment */
export type PipelineEnvironment = 'development' | 'staging' | 'production';

/** Log level options */
export type LogLevel = 'debug' | 'info' | 'warning' | 'error';

/** Quantization precision options */
export type QuantizationPrecision = 'fp32' | 'fp16' | 'bf16' | 'int8' | 'int4';

/** Tier stack configuration */
export interface TierStack {
  tts_primary?: string;
  tts_fallback?: string;
  voice_cloning?: string;
  lip_sync_video?: string;
  lip_sync_image?: string;
  emotion_text?: string;
  emotion_audio?: string;
  asr?: string;
  vocoder?: string;
  llm?: string;
  embeddings?: string;
  vector_db?: string;
}

/** Recommended stack configuration */
export interface RecommendedStack {
  tier_1_premium?: TierStack;
  tier_2_balanced?: TierStack;
  tier_3_edge?: TierStack;
}

/** Pipeline stage configuration */
export interface PipelineStage {
  stage: string;
  description?: string;
  models: string[];
  latency_target_ms?: number;
  gpu_required?: boolean;
  can_stream?: boolean;
  parallelizable?: boolean;
  skip_conditions?: string[];
}

/** Model latency benchmarks */
export interface LatencyBenchmark {
  gpu_a100?: number;
  gpu_4090?: number;
  gpu_3090?: number;
  cpu_only?: number;
}

/** Model registry entry */
export interface ModelRegistryEntry {
  name?: string;
  version?: string;
  repo?: string;
  license?: ModelLicense;
  commercial_use?: boolean;
  model_size_gb?: number;
  vram_required_gb?: number;
  quantization_options?: string[];
  supported_languages?: string[];
  latency_benchmark_ms?: LatencyBenchmark;
}

/** Model registry (dictionary of models) */
export interface ModelRegistry {
  [modelKey: string]: ModelRegistryEntry;
}

/** Performance benchmarks */
export interface PerformanceBenchmarks {
  rtf_target?: number;
  first_byte_ms?: number;
  quality_mos_target?: number;
  speaker_similarity_target?: number;
  word_error_rate_target?: number;
  gpu_utilization_target?: number;
  throughput_chars_per_second?: number;
}

/** Infrastructure cost breakdown */
export interface InfrastructureCost {
  cloud_gpu_cost?: number;
  storage_cost?: number;
  bandwidth_cost?: number;
  total?: number;
}

/** Cost comparison data */
export interface CostComparison {
  elevenlabs_equivalent_cost_per_1m_chars?: number;
  playht_equivalent_cost_per_1m_chars?: number;
  noizyvox_oss_cost_per_1m_chars?: number;
  savings_percent?: number;
  break_even_volume_chars?: number;
  infrastructure_monthly_cost?: InfrastructureCost;
}

/** Hardware requirements for a tier */
export interface TierHardwareRequirements {
  gpu?: string;
  vram_min_gb?: number;
  ram_min_gb?: number;
  storage_min_gb?: number;
  cpu_cores_min?: number;
}

/** Hardware requirements by tier */
export interface HardwareRequirements {
  tier_1_premium?: TierHardwareRequirements;
  tier_2_balanced?: TierHardwareRequirements;
  tier_3_edge?: TierHardwareRequirements;
}

/** Batching configuration */
export interface BatchingConfig {
  enabled?: boolean;
  max_batch_size?: number;
  max_wait_ms?: number;
}

/** Caching configuration */
export interface CachingConfig {
  enabled?: boolean;
  cache_embeddings?: boolean;
  cache_ssml?: boolean;
  cache_audio_segments?: boolean;
  ttl_seconds?: number;
}

/** Quantization configuration */
export interface QuantizationConfig {
  enabled?: boolean;
  precision?: QuantizationPrecision;
  dynamic_quantization?: boolean;
}

/** Streaming configuration */
export interface PipelineStreamingConfig {
  enabled?: boolean;
  chunk_size_tokens?: number;
  overlap_tokens?: number;
}

/** Model loading configuration */
export interface ModelLoadingConfig {
  preload_all?: boolean;
  lazy_load?: boolean;
  unload_idle_seconds?: number;
  model_parallelism?: boolean;
}

/** Optimization settings */
export interface OptimizationSettings {
  batching?: BatchingConfig;
  caching?: CachingConfig;
  quantization?: QuantizationConfig;
  streaming?: PipelineStreamingConfig;
  model_loading?: ModelLoadingConfig;
}

/** Fallback chain entry */
export interface FallbackChainEntry {
  component?: string;
  primary?: string;
  fallbacks?: string[];
  failover_conditions?: string[];
}

/** Quality gates configuration */
export interface QualityGates {
  mos_minimum?: number;
  speaker_similarity_minimum?: number;
  intelligibility_minimum?: number;
  emotion_accuracy_minimum?: number;
  retry_on_failure?: boolean;
  max_retries?: number;
  fallback_on_quality_fail?: boolean;
}

/** Alerting configuration */
export interface AlertingConfig {
  enabled?: boolean;
  latency_threshold_ms?: number;
  error_rate_threshold?: number;
  quality_drop_threshold?: number;
}

/** Monitoring configuration */
export interface PipelineMonitoring {
  enabled?: boolean;
  metrics_endpoint?: string;
  log_level?: LogLevel;
  trace_requests?: boolean;
  sample_rate?: number;
  alerting?: AlertingConfig;
}

/** Pipeline metadata */
export interface PipelineMetadata {
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  environment?: PipelineEnvironment;
  tags?: string[];
}

/** Complete supersonic pipeline configuration */
export interface SupersonicPipeline {
  pipeline_id: SupersonicPipelineId;
  version: string;
  name?: string;
  description?: string;
  
  /** Recommended model stacks by tier */
  recommended_stack?: RecommendedStack;
  
  /** Currently active tier */
  active_tier?: PipelineTier;
  
  /** Ordered pipeline stages */
  pipeline_stages?: PipelineStage[];
  
  /** Model registry with details */
  model_registry?: ModelRegistry;
  
  /** Performance benchmarks */
  performance_benchmarks?: PerformanceBenchmarks;
  
  /** Cost comparison vs commercial */
  cost_comparison?: CostComparison;
  
  /** Hardware requirements by tier */
  hardware_requirements?: HardwareRequirements;
  
  /** Optimization settings */
  optimization_settings?: OptimizationSettings;
  
  /** Fallback chain for components */
  fallback_chain?: FallbackChainEntry[];
  
  /** Quality gates */
  quality_gates?: QualityGates;
  
  /** Monitoring configuration */
  monitoring?: PipelineMonitoring;
  
  /** Metadata */
  metadata?: PipelineMetadata;
}

// ============================================================================
// OPEN SOURCE INTEGRATIONS TYPES
// ============================================================================

/** Open source integration ID format: oss_[16 alphanumeric] */
export type OssIntegrationId = `oss_${string}`;

/** Device options */
export type DeviceType = 'cuda' | 'cpu' | 'mps' | 'auto';

/** ASR model sizes */
export type WhisperModelSize = 'tiny' | 'base' | 'small' | 'medium' | 'large' | 'large-v2' | 'large-v3' | 'turbo';

/** LLM quantization options */
export type LlmQuantization = 'none' | 'int8' | 'int4' | 'gptq' | 'awq';

/** LLM backend options */
export type LlmBackendType = 'transformers' | 'vllm' | 'llama.cpp' | 'exllama';

/** Preprocess options for SadTalker */
export type SadTalkerPreprocess = 'crop' | 'resize' | 'full';

/** Enhancer options */
export type FaceEnhancer = 'gfpgan' | 'restoreformer' | 'none';

/** Recognizer options for Rhubarb */
export type RhubarbRecognizer = 'pocketSphinx' | 'phonetic';

/** Output format for Rhubarb */
export type RhubarbOutputFormat = 'json' | 'tsv' | 'xml' | 'dat';

/** Emotion granularity */
export type EmotionGranularity = 'utterance' | 'frame';

/** Vector distance metric */
export type VectorDistance = 'cosine' | 'euclid' | 'dot';

/** UTMOS domain */
export type UtmosDomain = 'synth' | 'natural' | 'bvcc';

/** Base model configuration */
export interface BaseModelConfig {
  enabled?: boolean;
  version?: string;
  repo?: string;
  license?: string;
  commercial_use?: boolean;
  model_path?: string;
}

/** Fish Speech configuration */
export interface FishSpeechConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    num_codebooks?: number;
    streaming_enabled?: boolean;
    chunk_length_ms?: number;
    zero_shot_enabled?: boolean;
    reference_audio_min_seconds?: number;
    reference_audio_max_seconds?: number;
    supported_languages?: string[];
  };
  quantization?: {
    enabled?: boolean;
    precision?: 'fp32' | 'fp16' | 'int8';
  };
}

/** XTTS-v2 configuration */
export interface XttsConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    gpt_cond_len?: number;
    gpt_cond_chunk_len?: number;
    streaming_enabled?: boolean;
    stream_chunk_size?: number;
    supported_languages?: string[];
  };
}

/** F5-TTS configuration */
export interface F5TtsConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    nfe_step?: number;
    cfg_strength?: number;
    sway_sampling_coef?: number;
    speed?: number;
  };
}

/** CosyVoice configuration */
export interface CosyVoiceConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    instruct_mode?: boolean;
    cross_lingual?: boolean;
    streaming_enabled?: boolean;
  };
}

/** Kokoro TTS configuration */
export interface KokoroConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    cpu_optimized?: boolean;
    model_size_mb?: number;
    rtf_cpu?: number;
  };
}

/** Piper TTS configuration */
export interface PiperConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    noise_scale?: number;
    length_scale?: number;
    noise_w?: number;
    sentence_silence?: number;
  };
}

/** OpenVoice configuration */
export interface OpenVoiceConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    tone_color_conversion?: boolean;
    cross_lingual?: boolean;
    instant_cloning?: boolean;
  };
}

/** TTS models collection */
export interface TtsModels {
  fish_speech?: FishSpeechConfig;
  xtts_v2?: XttsConfig;
  f5_tts?: F5TtsConfig;
  cosyvoice?: CosyVoiceConfig;
  kokoro_tts?: KokoroConfig;
  piper?: PiperConfig;
  openvoice?: OpenVoiceConfig;
}

/** Whisper configuration */
export interface WhisperConfig extends BaseModelConfig {
  model_size?: WhisperModelSize;
  config?: {
    compute_type?: 'float32' | 'float16' | 'int8';
    beam_size?: number;
    word_timestamps?: boolean;
    vad_filter?: boolean;
    condition_on_previous_text?: boolean;
  };
}

/** Faster Whisper configuration */
export interface FasterWhisperConfig extends BaseModelConfig {
  config?: {
    device?: DeviceType;
    compute_type?: string;
    cpu_threads?: number;
    num_workers?: number;
    batched?: boolean;
    batch_size?: number;
  };
}

/** WhisperX configuration */
export interface WhisperXConfig extends BaseModelConfig {
  config?: {
    align_model?: boolean;
    diarize?: boolean;
    min_speakers?: number;
    max_speakers?: number;
  };
}

/** ASR models collection */
export interface AsrModels {
  whisper?: WhisperConfig;
  faster_whisper?: FasterWhisperConfig;
  whisperx?: WhisperXConfig;
}

/** BigVGAN configuration */
export interface BigVganConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    hop_size?: number;
    resblock?: string;
    upsample_rates?: number[];
  };
}

/** HiFi-GAN configuration */
export interface HifiGanConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    resblock_kernel_sizes?: number[];
  };
}

/** Vocos configuration */
export interface VocosConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    feature_extractor?: string;
    bandwidth?: number;
  };
}

/** Vocoder models collection */
export interface VocoderModels {
  bigvgan?: BigVganConfig;
  hifigan?: HifiGanConfig;
  vocos?: VocosConfig;
}

/** LatentSync configuration */
export interface LatentSyncConfig extends BaseModelConfig {
  config?: {
    fps?: number;
    face_detection?: string;
    audio_encoder?: string;
  };
}

/** Wav2Lip configuration */
export interface Wav2LipConfig extends BaseModelConfig {
  config?: {
    fps?: number;
    pads?: number[];
    face_det_batch_size?: number;
    wav2lip_batch_size?: number;
  };
}

/** SadTalker configuration */
export interface SadTalkerConfig extends BaseModelConfig {
  config?: {
    preprocess?: SadTalkerPreprocess;
    still?: boolean;
    enhancer?: FaceEnhancer;
  };
}

/** Hallo2 configuration */
export interface Hallo2Config extends BaseModelConfig {
  config?: {
    fps?: number;
    long_video_support?: boolean;
    max_video_length_seconds?: number;
  };
}

/** LivePortrait configuration */
export interface LivePortraitConfig extends BaseModelConfig {
  config?: {
    stitching?: boolean;
    relative_motion?: boolean;
    pasteback?: boolean;
  };
}

/** Rhubarb configuration */
export interface RhubarbConfig extends BaseModelConfig {
  config?: {
    recognizer?: RhubarbRecognizer;
    output_format?: RhubarbOutputFormat;
    extended_shapes?: boolean;
  };
}

/** Lip sync models collection */
export interface LipSyncModels {
  latentsync?: LatentSyncConfig;
  wav2lip?: Wav2LipConfig;
  sadtalker?: SadTalkerConfig;
  hallo2?: Hallo2Config;
  liveportrait?: LivePortraitConfig;
  rhubarb?: RhubarbConfig;
}

/** Emotion2Vec configuration */
export interface Emotion2VecConfig extends BaseModelConfig {
  config?: {
    granularity?: EmotionGranularity;
    num_emotions?: number;
  };
}

/** GoEmotions configuration */
export interface GoEmotionsConfig extends BaseModelConfig {
  config?: {
    num_labels?: number;
    threshold?: number;
    multilabel?: boolean;
  };
}

/** SpeechBrain emotion configuration */
export interface SpeechBrainEmotionConfig extends BaseModelConfig {
  config?: {
    model_hub?: string;
    sample_rate?: number;
  };
}

/** Emotion models collection */
export interface EmotionModels {
  emotion2vec?: Emotion2VecConfig;
  go_emotions?: GoEmotionsConfig;
  speechbrain_emotion?: SpeechBrainEmotionConfig;
}

/** BGE-M3 configuration */
export interface BgeM3Config extends BaseModelConfig {
  config?: {
    max_length?: number;
    embedding_dim?: number;
    pooling_method?: string;
  };
}

/** ECAPA-TDNN configuration */
export interface EcapaTdnnConfig extends BaseModelConfig {
  config?: {
    embedding_dim?: number;
    sample_rate?: number;
  };
}

/** Resemblyzer configuration */
export interface ResemblyzerConfig extends BaseModelConfig {
  config?: {
    embedding_dim?: number;
    sample_rate?: number;
  };
}

/** Embedding models collection */
export interface EmbeddingModels {
  bge_m3?: BgeM3Config;
  ecapa_tdnn?: EcapaTdnnConfig;
  resemblyzer?: ResemblyzerConfig;
}

/** LLaMA configuration */
export interface LlamaConfig extends BaseModelConfig {
  config?: {
    model_size?: string;
    context_length?: number;
    quantization?: LlmQuantization;
    backend?: LlmBackendType;
  };
}

/** Qwen configuration */
export interface QwenConfig extends BaseModelConfig {
  config?: {
    model_size?: string;
    context_length?: number;
    quantization?: string;
    backend?: string;
  };
}

/** Gemma configuration */
export interface GemmaConfig extends BaseModelConfig {
  config?: {
    model_size?: string;
    context_length?: number;
    quantization?: string;
    backend?: string;
  };
}

/** LLM models collection */
export interface LlmModels {
  llama?: LlamaConfig;
  qwen?: QwenConfig;
  gemma?: GemmaConfig;
}

/** DeepFilterNet configuration */
export interface DeepFilterNetConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    atten_lim_db?: number;
    post_filter?: boolean;
  };
}

/** Resemble Enhance configuration */
export interface ResembleEnhanceConfig extends BaseModelConfig {
  config?: {
    denoise?: boolean;
    enhance?: boolean;
    sample_rate?: number;
  };
}

/** Audio enhancement models */
export interface AudioEnhancementModels {
  deepfilternet?: DeepFilterNetConfig;
  resemble_enhance?: ResembleEnhanceConfig;
}

/** UTMOS configuration */
export interface UtmosConfig extends BaseModelConfig {
  config?: {
    domain?: UtmosDomain;
  };
}

/** DNSMOS configuration */
export interface DnsmosConfig extends BaseModelConfig {
  config?: {
    sample_rate?: number;
    personalized?: boolean;
  };
}

/** Quality assessment models */
export interface QualityAssessmentModels {
  utmos?: UtmosConfig;
  dnsmos?: DnsmosConfig;
}

/** Qdrant configuration */
export interface QdrantConfig {
  enabled?: boolean;
  version?: string;
  license?: string;
  commercial_use?: boolean;
  config?: {
    host?: string;
    port?: number;
    grpc_port?: number;
    collection_config?: {
      distance?: VectorDistance;
      on_disk?: boolean;
    };
  };
}

/** ChromaDB configuration */
export interface ChromaDbConfig {
  enabled?: boolean;
  version?: string;
  license?: string;
  commercial_use?: boolean;
  config?: {
    persist_directory?: string;
    anonymized_telemetry?: boolean;
  };
}

/** SQLite-VSS configuration */
export interface SqliteVssConfig {
  enabled?: boolean;
  version?: string;
  license?: string;
  commercial_use?: boolean;
  config?: {
    db_path?: string;
    dimensions?: number;
  };
}

/** Vector databases collection */
export interface VectorDatabases {
  qdrant?: QdrantConfig;
  chromadb?: ChromaDbConfig;
  sqlite_vss?: SqliteVssConfig;
}

/** AudioSeal configuration */
export interface AudioSealConfig extends BaseModelConfig {
  config?: {
    nbits?: number;
    sample_rate?: number;
  };
}

/** Watermarking models */
export interface WatermarkingModels {
  audioseal?: AudioSealConfig;
}

/** HuggingFace Hub configuration */
export interface HuggingFaceHubConfig {
  token?: string;
  offline_mode?: boolean;
  cache_dir?: string;
}

/** Logging configuration */
export interface LoggingConfig {
  level?: 'debug' | 'info' | 'warning' | 'error';
  format?: string;
}

/** Runtime configuration */
export interface OssRuntimeConfig {
  device?: DeviceType;
  gpu_memory_fraction?: number;
  model_cache_dir?: string;
  huggingface_hub?: HuggingFaceHubConfig;
  logging?: LoggingConfig;
}

/** OSS integration metadata */
export interface OssMetadata {
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  tags?: string[];
}

/** Complete open source integrations configuration */
export interface OpenSourceIntegrations {
  integration_id: OssIntegrationId;
  version: string;
  name?: string;
  
  /** TTS model configurations */
  tts_models?: TtsModels;
  
  /** ASR model configurations */
  asr_models?: AsrModels;
  
  /** Vocoder model configurations */
  vocoder_models?: VocoderModels;
  
  /** Lip sync model configurations */
  lip_sync_models?: LipSyncModels;
  
  /** Emotion model configurations */
  emotion_models?: EmotionModels;
  
  /** Embedding model configurations */
  embedding_models?: EmbeddingModels;
  
  /** LLM model configurations */
  llm_models?: LlmModels;
  
  /** Audio enhancement configurations */
  audio_enhancement?: AudioEnhancementModels;
  
  /** Quality assessment configurations */
  quality_assessment?: QualityAssessmentModels;
  
  /** Vector database configurations */
  vector_databases?: VectorDatabases;
  
  /** Watermarking configurations */
  watermarking?: WatermarkingModels;
  
  /** Runtime configuration */
  runtime_config?: OssRuntimeConfig;
  
  /** Metadata */
  metadata?: OssMetadata;
}

// ============================================================================
// OPENAI VOICE COMPLETE TYPES
// ============================================================================

/** Speed control settings for TTS */
export interface TtsSpeedControl {
  min: number;
  max: number;
  default: number;
}

/** Instruction capabilities for gpt-4o-mini-tts */
export interface InstructionCapabilities {
  emotion_control?: boolean;
  speaking_style?: boolean;
  character_voice?: boolean;
  pacing_control?: boolean;
  emphasis_control?: boolean;
  accent_hints?: boolean;
}

/** Text-to-Speech model configuration */
export interface OpenAiTtsModel {
  model_id: string;
  generation?: string;
  description?: string;
  quality_tier?: 'standard' | 'high-definition' | 'premium';
  latency?: string;
  sample_rate_hz?: number;
  pricing_per_1m_chars_usd?: number;
  voices?: string[];
  output_formats?: string[];
  max_input_chars?: number;
  streaming?: boolean;
  speed_control?: TtsSpeedControl;
  instruction_guided?: boolean;
  instruction_capabilities?: InstructionCapabilities;
  instruction_examples?: string[];
  best_for?: string[];
  limitations?: string[];
  noizyvox_recommendation?: string;
}

/** ASR model features */
export interface AsrFeatures {
  transcription?: boolean;
  translation_to_english?: boolean;
  word_timestamps?: boolean;
  segment_timestamps?: boolean;
  language_detection?: boolean;
  prompt_conditioning?: boolean;
  streaming?: boolean;
  improved_accent_handling?: boolean;
  better_noise_robustness?: boolean;
}

/** Speech-to-Text model configuration */
export interface OpenAiAsrModel {
  model_id: string;
  generation?: string;
  description?: string;
  languages_supported?: number;
  pricing_per_minute_usd?: number;
  max_file_size_mb?: number;
  supported_formats?: string[];
  output_formats?: string[];
  features?: AsrFeatures;
  word_error_rate?: string;
  best_for?: string[];
  noizyvox_recommendation?: string;
}

/** Realtime model pricing */
export interface RealtimePricing {
  audio_input_per_minute_usd?: number;
  audio_output_per_minute_usd?: number;
  text_input_per_1m_tokens_usd?: number;
  text_output_per_1m_tokens_usd?: number;
  cached_text_input_per_1m_tokens_usd?: number;
}

/** Realtime audio formats */
export interface RealtimeAudioFormats {
  input?: string[];
  output?: string[];
}

/** Realtime model features */
export interface RealtimeFeatures {
  native_audio_understanding?: boolean;
  bidirectional_streaming?: boolean;
  function_calling?: boolean;
  tool_use?: boolean;
  multi_turn_conversation?: boolean;
  emotion_preservation?: boolean;
  natural_interruption?: boolean;
  server_side_vad?: boolean;
  input_transcription?: boolean;
  output_transcription?: boolean;
  lower_latency?: boolean;
}

/** Realtime Speech model configuration */
export interface OpenAiRealtimeModel {
  model_id: string;
  generation?: string;
  description?: string;
  type?: string;
  latency?: string;
  pricing?: RealtimePricing;
  voices?: string[];
  exclusive_voices?: string[];
  audio_formats?: RealtimeAudioFormats;
  features?: RealtimeFeatures;
  context_window_tokens?: number;
  max_output_tokens?: number;
  best_for?: string[];
  noizyvox_recommendation?: string;
}

/** Audio Preview model capabilities */
export interface AudioPreviewCapabilities {
  audio_input?: boolean;
  audio_output?: boolean;
  text_input?: boolean;
  text_output?: boolean;
  image_input?: boolean;
  function_calling?: boolean;
}

/** Audio Preview model pricing */
export interface AudioPreviewPricing {
  audio_input_per_1m_tokens_usd?: number;
  audio_output_per_1m_tokens_usd?: number;
  text_input_per_1m_tokens_usd?: number;
  text_output_per_1m_tokens_usd?: number;
}

/** Audio Preview model configuration */
export interface OpenAiAudioPreviewModel {
  model_id: string;
  description?: string;
  capabilities?: AudioPreviewCapabilities;
  pricing?: AudioPreviewPricing;
  use_cases?: string[];
}

/** OpenAI Audio Model Family */
export interface OpenAiAudioModelFamily {
  text_to_speech_models?: OpenAiTtsModel[];
  speech_to_text_models?: OpenAiAsrModel[];
  realtime_speech_models?: OpenAiRealtimeModel[];
  audio_preview_models?: OpenAiAudioPreviewModel[];
}

/** Voice cloning capabilities */
export interface VoiceCloningCapabilities {
  min_audio_sample_seconds?: number;
  quality?: string;
  languages?: string;
  emotion_transfer?: boolean;
  speaker_verification?: boolean;
}

/** Voice Engine Preview capabilities */
export interface VoiceEngineCapabilities {
  voice_cloning?: VoiceCloningCapabilities;
  safety_measures?: string[];
}

/** Voice Engine Preview configuration */
export interface VoiceEnginePreview {
  status?: string;
  capabilities?: VoiceEngineCapabilities;
  access_requirements?: string[];
  noizyvox_recommendation?: string;
}

/** Standard voice characteristics */
export interface VoiceCharacteristic {
  voice_id: string;
  gender?: string;
  age_range?: string;
  character_traits?: string[];
  tonal_qualities?: string[];
  pitch_range?: string;
  speaking_rate?: string;
  best_content_types?: string[];
  emotion_range?: string;
  availability?: string[];
  noizyvox_recommendation?: string;
  premium?: boolean;
}

/** Voice Characteristics configuration */
export interface VoiceCharacteristics {
  standard_voices?: VoiceCharacteristic[];
  extended_voices?: VoiceCharacteristic[];
  exclusive_realtime_voices?: VoiceCharacteristic[];
}

/** Emotion control configuration */
export interface EmotionControl {
  supported_emotions?: string[];
  instruction_patterns?: string[];
}

/** Speaking style control */
export interface SpeakingStyleControl {
  supported_styles?: string[];
  instruction_patterns?: string[];
}

/** Pacing control */
export interface PacingControl {
  options?: string[];
  instruction_patterns?: string[];
}

/** Character voice control */
export interface CharacterVoiceControl {
  instruction_patterns?: string[];
  example_characters?: string[];
}

/** Instruction-guided synthesis capabilities */
export interface InstructionGuidedCapabilities {
  emotion_control?: EmotionControl;
  speaking_style_control?: SpeakingStyleControl;
  pacing_control?: PacingControl;
  character_voice?: CharacterVoiceControl;
}

/** Persona mapping example */
export interface PersonaMappingExample {
  persona_id?: string;
  display_name?: string;
  archetype_tags?: string[];
  generated_instruction?: string;
}

/** NOIZYVOX persona mapping */
export interface NoizyvoxPersonaMapping {
  instruction_template?: string;
  example_mapping?: PersonaMappingExample;
}

/** Instruction-guided synthesis configuration */
export interface InstructionGuidedSynthesis {
  capabilities?: InstructionGuidedCapabilities;
  noizyvox_persona_mapping?: NoizyvoxPersonaMapping;
}

/** REST endpoint configuration */
export interface RestEndpoint {
  endpoint?: string;
  method?: string;
  content_type?: string;
  response_type?: string;
  description?: string;
  request_schema?: Record<string, string>;
}

/** REST endpoints */
export interface RestEndpoints {
  text_to_speech?: RestEndpoint;
  transcription?: RestEndpoint;
  translation?: RestEndpoint;
}

/** WebSocket endpoint configuration */
export interface WebSocketEndpoint {
  endpoint?: string;
  query_params?: Record<string, string>;
  headers?: Record<string, string>;
  protocol?: string;
  audio_format?: string;
}

/** WebSocket endpoints */
export interface WebSocketEndpoints {
  realtime_api?: WebSocketEndpoint;
}

/** WebRTC endpoint configuration */
export interface WebRtcEndpoint {
  endpoint?: string;
  description?: string;
  response?: string;
}

/** WebRTC endpoints */
export interface WebRtcEndpoints {
  session_creation?: WebRtcEndpoint;
}

/** API Architecture */
export interface ApiArchitecture {
  rest_endpoints?: RestEndpoints;
  websocket_endpoints?: WebSocketEndpoints;
  webrtc_endpoints?: WebRtcEndpoints;
}

/** SDK audio support */
export interface SdkAudioSupport {
  tts?: boolean;
  transcription?: boolean;
  translation?: boolean;
  streaming?: boolean;
}

/** Official SDK configuration */
export interface OfficialSdk {
  name?: string;
  package?: string;
  installation?: string;
  github?: string;
  documentation?: string;
  audio_support?: SdkAudioSupport;
  features?: string[];
}

/** Azure OpenAI SDK */
export interface AzureOpenAiSdk {
  name?: string;
  languages?: string[];
  github?: string;
  documentation?: string;
  features?: string[];
}

/** SDK Ecosystem */
export interface SdkEcosystem {
  official_sdks?: OfficialSdk[];
  azure_openai_sdk?: AzureOpenAiSdk;
}

/** Whisper fine-tuning configuration */
export interface WhisperFineTuning {
  availability?: string;
  use_cases?: string[];
  process?: string[];
  noizyvox_recommendation?: string;
}

/** Text model fine-tuning configuration */
export interface TextModelFineTuning {
  available_models?: string[];
  api_endpoint?: string;
  data_format?: string;
  use_cases_for_voice?: string[];
  noizyvox_recommendation?: string;
}

/** Fine-tuning capabilities */
export interface FineTuningCapabilities {
  whisper_fine_tuning?: WhisperFineTuning;
  text_model_fine_tuning?: TextModelFineTuning;
}

/** TTS pricing entry */
export interface TtsPricingEntry {
  per_1m_characters?: number;
  per_1k_characters?: number;
  streaming?: string;
  instructions?: string;
}

/** ASR pricing entry */
export interface AsrPricingEntry {
  per_minute?: number;
  per_hour?: number;
}

/** Realtime API pricing entry */
export interface RealtimeApiPricingEntry {
  audio_input_per_minute?: number;
  audio_output_per_minute?: number;
  text_input_per_1m_tokens?: number;
  text_output_per_1m_tokens?: number;
  cached_input_per_1m_tokens?: number;
}

/** Audio in Chat pricing entry */
export interface AudioInChatPricingEntry {
  audio_input_per_1m_tokens?: number;
  audio_output_per_1m_tokens?: number;
}

/** Complete pricing information */
export interface PricingComplete {
  text_to_speech?: Record<string, TtsPricingEntry>;
  speech_to_text?: Record<string, AsrPricingEntry>;
  realtime_api?: Record<string, RealtimeApiPricingEntry>;
  audio_in_chat?: Record<string, AudioInChatPricingEntry>;
}

/** Tier recommendation */
export interface TierRecommendation {
  tts_model?: string;
  tts_rationale?: string;
  asr_model?: string;
  asr_rationale?: string;
  realtime_model?: string;
  realtime_rationale?: string;
  estimated_cost_per_1m_chars?: number;
  fallback_to_oss?: boolean;
}

/** Persona pack strategy */
export interface PersonaPackStrategy {
  primary_tts?: string;
  voice_selection?: string[];
  instruction_usage?: string;
  hybrid_approach?: string;
}

/** Agentic voice strategy */
export interface AgenticVoiceStrategy {
  primary_model?: string;
  fallback_model?: string;
  function_calling?: boolean;
  vad_mode?: string;
}

/** NOIZYVOX Recommendations */
export interface NoizyvoxRecommendations {
  tier_1_premium_production?: TierRecommendation;
  tier_2_balanced?: TierRecommendation;
  tier_3_high_volume?: TierRecommendation;
  persona_pack_strategy?: PersonaPackStrategy;
  agentic_voice_strategy?: AgenticVoiceStrategy;
}

/** Implementation examples */
export interface ImplementationExamples {
  python_tts_streaming?: string;
  python_realtime_agent?: string;
  javascript_webrtc?: string;
  persona_instruction_generator?: string;
}

/** OpenAI Voice Complete metadata */
export interface OpenAiVoiceCompleteMetadata {
  created_at?: string;
  updated_at?: string;
  created_by?: string;
  openai_api_version?: string;
  tags?: string[];
}

/** OpenAI Voice Complete - Complete OpenAI voice technology documentation */
export interface OpenAiVoiceComplete {
  $schema?: string;
  
  /** Unique identifier (pattern: oai_[16 chars]) */
  integration_id: `oai_${string}`;
  
  /** Configuration version */
  version: string;
  
  /** Integration name */
  name?: string;
  
  /** OpenAI audio model family */
  openai_audio_model_family?: OpenAiAudioModelFamily;
  
  /** Voice Engine preview (limited access) */
  voice_engine_preview?: VoiceEnginePreview;
  
  /** Voice characteristics */
  voice_characteristics?: VoiceCharacteristics;
  
  /** Instruction-guided synthesis */
  instruction_guided_synthesis?: InstructionGuidedSynthesis;
  
  /** API architecture */
  api_architecture?: ApiArchitecture;
  
  /** SDK ecosystem */
  sdk_ecosystem?: SdkEcosystem;
  
  /** Fine-tuning capabilities */
  fine_tuning_capabilities?: FineTuningCapabilities;
  
  /** Complete pricing information */
  pricing_complete?: PricingComplete;
  
  /** NOIZYVOX recommendations */
  noizyvox_recommendations?: NoizyvoxRecommendations;
  
  /** Implementation examples */
  implementation_examples?: ImplementationExamples;
  
  /** Metadata */
  metadata?: OpenAiVoiceCompleteMetadata;
}
