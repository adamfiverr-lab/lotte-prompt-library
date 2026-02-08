# Manual Image Upload to Lotte Viewer

How to add generated images to the GitHub viewer outside of the daily cron job.

---

## Quick Steps

### 1. Generate Image

Use Replicate API with Nano Banana Pro:

```bash
export REPLICATE_API_TOKEN="$REPLICATE_API_TOKEN"  # Set via environment variable

curl -X POST \
  https://api.replicate.com/v1/models/google/nano-banana-pro/predictions \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Lotte, 22 year old young blonde woman with wavy shoulder-length hair, bright blue eyes, tanned golden skin...",
      "image_input": ["https://drive.google.com/uc?export=download&id=1muNlst-7Vo9pwma2qCnif4nC5ZhiDi0S"],
      "aspect_ratio": "4:5",
      "resolution": "2K",
      "safety_filter_level": "block_only_high"
    }
  }'
```

**Poll for result:**
```bash
curl -s -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  https://api.replicate.com/v1/predictions/<PREDICTION_ID>
```

### 2. Download Image

```bash
curl -sL -o images/lotte-<DATE>.jpg "<IMAGE_URL_FROM_REPLICATE>"
```

### 3. Update Viewer HTML

Edit `index.html` and add post to `const posts` array:

```javascript
const posts = [
{
    date: '2026-02-08',
    trend: 'Trend Name',
    image: 'https://raw.githubusercontent.com/adamfiverr-lab/lotte-viewer/main/images/lotte-<DATE>.jpg',
    filename: 'lotte-<DATE>.jpg',
    instagram: `Caption text here...`,
    fanvue: `Fanvue caption here...`,
},
// ... existing posts
];
```

**Notes:**
- Posts are sorted by date (newest first) automatically
- Image URL format: `https://raw.githubusercontent.com/adamfiverr-lab/lotte-viewer/main/images/<FILENAME>`
- Use template literals (backticks) for multi-line captions

### 4. Commit and Push

```bash
git add images/lotte-<DATE>.jpg index.html
git commit -m "Add <description> image"
git push origin main
```

**Wait 2-5 minutes** for GitHub Pages to deploy.

---

## File Locations

- **Images:** `/home/gavien/workspace/lotte/images/`
- **Viewer HTML:** `/home/gavien/workspace/lotte/index.html`
- **GitHub Repo:** `adamfiverr-lab/lotte-viewer`
- **Live URL:** https://adamfiverr-lab.github.io/lotte-viewer/

---

## Tips

### If Generation is Blocked (E005)

Add photography_rules to prompt:
```
...photorealistic, photography_rules: no_male_presence, suggestive_not_explicit, mirror_selfie, realism_very_high
```

### If Service Unavailable (E003)

Replicate is overloaded. Options:
- Wait 30-60 minutes and retry
- Queue via cron for tonight
- Try during off-peak hours

### Batch Upload Multiple Images

1. Generate all images first
2. Save all to images/ folder
3. Add all posts to index.html
4. Single commit/push for all

---

## Example: Complete Workflow

```bash
cd /home/gavien/workspace/lotte

# 1. Generate image
# (use curl command above, get image URL)

# 2. Download
curl -sL -o images/lotte-pool-scene.jpg "https://replicate.delivery/..."

# 3. Edit index.html - add post entry
# (use nano, vim, or edit tool)

# 4. Commit and push
git add images/lotte-pool-scene.jpg index.html
git commit -m "Add pool scene image"
git push origin main

# 5. Verify
# Check https://adamfiverr-lab.github.io/lotte-viewer/ in 2-5 minutes
```

---

## Troubleshooting

**Image not showing:**
- Check image URL is accessible: `curl -I <IMAGE_URL>`
- Verify filename matches in posts array
- Hard refresh browser (Ctrl+F5)

**Viewer not updating:**
- GitHub Pages takes 2-10 minutes to deploy
- Check commit pushed to `main` branch: `git log`
- Verify at: `https://adamfiverr-lab.github.io/lotte-viewer/?nocache=1`

**Wrong order:**
- Posts auto-sort by date (newest first)
- Check date format: '2026-02-08' (YYYY-MM-DD)

---

## Reference Files

- Daily post script: `/home/gavien/.openclaw/skills/lotte-daily-posting/scripts/daily-post-github.py`
- Prompt template: `/home/gavien/workspace/lotte/LOTTE-PROMPT-TEMPLATE.md`
- Character reference: `/home/gavien/workspace/lotte/skills/lotte-ai-influencer/assets/lotte-reference.jpg`
