# Lotte Wan 2.6 Image Generation

Generate Lotte images using Alibaba's Wan 2.6 image-edit model via AtlasCloud API. More permissive with explicit/suggestive content than Nano Banana Pro.

---

## Overview

**Model:** `alibaba/wan-2.6/image-edit`  
**Provider:** AtlasCloud (api.atlascloud.ai)  
**Type:** Image-to-Image editing with text prompts  
**Strengths:** Accepts explicit/sensual language without E005 safety blocks

**vs Nano Banana Pro:**
- ✅ More permissive with suggestive/explicit prompts
- ✅ No "flagged as sensitive" (E005) errors
- ✅ Handles JSON prompt structure well
- ❌ Requires input image (can't generate from scratch)
- ❌ Fixed aspect ratios only

---

## Setup

### 1. Get API Key

1. Sign up at https://atlascloud.ai
2. Add payment method
3. Generate API key from Console → API Keys
4. Store in environment: `export ATLAS_API_KEY="apikey-xxxxx"`

### 2. Lotte Reference Image

The model requires an input image to edit/transform. Uses Lotte's reference image:

```
https://drive.google.com/uc?export=download&id=1muNlst-7Vo9pwma2qCnif4nC5ZhiDi0S
```

---

## Usage

### Basic Generation

```bash
curl -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ATLAS_API_KEY" \
  -d '{
    "model": "alibaba/wan-2.6/image-edit",
    "prompt": "Lotte, 22 year old, wavy shoulder-length blonde hair, bright blue eyes...",
    "images": ["https://drive.google.com/uc?export=download&id=1muNlst-7Vo9pwma2qCnif4nC5ZhiDi0S"],
    "size": "960*1280",
    "seed": -1
  }'
```

### Using JSON Prompts

Convert JSON prompts from library to text:

```bash
./scripts/generate-from-json.sh prompts/highly-explicit/pov-under-table-kneeling.json
```

### Aspect Ratios

| Ratio | Size | Use Case |
|-------|------|----------|
| 3:4 | `960*1280` | Instagram portrait |
| 9:16 | `720*1280` | Stories/Reels/TikTok |
| 1:1 | `1024*1024` | Square posts |
| 2:3 | `800*1200` | Classic portrait |

**Full list:** 576*1344, 720*1280, 768*1024, 800*1200, 936*1664, 960*1280, 1024*1024, 1040*1560, 1104*1472, 1200*800, 1280*720, 1280*960, 1280*1280

---

## Lotte Character Profile

When converting JSON prompts for Wan 2.6, use these Lotte-specific traits:

```json
{
  "name": "Lotte",
  "age": "22",
  "hair": "wavy shoulder-length blonde",
  "eyes": "bright blue",
  "skin": "tanned golden",
  "body": "fit slim-thick",
  "reference_image": "https://drive.google.com/uc?export=download&id=1muNlst-7Vo9pwma2qCnif4nC5ZhiDi0S"
}
```

**Always include in prompts:**
- Wavy shoulder-length blonde hair (not straight/platinum)
- Bright blue eyes (not green)
- Tanned golden skin
- Fit slim-thick figure

---

## JSON to Text Conversion

The model accepts text prompts only. Convert JSON structure to descriptive text:

**Example conversion:**
```json
// JSON
{
  "subject": {
    "action": "kneeling under table",
    "outfit": {
      "top": {"type": "cropped tank", "fit": "tight, braless"}
    }
  }
}

// Text prompt
"Lotte kneeling under table, wearing cropped tank top, tight braless..."
```

**Keep explicit language:**
- ✅ "tight, braless" 
- ✅ "subtle nipple outline"
- ✅ "inner thighs framing face"
- ✅ "voyeuristic energy"
- ✅ "suggestive not explicit"

Wan 2.6 handles these without blocking.

---

## Response Handling

### Success Response

```json
{
  "code": 200,
  "data": {
    "id": "prediction-id",
    "status": "created",
    "outputs": null,
    "urls": {
      "get": "https://api.atlascloud.ai/api/v1/model/prediction/{id}"
    }
  }
}
```

### Poll for Result

```bash
curl -s "https://api.atlascloud.ai/api/v1/model/prediction/{id}" \
  -H "Authorization: Bearer $ATLAS_API_KEY"
```

### Completed Result

```json
{
  "code": 200,
  "data": {
    "status": "completed",
    "outputs": ["https://dashscope-result-sgp...image-url.png"],
    "has_nsfw_contents": null,
    "error": ""
  }
}
```

---

## Error Handling

### Invalid Size Format

**Error:** `Invalid size format: 720x1280, expected format: width*height`  
**Fix:** Use asterisk not x: `720*1280`

### Invalid Aspect Ratio

**Error:** Size not in enum list  
**Fix:** Use one of the preset sizes only (see table above)

### Service Unavailable

**Error:** Temporary outage  
**Fix:** Retry after 30-60 seconds

---

## Workflow

1. **Select prompt** from `/home/gavien/workspace/lotte/prompts/highly-explicit/`
2. **Convert JSON to text** using Lotte character adaptations
3. **Choose aspect ratio** (recommend 960*1280 for Instagram)
4. **Generate** via API call
5. **Poll** for completion (usually 30-60 seconds)
6. **Download** image from output URL
7. **Optional:** Upload to GitHub viewer

---

## Comparison: Wan 2.6 vs Nano Banana Pro

| Feature | Wan 2.6 | Nano Banana Pro |
|---------|---------|-----------------|
| Explicit content | ✅ Accepted | ❌ E005 blocked |
| Safety filters | Permissive | Strict |
| Input required | Image + text | Text + reference |
| Aspect ratios | Fixed presets | Flexible |
| Speed | ~30-60s | ~30-60s |
| Cost | Pay per use | Pay per use |
| Best for | Suggestive/explicit | Safe/sFW content |

---

## Files

- `SKILL.md` - This documentation
- `scripts/generate.sh` - Basic generation script
- `scripts/generate-from-json.sh` - Generate from JSON prompt
- `scripts/poll-result.sh` - Poll for generation result
- `examples/` - Example prompts and outputs

---

## Related

- Main Lotte workspace: `/home/gavien/workspace/lotte/`
- Prompt library: `/home/gavien/workspace/lotte/prompts/`
- GitHub viewer: `adamfiverr-lab/lotte-viewer`
- Nano Banana Pro skill: `lotte-ai-influencer`
