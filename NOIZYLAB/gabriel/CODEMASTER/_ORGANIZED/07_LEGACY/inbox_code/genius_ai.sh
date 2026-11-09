#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
#  🧠 GENIUS AI MODULE - Mail Manager Pro v3.5.0
#  Advanced Machine Learning & Intelligence Features
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

readonly AI_CACHE_DIR="${SCRIPT_DIR:-$(dirname "$0")/..}/cache/ai"
readonly AI_MODELS_DIR="${SCRIPT_DIR:-$(dirname "$0")/..}/models"
readonly AI_TRAINING_DIR="${SCRIPT_DIR:-$(dirname "$0")/..}/data/training"

# Initialize AI directories
mkdir -p "$AI_CACHE_DIR" "$AI_MODELS_DIR" "$AI_TRAINING_DIR" 2>/dev/null || true

#───────────────────────────────────────────────────────────────────────────────
# SENTIMENT ANALYSIS
#───────────────────────────────────────────────────────────────────────────────
ai_sentiment_analyze() {
    local text="$1"
    
    local positive_words="great|excellent|thanks|appreciate|happy|love|wonderful|fantastic|amazing|pleased|good|best|perfect"
    local negative_words="urgent|angry|frustrated|disappointed|terrible|worst|hate|awful|bad|problem|issue|fail|wrong|sorry"
    local neutral_words="please|regards|hello|hi|sincerely|attached|following|update|information"
    
    local positive_count=$(echo "$text" | grep -oiE "$positive_words" | wc -l | tr -d ' ')
    local negative_count=$(echo "$text" | grep -oiE "$negative_words" | wc -l | tr -d ' ')
    
    local sentiment="neutral"
    local confidence=50
    
    if ((positive_count > negative_count)); then
        sentiment="positive"
        confidence=$((60 + positive_count * 5))
    elif ((negative_count > positive_count)); then
        sentiment="negative"
        confidence=$((60 + negative_count * 5))
    fi
    
    ((confidence > 100)) && confidence=100
    
    echo "{\"sentiment\":\"$sentiment\",\"confidence\":$confidence,\"positive\":$positive_count,\"negative\":$negative_count}"
}

