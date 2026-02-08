#!/bin/bash
# Generate Lotte image using Wan 2.6 image-edit
# Usage: ./generate.sh "prompt text" [size] [seed]

set -e

# Configuration
API_KEY="${ATLAS_API_KEY:-$1}"
if [ -z "$API_KEY" ]; then
    echo "Error: ATLAS_API_KEY not set"
    echo "Usage: ATLAS_API_KEY=apikey-xxxxx ./generate.sh 'prompt text'"
    exit 1
fi

PROMPT="${1:-Lotte, 22 year old, wavy shoulder-length blonde hair, bright blue eyes, tanned golden skin}"
SIZE="${2:-960*1280}"  # 3:4 aspect ratio default
SEED="${3:--1}"

LOTTE_REFERENCE="https://drive.google.com/uc?export=download&id=1muNlst-7Vo9pwma2qCnif4nC5ZhiDi0S"

echo "🎨 Generating Lotte image with Wan 2.6..."
echo "Prompt: ${PROMPT:0:80}..."
echo "Size: $SIZE"

# Make API call
RESPONSE=$(curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
    \"model\": \"alibaba/wan-2.6/image-edit\",
    \"prompt\": \"$PROMPT\",
    \"images\": [\"$LOTTE_REFERENCE\"],
    \"size\": \"$SIZE\",
    \"seed\": $SEED
  }")

# Extract prediction ID
PREDICTION_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

if [ -z "$PREDICTION_ID" ]; then
    echo "❌ Failed to start generation"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi

echo ""
echo "✅ Generation started!"
echo "Prediction ID: $PREDICTION_ID"
echo ""
echo "⏳ Polling for result..."

# Poll for result
for i in {1..20}; do
    sleep 5
    
    RESULT=$(curl -s "https://api.atlascloud.ai/api/v1/model/prediction/$PREDICTION_ID" \
      -H "Authorization: Bearer $API_KEY")
    
    STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['status'])")
    
    echo "  Attempt $i/20: $STATUS"
    
    if [ "$STATUS" = "completed" ]; then
        IMAGE_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(d['outputs'][0] if d.get('outputs') else 'None')")
        echo ""
        echo "✅ Generation complete!"
        echo "Image URL: $IMAGE_URL"
        
        # Save to file
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        OUTPUT_FILE="lotte-wan26_$TIMESTAMP.json"
        echo "$RESULT" | python3 -m json.tool > "$OUTPUT_FILE"
        echo "Response saved to: $OUTPUT_FILE"
        exit 0
    fi
    
    if [ "$STATUS" = "failed" ]; then
        ERROR=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'].get('error','Unknown error'))")
        echo ""
        echo "❌ Generation failed: $ERROR"
        exit 1
    fi
done

echo ""
echo "⏱️ Timeout - check manually:"
echo "curl -s \"https://api.atlascloud.ai/api/v1/model/prediction/$PREDICTION_ID\" -H \"Authorization: Bearer $API_KEY\""
