# Starfield banner generator

Self-contained Python that writes an animated `assets/starfield.svg` (1200×300).
Twinkling starfield + constellation lines + brighter stars + one shooting star.
No external deps. Run, then commit `assets/starfield.svg`.

```python
import random
random.seed(42)
W, H = 1200, 300
stars = [(random.uniform(0,W), random.uniform(0,H), random.uniform(0.4,1.8),
          random.uniform(2.0,5.0), random.uniform(0,5.0), random.uniform(0.3,0.9))
         for _ in range(140)]
star_svg = []
for x,y,r,dur,delay,op in stars:
    star_svg.append(
        f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="#cfe3ff" opacity="{op:.2f}">\n'
        f'    <animate attributeName="opacity" values="{op:.2f};{min(op+0.4,1):.2f};{op:.2f}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>\n'
        f'    <animate attributeName="r" values="{r:.2f};{r*1.6:.2f};{r:.2f}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>\n'
        f'  </circle>')
bright = [(180,90),(320,140),(470,80),(610,170),(760,110),(900,150),(1040,95)]
lines = [f'  <line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#7aa2ff" stroke-width="0.6" opacity="0.25"/>'
         for (a,b),(c,d) in zip(bright, bright[1:])]
bright_c = [f'  <circle cx="{x}" cy="{y}" r="2.4" fill="#ffffff"><animate attributeName="opacity" values="0.6;1;0.6" dur="3s" repeatCount="indefinite"/></circle>'
            for x,y in bright]
shooting = ('  <g opacity="0"><line x1="0" y1="0" x2="40" y2="0" stroke="url(#trail)" stroke-width="1.5"/>\n'
            '    <animateTransform attributeName="transform" type="translate" from="-50 60" to="1250 260" dur="6s" begin="2s" repeatCount="indefinite"/>\n'
            '    <animate attributeName="opacity" values="0;1;1;0" dur="6s" begin="2s" repeatCount="indefinite"/></g>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">
  <defs><radialGradient id="bg" cx="50%" cy="40%" r="80%"><stop offset="0%" stop-color="#11142a"/><stop offset="55%" stop-color="#0a0c1a"/><stop offset="100%" stop-color="#04060f"/></radialGradient>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="#ffffff" stop-opacity="0"/><stop offset="100%" stop-color="#cfe3ff" stop-opacity="1"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
{chr(10).join(lines)}
{chr(10).join(bright_c)}
{chr(10).join(star_svg)}
{shooting}
</svg>'''
open("assets/starfield.svg","w").write(svg)
```

Embed in README:
`![starfield](https://raw.githubusercontent.com/USER/USER/main/assets/starfield.svg)`