#───────────────────────────────────────────────────────────────────────────────
# SPAM DETECTION
#───────────────────────────────────────────────────────────────────────────────
ai_spam_score() {
    local subject="$1"
    local sender="${2:-}"
    local body="${3:-}"
    local full_text="$subject $body"
    
    local score=0
    
    # Spam trigger words (+10 each)
    local spam_words="free|winner|lottery|click here|unsubscribe|limited time|act now|exclusive deal|congratulations|claim|prize"
    local spam_count=$(echo "$full_text" | grep -oiE "$spam_words" | wc -l | tr -d ' ')
    score=$((score + spam_count * 10))
    
    # ALL CAPS detection (+15)
    local caps_ratio=$(echo "$subject" | grep -o '[A-Z]' | wc -l | tr -d ' ')
    local total_chars=${#subject}
    if ((total_chars > 0 && caps_ratio * 100 / total_chars > 50)); then
        score=$((score + 15))
    fi
    
    # Exclamation marks (+5 each, max 20)
    local exclaim_count=$(echo "$subject" | grep -o '!' | wc -l | tr -d ' ')
    ((exclaim_count > 4)) && exclaim_count=4
    score=$((score + exclaim_count * 5))
    
    # Money symbols (+10)
    if echo "$full_text" | grep -qE '\$[0-9]+|€|£'; then
        score=$((score + 10))
    fi
    
    # Suspicious sender domains (+20)
    local suspicious_domains="@.*\.(xyz|top|click|win|free|promo)"
    if echo "$sender" | grep -qiE "$suspicious_domains"; then
        score=$((score + 20))
    fi
    
    # Cap at 100
    ((score > 100)) && score=100
    
    local classification="ham"
    ((score >= 70)) && classification="spam"
    ((score >= 40 && score < 70)) && classification="suspicious"
    
    echo "{\"score\":$score,\"classification\":\"$classification\"}"
}

#───────────────────────────────────────────────────────────────────────────────
# SMART THREADING (Conversation Detection)
#───────────────────────────────────────────────────────────────────────────────
ai_detect_thread() {
    local subject="$1"
    local message_id="${2:-}"
    
    local is_reply="false"
    local thread_id=""
    local thread_position=0
    
    # Check for reply prefixes
    if echo "$subject" | grep -qiE "^(Re:|Fw:|Fwd:|Re\[.*\]:)"; then
        is_reply="true"
        thread_position=1
        
        # Count reply depth
        local reply_count=$(echo "$subject" | grep -oiE "Re:" | wc -l | tr -d ' ')
        thread_position=$reply_count
    fi
    
    # Generate thread ID from cleaned subject
    local clean_subject=$(echo "$subject" | sed -E 's/^(Re:|Fw:|Fwd:|Re\[.*\]:)+//gi' | xargs)
    thread_id=$(echo -n "$clean_subject" | shasum -a 256 | cut -c1-16)
    
    echo "{\"is_reply\":$is_reply,\"thread_id\":\"$thread_id\",\"position\":$thread_position,\"clean_subject\":\"$clean_subject\"}"
}

#───────────────────────────────────────────────────────────────────────────────
# AUTO-RESPONSE SUGGESTION
#───────────────────────────────────────────────────────────────────────────────
ai_suggest_response() {
    local email_text="$1"
    local response_type="${2:-professional}"
    
    local suggestion=""
    
    # Meeting request
    if echo "$email_text" | grep -qiE "meeting|schedule|call|calendar|available"; then
        case "$response_type" in
            professional)
                suggestion="Thank you for reaching out. I am available on [DATE/TIME]. Please let me know if this works for you."
                ;;
            casual)
                suggestion="Sure! I can do [DATE/TIME]. Let me know!"
                ;;
            decline)
                suggestion="Thank you for the invitation. Unfortunately, I am not available at that time. Could we reschedule?"
                ;;
        esac
    # Question
    elif echo "$email_text" | grep -qiE "\?|question|wondering|could you|can you"; then
        suggestion="Thank you for your question. [YOUR ANSWER HERE]. Please let me know if you need any clarification."
    # Thank you email
    elif echo "$email_text" | grep -qiE "thank you|thanks|appreciate"; then
        suggestion="You're welcome! Happy to help. Let me know if there's anything else I can assist with."
    # Information request
    elif echo "$email_text" | grep -qiE "information|details|send me|provide|attached"; then
        suggestion="Please find the requested information attached/below. Let me know if you need anything else."
    else
        suggestion="Thank you for your email. I will review and get back to you shortly."
    fi
    
    echo "$suggestion"
}

#───────────────────────────────────────────────────────────────────────────────
# EMAIL SUMMARIZATION
#───────────────────────────────────────────────────────────────────────────────
ai_summarize_email() {
    local email_text="$1"
    local max_sentences="${2:-3}"
    
    # Extract key sentences (sentences with important keywords)
    local important_patterns="deadline|action|required|please|important|urgent|meeting|confirm|attached|decision|approve"
    
    # Split into sentences and filter
    local summary=""
    local sentence_count=0
    
    while IFS= read -r sentence; do
        if ((sentence_count >= max_sentences)); then
            break
        fi
        
        if echo "$sentence" | grep -qiE "$important_patterns"; then
            if [[ -n "$summary" ]]; then
                summary="$summary "
            fi
            summary="$summary$(echo "$sentence" | xargs)"
            ((sentence_count++))
        fi
    done < <(echo "$email_text" | sed 's/\. /\.\n/g')
    
    # If no important sentences found, take first sentences
    if [[ -z "$summary" ]]; then
        summary=$(echo "$email_text" | sed 's/\. /\.\n/g' | head -n "$max_sentences" | tr '\n' ' ')
    fi
    
    echo "$summary"
}

