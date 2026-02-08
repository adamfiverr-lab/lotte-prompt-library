#!/bin/bash
# Generate Lotte image from JSON prompt file
# Usage: ./generate-from-json.sh /path/to/prompt.json [size]

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <json-prompt-file> [size]"
    echo "Example: $0 ../../../prompts/highly-explicit/pov-under-table-kneeling.json"
    exit 1
fi

JSON_FILE="$1"
SIZE="${2:-960*1280}"

if [ ! -f "$JSON_FILE" ]; then
    echo "Error: File not found: $JSON_FILE"
    exit 1
fi

echo "📄 Converting JSON prompt: $JSON_FILE"

# Extract and convert JSON to text prompt
python3 << PYTHON
import json
import sys

try:
    with open("$JSON_FILE") as f:
        data = json.load(f)
    
    # Build Lotte character description
    lotte = "Lotte, 22 year old"
    
    char = data.get('character_lock', {})
    if char.get('ethnicity'):
        lotte += f", {char['ethnicity']}"
    
    # Lotte specific traits (override JSON if needed)
    lotte += ", wavy shoulder-length blonde hair, bright blue eyes, tanned golden skin, fit slim-thick figure"
    
    # Body description
    body = char.get('body', {})
    if body.get('chest'):
        lotte += f", {body['chest']} chest"
    if body.get('waist'):
        lotte += f", {body['waist']} waist"
    if body.get('hips'):
        lotte += f", {body['hips']} hips"
    
    # Scene
    scene = data.get('scene', {})
    if scene.get('location'):
        lotte += f", {scene['location']}"
    if scene.get('time'):
        lotte += f", {scene['time']}"
    
    # Subject action
    subject = data.get('subject', {})
    if subject.get('action'):
        lotte += f", {subject['action']}"
    
    # Pose
    pose = subject.get('pose', {})
    if pose.get('position'):
        lotte += f", {pose['position']}"
    if pose.get('expression'):
        lotte += f", {pose['expression']}"
    if pose.get('head'):
        lotte += f", {pose['head']}"
    if pose.get('hands'):
        lotte += f", {pose['hands']}"
    
    # Outfit
    outfit = subject.get('outfit', {})
    if outfit.get('top'):
        top = outfit['top']
        lotte += f", wearing {top.get('color', '')} {top.get('type', '')}"
        if top.get('fit'):
            lotte += f", {top['fit']}"
        if top.get('details'):
            lotte += f", {top['details']}"
    
    if outfit.get('bottom'):
        bottom = outfit['bottom']
        lotte += f", {bottom.get('color', '')} {bottom.get('type', '')}"
        if bottom.get('fit'):
            lotte += f", {bottom['fit']}"
    
    # Environment
    env = data.get('environment', {})
    bg = env.get('background', [])
    if bg:
        lotte += f", {' '.join(bg)}"
    
    if env.get('lighting'):
        light = env['lighting']
        if light.get('type'):
            lotte += f", {light['type']}"
        if light.get('effect'):
            lotte += f", {light['effect']}"
    
    # Camera/meta
    meta = data.get('meta', {})
    if meta.get('style'):
        lotte += f", {meta['style']}"
    if meta.get('camera'):
        lotte += f", {meta['camera']} photo"
    
    # Photography rules
    rules = data.get('photography_rules', {})
    if rules.get('suggestive_not_explicit'):
        lotte += ", suggestive not explicit"
    if rules.get('voyeuristic_energy'):
        lotte += ", voyeuristic energy"
    
    lotte += ", photorealistic"
    
    print(lotte)
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON

echo ""
echo "✅ Conversion complete!"
echo "Use with ./generate.sh 'prompt text above' $SIZE"
