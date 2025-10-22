# Getting Started with Product Design Skill

5-minute quickstart guide for Navigator's Figma integration.

---

## 1. Install (30 seconds)

```bash
cd skills/product-design
./setup.sh
```

**Expected output**:
```
✅ Setup Complete!
```

If you see errors, check [INSTALL.md](INSTALL.md) for troubleshooting.

---

## 2. Enable Figma MCP (1 minute)

1. Open **Figma Desktop** app
2. **Figma** → **Preferences** (macOS) or **File** → **Settings** (Windows)
3. Find "**Enable local MCP Server**"
4. Toggle **ON**

You should see: "MCP server running at http://127.0.0.1:3845/mcp"

---

## 3. Try It (2 minutes)

Open Navigator and say:

```
"Review this Figma design: https://figma.com/file/YOUR_FILE_URL"
```

Navigator will automatically:
- ✅ Connect to Figma Desktop
- ✅ Extract design tokens and components
- ✅ Compare against your codebase
- ✅ Generate implementation plan
- ✅ Create Navigator task document

**Output**:
```
✅ Design review complete for Dashboard Redesign

Generated Documentation:
- Design review: .agent/design-system/reviews/2025-10-22-dashboard.md
- Implementation plan: .agent/tasks/TASK-17-dashboard-redesign.md

Summary:
- Design Tokens: 12 new, 5 modified
- Components: 3 new, 1 to extend
- Estimated Time: 12 hours
- Complexity: Medium

Next Steps:
[1] Start implementation now
[2] Review plan first
[3] Modify plan before starting
```

---

## That's It!

You're ready to use Navigator's product-design skill.

### What You Can Do

**Design Review**:
```
"Review this Figma design: [URL]"
```

**Extract Tokens**:
```
"Extract design tokens from Figma"
```

**Check Design System**:
```
"Check design system impact for [feature]"
```

**Generate Implementation Plan**:
```
"Plan implementation for this design"
```

---

## Troubleshooting

### "Figma Desktop not running"

**Fix**: Start Figma Desktop and enable MCP (see step 2 above)

### "Setup failed"

**Fix**: See detailed guide in [INSTALL.md](INSTALL.md)

### "Can't connect to MCP"

**Fix**: Verify port 3845 is accessible:
```bash
curl http://127.0.0.1:3845/mcp
# Should return JSON (even if error message)
```

---

## Learn More

- **[README.md](README.md)** - Features and architecture
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[SKILL.md](SKILL.md)** - Complete skill documentation

---

**Time to get started**: 5 minutes
**Ready to use**: Immediately after setup