#───────────────────────────────────────────────────────────────────────────────
# CONTACT EXTRACTION
#───────────────────────────────────────────────────────────────────────────────
ai_extract_contacts() {
    local email_text="$1"
    
    # Extract email addresses
    local emails=$(echo "$email_text" | grep -oiE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | sort -u)
    
    # Extract phone numbers
    local phones=$(echo "$email_text" | grep -oE '(\+?[0-9]{1,3}[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}' | sort -u)
    
    # Extract URLs
    local urls=$(echo "$email_text" | grep -oE 'https?://[a-zA-Z0-9./?=_%&-]+' | sort -u)
    
    echo "{"
    echo "  \"emails\": [$(echo "$emails" | while read -r e; do echo -n "\"$e\","; done | sed 's/,$//')],"
    echo "  \"phones\": [$(echo "$phones" | while read -r p; do echo -n "\"$p\","; done | sed 's/,$//')],"
    echo "  \"urls\": [$(echo "$urls" | while read -r u; do echo -n "\"$u\","; done | sed 's/,$//')] "
    echo "}"
}

#───────────────────────────────────────────────────────────────────────────────
# DATE/TIME EXTRACTION
#───────────────────────────────────────────────────────────────────────────────
ai_extract_dates() {
    local email_text="$1"
    
    # Common date patterns
    local dates=$(echo "$email_text" | grep -oE '(January|February|March|April|May|June|July|August|September|October|November|December)[[:space:]]+[0-9]{1,2}(,?[[:space:]]+[0-9]{4})?' | head -5)
    local numeric_dates=$(echo "$email_text" | grep -oE '[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}' | head -5)
    local iso_dates=$(echo "$email_text" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -5)
    
    # Time patterns
    local times=$(echo "$email_text" | grep -oiE '[0-9]{1,2}:[0-9]{2}[[:space:]]*(am|pm|AM|PM)?' | head -5)
    
    # Relative dates
    local relative=""
    if echo "$email_text" | grep -qiE "tomorrow"; then
        relative="tomorrow"
    elif echo "$email_text" | grep -qiE "next week"; then
        relative="next week"
    elif echo "$email_text" | grep -qiE "today"; then
        relative="today"
    fi
    
    echo "{"
    echo "  \"dates\": [$(echo "$dates $numeric_dates $iso_dates" | tr ' ' '\n' | grep -v '^$' | while read -r d; do echo -n "\"$d\","; done | sed 's/,$//')],"
    echo "  \"times\": [$(echo "$times" | while read -r t; do echo -n "\"$t\","; done | sed 's/,$//')],"
    echo "  \"relative\": \"$relative\""
    echo "}"
}

#───────────────────────────────────────────────────────────────────────────────
# ACTION ITEM EXTRACTION
#───────────────────────────────────────────────────────────────────────────────
ai_extract_actions() {
    local email_text="$1"
    
    local actions=()
    
    # Patterns that indicate action items
    local action_patterns=(
        "please.*"
        "could you.*"
        "can you.*"
        "need you to.*"
        "action required.*"
        "must.*by"
        "deadline.*"
        "submit.*"
        "send.*"
        "review.*"
        "confirm.*"
        "approve.*"
    )
    
    for pattern in "${action_patterns[@]}"; do
        local found=$(echo "$email_text" | grep -oiE "$pattern[^.!?]*[.!?]" | head -3)
        if [[ -n "$found" ]]; then
            while IFS= read -r action; do
                actions+=("$action")
            done <<< "$found"
        fi
    done
    
    echo "["
    local first=true
    for action in "${actions[@]}"; do
        if [[ -n "$action" ]]; then
            if [[ "$first" == "true" ]]; then
                first=false
            else
                echo ","
            fi
            echo -n "  \"$(echo "$action" | tr '"' "'" | xargs)\""
        fi
    done
    echo ""
    echo "]"
}

