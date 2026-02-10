# Wan 2.6 Image Generation Guide

Complete guide for generating images with Wan 2.6 via AtlasCloud API.

## Table of Contents
- [Overview](#overview)
- [API Basics](#api-basics)
- [JSON Prompt Format](#json-prompt-format)
- [Realism Boilerplate](#realism-boilerplate)
- [Workflow](#workflow)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Wan 2.6** (Alibaba) is an image generation model accessible via AtlasCloud API. Key advantages:
- ✅ Accepts structured JSON prompts
- ✅ More permissive than Nano Banana Pro (no E005 blocks)
- ✅ Good character consistency with reference images
- ✅ Natural skin texture with proper prompting

**Comparison with Nano Banana Pro:**
| Feature | Wan 2.6 | Nano Banana Pro |
|---------|---------|-----------------|
| JSON prompts | ✅ Native support | ❌ Text only |
| Explicit content | ✅ Accepted | ❌ Blocked (E005) |
| Skin realism | Good with boilerplate | Built-in |
| Speed | Moderate | Fast |

---

## API Basics

### Endpoint
```
POST https://api.atlascloud.ai/api/v1/model/generateImage
```

### Authentication
```bash
Authorization: Bearer apikey-48f8bd48013b464da07b762b0a6e3511
```

### Headers
```bash
Content-Type: application/json
```

### Request Structure
```json
{
  "model": "alibaba/wan-2.6/image-edit",
  "prompt": "{...}",
  "images": ["https://reference-image-url.jpg"],
  "size": "960*1280",
  "seed": -1
}
```

### Valid Sizes (Aspect Ratios)
| Size | Ratio | Use Case |
|------|-------|----------|
| `960*1280` | 3:4 | Instagram portrait |
| `720*1280` | 9:16 | Instagram Stories |
| `1280*960` | 4:3 | Landscape |
| `1024*1024` | 1:1 | Square |

**Note:** Use asterisk format (`*`) not `x`.

---

## JSON Prompt Format

Wan 2.6 accepts **stringified JSON** as the prompt. This allows precise control over all elements.

### Basic Structure
```json
{
  "type": "img_prompt",
  "ref_lock": "strict",
  "character": {
    "name": "Lotte",
    "age": "22",
    "hair": "wavy shoulder-length blonde",
    "eyes": "bright blue",
    "skin": "tanned golden, real skin texture with visible pores, natural skin, not plastic",
    "body": "fit slim-thick"
  },
  "layout": {
    "style": "mirror selfie"
  },
  "subject": {
    "skin": "tanned golden, real skin texture with visible pores, natural skin, not plastic, slight sheen",
    "accessory": "black sunglasses on head"
  },
  "outfit": {
    "bikini": {
      "style": "triangle top + low-rise bottom",
      "pattern": "white with white floral print",
      "trim": "yellow edging and ties"
    },
    "footwear": "yellow open-toe sandals with ankle strap",
    "jewelry": "large gold hoop earrings"
  },
  "accessories": {
    "phone": "black iPhone 16 Max with matte black case, visible in frame",
    "sunglasses": "held near lips"
  },
  "pose": "deep squat with open legs, chin on fist, pout",
  "environment": {
    "room": "indoor dressing/bedroom",
    "background": "white louvered closet doors, NO mirrors in background",
    "floor": "beige carpet",
    "mirror": "single full-length mirror only, thin gold frame"
  },
  "lighting": "soft indoor, neutral-warm, minimal shadows",
  "camera": "iPhone 15 Pro Max, raw iphone realism",
  "quality": "ultra photorealistic 8k, real skin texture with visible pores, natural skin, not plastic, slight grain, photorealistic, sharp, natural colors",
  "constraints": {
    "no_face_or_body_change": true,
    "match_reference_exactly": true
  }
}
```

### Key Fields

#### `type`
Always `"img_prompt"` for image generation.

#### `ref_lock`
- `"strict"` - Strong adherence to reference image
- `"loose"` - More creative freedom

#### `character`
Define the subject's appearance. Include realism descriptors in `skin` field.

#### `layout`
Scene composition:
- `"mirror selfie"`
- `"portrait"`
- `"full body"`
- `"close up"`

#### `subject`
Specific subject details including skin texture descriptors.

#### `outfit`
Clothing details:
```json
"outfit": {
  "top": { "type": "sheer white tank top", "state": "soaked, transparent" },
  "bottom": { "type": "black lace thong", "state": "low-rise" }
}
```

#### `pose`
Body positioning. Be specific:
- `"deep squat with open legs, chin on fist, pout"`
- `"on knees, back deeply arched, looking over shoulder"`
- `"standing, hand on hip, slight smile"`

#### `environment`
Setting details:
```json
"environment": {
  "room": "luxury hotel bedroom",
  "background": "floor-to-ceiling windows with city lights",
  "floor": "white marble",
  "mirror": "single full-length mirror only"
}
```

**Important:** Include `"NO mirrors in background"` to avoid duplication issues.

#### `lighting`
- `"soft indoor, neutral-warm, minimal shadows"`
- `"dramatic backlight, silhouette with rim lighting"`
- `"golden hour, warm glow"`

#### `camera`
Camera style affects realism:
- `"iPhone 15 Pro Max, raw iphone realism"`
- `"Canon EOS R5, 85mm lens, f/1.8"`

#### `quality`
**Critical field** - include all realism descriptors here:
- `"ultra photorealistic 8k"`
- `"real skin texture with visible pores"`
- `"natural skin, not plastic"`
- `"slight grain"`
- `"photorealistic, sharp, natural colors"`

#### `constraints`
```json
"constraints": {
  "no_face_or_body_change": true,
  "match_reference_exactly": true,
  "suggestive_not_explicit": true
}
```

---

## Realism Boilerplate

For natural, non-plastic skin, repeat these phrases **3 times** across the JSON:

### Key Phrases
1. `"real skin texture with visible pores"`
2. `"natural skin, not plastic"`
3. `"slight sheen"` (for natural glow)
4. `"slight grain"` (in quality field)
5. `"raw iphone realism"`

### Placement Strategy
| Field | Content |
|-------|---------|
| `character.skin` | `"tanned golden, real skin texture with visible pores, natural skin, not plastic"` |
| `subject.skin` | `"tanned golden, real skin texture with visible pores, natural skin, not plastic, slight sheen"` |
| `quality` | `"ultra photorealistic 8k, real skin texture with visible pores, natural skin, not plastic, slight grain..."` |

**Note on Cloudinary:** Previously used for temporary preview hosting. Now using local-only workflow.

---

## Workflow

### Complete Pipeline

```
1. Generate (AtlasCloud/Wan 2.6)
   ↓
2. Download immediately (Aliyun OSS URL expires ~1 hour)
   ↓
3. Save to local workspace
   ↓
4. User reviews → Deploy if approved
```

### Step 1: Generate
```bash
curl -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer apikey-48f8bd48013b464da07b762b0a6e3511" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "alibaba/wan-2.6/image-edit",
    "prompt": "{...JSON prompt...}",
    "images": ["https://reference-image.jpg"],
    "size": "960*1280",
    "seed": -1
  }'
```

### Step 2: Poll for Result
```bash
curl "https://api.atlascloud.ai/api/v1/model/prediction/{prediction_id}" \
  -H "Authorization: Bearer apikey-48f8bd48013b464da07b762b0a6e3511"
```

### Step 3: Download
```bash
curl -sL -o image.png "https://dashscope-result-sgp.oss-ap-southeast-1.aliyuncs.com/..."
```

### Step 4: Save Locally
```bash
# Move to daily-output folder
mv image.png daily-output/
```

**Storage Strategy:** All images stored locally in workspace.

---

## Examples

### Example 1: Pool Scene
```json
{
  "type": "img_prompt",
  "ref_lock": "strict",
  "character": {
    "name": "Lotte",
    "age": "22",
    "hair": "wavy shoulder-length blonde",
    "eyes": "bright blue",
    "skin": "tanned golden, real skin texture with visible pores",
    "body": "fit slim-thick"
  },
  "layout": { "style": "full body" },
  "outfit": {
    "bikini": "white triangle bikini with yellow trim"
  },
  "pose": "standing at pool edge, one hand on hip, confident smile",
  "environment": {
    "setting": "luxury villa poolside",
    "time": "golden hour sunset",
    "lighting": "warm golden light, long shadows"
  },
  "quality": "ultra photorealistic 8k, real skin texture with visible pores..."
}
```

### Example 2: Mirror Selfie
```json
{
  "layout": { "style": "mirror selfie" },
  "outfit": {
    "top": "cropped white tank top",
    "bottom": "high-waisted denim shorts"
  },
  "pose": "standing, one leg crossed over other, holding phone",
  "environment": {
    "room": "bedroom",
    "background": "white closet doors, NO mirrors in background",
    "mirror": "single full-length mirror"
  }
}
```

### Example 3: Suggestive/Explicit (Within Bounds)
```json
{
  "subject": {
    "skin": "tanned golden, real skin texture, wet with water droplets",
    "expression": "seductive, lips parted, looking over shoulder"
  },
  "outfit": {
    "top": { "type": "sheer white tank top, soaked and transparent" },
    "bottom": { "type": "black lace thong, low-rise" }
  },
  "pose": "on knees on bed, back deeply arched, looking back at camera",
  "environment": {
    "room": "luxury hotel bedroom",
    "background": "floor-to-ceiling windows with city lights at night",
    "lighting": "dramatic backlight, silhouette with rim lighting"
  },
  "constraints": {
    "suggestive_not_explicit": true,
    "voyeuristic_energy": true
  }
}
```

---

## Troubleshooting

### Issue: "Invalid size format"
**Solution:** Use asterisk (`*`) not `x`:
- ✅ `960*1280`
- ❌ `960x1280`

### Issue: "403 Forbidden" on image URL
**Cause:** Aliyun OSS URLs expire quickly (~1 hour).
**Solution:** Download images immediately after generation and save locally.

### Issue: Skin looks plastic
**Solution:** Add realism boilerplate to 3 fields:
1. `character.skin`
2. `subject.skin`
3. `quality`

Repeat: `"real skin texture with visible pores, natural skin, not plastic"`

### Issue: Character doesn't match reference
**Solutions:**
- Set `ref_lock: "strict"`
- Set `constraints.match_reference_exactly: true`
- Ensure reference image URL is accessible

### Issue: Duplicate/mirrored subject
**Cause:** Mirrors in background reflecting the subject.
**Solution:** Add `"NO mirrors in background"` to environment.background.

### Issue: Generation fails/safety block
**Note:** Wan 2.6 is more permissive, but extreme content may still fail. Use `suggestive_not_explicit` framing.

---

## Quick Reference Card

### Minimal JSON Structure
```json
{
  "type": "img_prompt",
  "ref_lock": "strict",
  "character": { "name": "Lotte", "age": "22", "skin": "..." },
  "layout": { "style": "..." },
  "pose": "...",
  "environment": { "room": "..." },
  "quality": "ultra photorealistic 8k..."
}
```

### Essential Curl Commands
```bash
# Generate
curl -X POST "https://api.atlascloud.ai/api/v1/model/generateImage" \
  -H "Authorization: Bearer apikey-48f8bd48013b464da07b762b0a6e3511" \
  -H "Content-Type: application/json" \
  -d '{"model":"alibaba/wan-2.6/image-edit","prompt":"{...}","images":["..."],"size":"960*1280"}'

# Check status
curl "https://api.atlascloud.ai/api/v1/model/prediction/{id}" \
  -H "Authorization: Bearer apikey-48f8bd48013b464da07b762b0a6e3511"
```

### File Locations
- Templates: `/skills/lotte-wan26/templates/`
- Examples: `/skills/lotte-wan26/examples/`
- Scripts: `/skills/lotte-wan26/scripts/`
- This guide: `/docs/WAN2.6-GUIDE.md`

---

*Last updated: 2026-02-08*
*Wan 2.6 via AtlasCloud API*