#───────────────────────────────────────────────────────────────────────────────
# SMART LABEL SUGGESTIONS
#───────────────────────────────────────────────────────────────────────────────
ai_suggest_labels() {
    local subject="$1"
    local body="${2:-}"
    local sender="${3:-}"
    local full_text="$subject $body"
    
    local labels=()
    
    # Work related
    if echo "$full_text $sender" | grep -qiE "meeting|project|deadline|report|review|quarterly|budget|team|office"; then
        labels+=("work")
    fi
    
    # Finance
    if echo "$full_text $sender" | grep -qiE "invoice|payment|receipt|bank|statement|tax|expense|refund|billing"; then
        labels+=("finance")
    fi
    
    # Travel
    if echo "$full_text $sender" | grep -qiE "flight|hotel|booking|reservation|itinerary|travel|trip|airline|airport"; then
        labels+=("travel")
    fi
    
    # Shopping
    if echo "$full_text $sender" | grep -qiE "order|shipping|delivery|tracking|purchase|cart|amazon|ebay|shop"; then
        labels+=("shopping")
    fi
    
    # Social
    if echo "$sender" | grep -qiE "@(facebook|twitter|linkedin|instagram|tiktok|youtube)"; then
        labels+=("social")
    fi
    
    # Newsletter
    if echo "$full_text" | grep -qiE "newsletter|weekly digest|unsubscribe|subscription"; then
        labels+=("newsletter")
    fi
    
    # Urgent
    if echo "$full_text" | grep -qiE "urgent|asap|immediately|critical|emergency"; then
        labels+=("urgent")
    fi
    
    # Action required
    if echo "$full_text" | grep -qiE "action required|please respond|confirm|approve|review needed"; then
        labels+=("action-required")
    fi
    
    # Output as JSON array
    echo -n "["
    local first=true
    for label in "${labels[@]}"; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo -n ","
        fi
        echo -n "\"$label\""
    done
    echo "]"
}

#───────────────────────────────────────────────────────────────────────────────
# LEARNING & TRAINING
#───────────────────────────────────────────────────────────────────────────────
ai_learn_preference() {
    local action="$1"  # e.g., "moved_to_folder", "marked_important", "deleted"
    local email_data="$2"  # JSON with subject, sender, etc.
    
    local training_file="${AI_TRAINING_DIR}/preferences.jsonl"
    
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "{\"timestamp\":\"$timestamp\",\"action\":\"$action\",\"data\":$email_data}" >> "$training_file"
    
    echo "Preference learned: $action"
}

ai_get_statistics() {
    local training_file="${AI_TRAINING_DIR}/preferences.jsonl"
    
    if [[ ! -f "$training_file" ]]; then
        echo "{\"total_learned\":0,\"actions\":{}}"
        return
    fi
    
    local total=$(wc -l < "$training_file" | tr -d ' ')
    local actions=$(cat "$training_file" | jq -r '.action' 2>/dev/null | sort | uniq -c | awk '{print "\""$2"\":"$1}' | paste -sd, -)
    
    echo "{\"total_learned\":$total,\"actions\":{$actions}}"
}

#───────────────────────────────────────────────────────────────────────────────
# EXPORT
#───────────────────────────────────────────────────────────────────────────────
export -f ai_sentiment_analyze 2>/dev/null || true
export -f ai_spam_score 2>/dev/null || true
export -f ai_detect_thread 2>/dev/null || true
export -f ai_suggest_response 2>/dev/null || true
export -f ai_summarize_email 2>/dev/null || true
export -f ai_extract_contacts 2>/dev/null || true
export -f ai_extract_dates 2>/dev/null || true
export -f ai_extract_actions 2>/dev/null || true
export -f ai_suggest_labels 2>/dev/null || true
export -f ai_learn_preference 2>/dev/null || true
export -f ai_get_statistics 2>/dev/null || true

echo "🧠 Genius AI Module loaded" >&2
