---
type: synthesis
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/synthesis
  - adhd-workflow
---

# ADHD Workflow Optimization — Context-Switching Strategies

Patterns and techniques for rapid context-switching between 20+ projects without losing focus or direction.

## The ADHD Challenge

Your workspace has 20+ projects across 4 ecosystems. Without strategies, context-switching causes:
- **Context Whiplash** — Jump between unrelated projects, lose momentum
- **Thrashing** — Switching so fast that nothing gets done
- **Hyperfocus Traps** — Get lost in one project and forget what else needs doing
- **Information Overload** — So many projects that you don't know where to start

## The Solution: Structured Context-Switching

Instead of free-form jumping, use these patterns.

---

## Pattern 1: The "Themed Day" Approach

**Idea:** Dedicate time blocks to each ecosystem. Don't switch between TTRPG and AWS on the same day.

### Sample Weekly Schedule

```
Monday    → TTRPG Ecosystem (all TTRPG work)
Tuesday   → AWS Infrastructure (all infrastructure work)
Wednesday → AI/LLM Ecosystem (all AI work)
Thursday  → Utilities & Learning (library/tool work)
Friday    → Cross-Project Synthesis (integrate, plan, document)
```

**Benefits:**
- Deep focus (whole day in one ecosystem)
- Less context-switching overhead
- Brain builds momentum
- Friday synthesis prevents island-ifying

**Challenges:**
- Sometimes you need to cross ecosystems
- Inspiration might strike in "wrong" project

**Modification:** Theme by task instead of project:
```
Monday    → Feature Development (build new features across all projects)
Tuesday   → Bug Fixes (fix issues across all projects)
Wednesday → Documentation (write docs for all projects)
Thursday  → Testing (test across all projects)
Friday    → Deployment (release across all projects)
```

---

## Pattern 2: The "Energy-Matched" Approach

**Idea:** Match project complexity to your available mental energy. Different projects demand different cognitive load.

### Energy Levels

**High Energy (Morning):**
- Architecture design (AWS infrastructure, API design)
- Algorithm work (encounter generation, music composition)
- Complex debugging

**Medium Energy (Midday):**
- Feature implementation
- Code refactoring
- Testing and validation

**Low Energy (Late afternoon/tired):**
- Documentation
- Code review
- Simple utility work
- CI/CD setup

### Example Workflow

```
9 AM (Fresh):       Cartographers-Cloud-Kit API design
11 AM (Still high): AWS CDK infrastructure
1 PM (Post-lunch):  TTRPG-AI-RAG feature implementation
3 PM (Afternoon):   Cellophane library testing
5 PM (Tired):       Update documentation, run CI/CD
```

**Benefits:**
- Maximizes effectiveness
- Less frustration (not fighting energy levels)
- Natural breaks built in

---

## Pattern 3: The "Interrupt Buffer" Approach

**Idea:** Keep one "interrupt project" ready for context-switching.

**Interrupt Project:**
- Low cognitive load
- Quick wins possible
- No long context needed
- Can start/stop in 15 minutes

**Examples:**
- [[Wiki/entities/My-Mini-Projects]] (add new tutorial, experiment)
- [[Wiki/entities/FunWithMusic]] (run existing tutorial)
- [[Wiki/entities/Close-Application]] (validation task)
- [[Wiki/entities/MidnightsGitHubActions]] (add new workflow template)

**Workflow:**

```
Primary work: Complex TTRPG rule system (high focus)
  ↓
Waiting for tests to run (5-10 min delay)
  ↓
Switch to Interrupt Project: Add Deno tutorial to My-Mini-Projects
  ↓
Quick win complete (15 min)
  ↓
Tests finished, back to TTRPG
```

**Benefits:**
- Productive while waiting
- No heavy context-switching cost
- Maintains momentum

---

## Pattern 4: The "Anchor Project" Approach

**Idea:** Choose one project as your "anchor"—the one that grounds your week.

**Anchor Project Criteria:**
- Most important to you right now
- Clear, achievable goals
- Has momentum
- Return to it often

**Weekly Rhythm:**

```
Monday:   Anchor Project (2-3 hours focused work)
Tuesday:  Anchor Project + Related Projects (same ecosystem)
Wednesday: Explore Other Ecosystems (maintain breadth)
Thursday:  Anchor Project (another 2-3 hours)
Friday:   Reflect, plan next week's anchor
```

**Current Suggested Anchor:** [[Wiki/entities/TableTopMaestro]]
- Campaign management framework
- Integrates with TTRPG ecosystem
- Needed for long-term goals
- Clear path forward

**Benefits:**
- Provides stability
- Makes progress on what matters most
- Easier to say "no" to other projects

---

## Pattern 5: The "Quick Start Checklist" Approach

**Idea:** Before switching projects, use a 2-minute ritual to get context back.

### Context-Switch Ritual

```
1. [ ] Save your current project (commit/save work)
2. [ ] Write 1-line note: "Stopped here: [what you were doing]"
3. [ ] Close IDE/terminal
4. [ ] Take a 30-second break (stand up, stretch)
5. [ ] Read the Quick-Switch Guide for target project
6. [ ] Open target project
7. [ ] Read your previous stopping note (if returning)
8. [ ] Start work
```

**Time:** ~2 minutes (includes 30-second break)

**Benefits:**
- Ritual signals "context switch" to your brain
- Written note helps you return
- Break prevents mental exhaustion

---

## Pattern 6: The "Sync & Capture" Approach

**Idea:** Once per day, sync documentation and capture learnings.

### Daily Sync (5-10 minutes)

```
End of day, before leaving:

1. [ ] Did I learn something new? 
        → Update wiki concept pages
        
2. [ ] Did I hit a bug/issue?
        → Document in project README
        
3. [ ] Did I discover a pattern?
        → Add to Wiki/concepts/
        
4. [ ] Are there new dependencies?
        → Update Shared-Infrastructure-Map
        
5. [ ] Ready for next day?
        → Commit all work
        → Write stopping note
        → Plan tomorrow
```

**Benefits:**
- Wiki stays current
- Knowledge compounds
- Easier to return to projects
- Prevents information loss

---

## Pattern 7: The "Ecosystem Focus Cycle" Approach

**Idea:** Rotate through ecosystems on a 2-week cycle, not daily.

### 2-Week Cycles

```
Weeks 1-2:   TTRPG Ecosystem (build features, refactor, test)
Weeks 3-4:   AWS Infrastructure (deploy, optimize, monitor)
Weeks 5-6:   AI/LLM Ecosystem (experiment, benchmark, integrate)
Weeks 7-8:   Utilities & Learning (libraries, CI/CD, documentation)
Week 9:      Cross-Ecosystem Synthesis (integrate, plan, document)
Week 10+:    Repeat
```

**Benefits:**
- Deep focus per ecosystem
- Momentum builds over 2 weeks
- Break mental pattern every 2 weeks
- Friday synthesis prevents isolation

---

## Pattern 8: The "Hyperfocus Exploit" Approach

**Idea:** Recognize hyperfocus as a feature, not a bug. Channel it strategically.

### When Hyperfocus Strikes

**DON'T:** Fight it or switch projects prematurely  
**DO:** Let it run, but set a time boundary

```
Hyperfocus on: Complex TTRPG rule system
Boundary set: 4 hours
Timer set: 4-hour alarm

During 4 hours:
  - Close all notifications
  - No interrupts (except emergency)
  - Pure focus zone
  
After 4 hours:
  - Take 30-min break
  - Eat, walk, reset
  - Decide: Continue hyperfocus or switch?
```

**Benefits:**
- Harness ADHD strengths
- Massive progress in short time
- Prevents burnout (bounded time)
- Still maintains project variety

---

## Anti-Patterns to Avoid

### ❌ "Let Me Just Quickly Check..."

**What Happens:**
- "Let me just quickly look at Cartographers-Cloud-Kit"
- 45 minutes later, still in that project
- Lost context from original work

**Fix:** Never "just check." Use the ritual (Pattern 5).

### ❌ "I'll Finish This Later"

**What Happens:**
- Never finish anything
- Jump between incomplete tasks
- Frustration accumulates

**Fix:** Commit to finishing current task before switching. Even if incomplete, explicitly decide "pause for X reason, resume tomorrow."

### ❌ "Context Tsunami"

**What Happens:**
- Open 8 projects in 1 hour
- Brain overloaded
- Productivity drops to zero

**Fix:** Limit switches to 2-3 per day. Use patterns (1-4) to prevent this.

### ❌ "Hyperfocus Forever"

**What Happens:**
- Get trapped in one project for 3 days
- Other projects atrophy
- Burn out

**Fix:** Use Pattern 8 (boundary hyperfocus with time limits).

---

## Weekly Planning Template

Use this to plan your week:

```markdown
# Weekly Plan (2026-08-07 to 2026-08-13)

## Anchor Project
- [ ] TableTopMaestro: Complete Phase 1 data model

## Energy-Matched Tasks
- [ ] Mon 9 AM (high): Data model design
- [ ] Mon 2 PM (medium): Schema implementation
- [ ] Tue 9 AM (high): Encounter generation architecture
- [ ] Wed 2 PM (medium): Unit tests

## Ecosystem Exposure
- [ ] TTRPG (primary): TableTopMaestro + Automated-Taskmaster
- [ ] AWS (secondary): Review My-DDNS-Updater logs
- [ ] Utilities (maintenance): Update CI/CD workflows

## Interrupt Projects
- [ ] My-Mini-Projects: Add Rust tutorial (if waiting)
- [ ] FunWithMusic: Run SCAMP example (if blocked)

## Friday Synthesis
- [ ] Update Wiki/synthesis/ADHD-Workflow-Optimization with this week's learnings
- [ ] Review dependencies: Did anything break?
- [ ] Plan next week's anchor project

## Wins This Week
- (To be filled Friday)
- (To be filled Friday)
```

---

## The 80/20 Rule: Focus on What Matters

**Reality:** You can't maintain all 20+ projects equally.

**Solution:** Use Pareto Principle—20% of projects probably generate 80% of your value.

**Your 20%:**
- **Anchor Project** (highest priority)
- **Key Infrastructure** (my-shared-infra, Homelab)
- **One utility library** (Cellophane)

**Maintenance (80%):**
- TTRPG projects (run when needed)
- AI projects (experiment occasionally)
- Other utilities (update only when needed)

**Permission Granted:** You don't need to develop all projects equally. Pick 2-3 to focus on; maintain the rest.

---

## Tools & Reminders

### Set Phone Reminders

```
9 AM: "Start anchor project (2 hours focus)"
12 PM: "Lunch break + 30 min walk"
1 PM: "Medium-energy work (2 hours)"
4 PM: "Low-energy work or interrupt project"
5 PM: "Daily sync & plan tomorrow"
```

### Use Wiki as Your Dashboard

- Start each day reading [[Wiki/synthesis/Project-Dashboard]]
- Plan using [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]]
- Check dependencies in [[Wiki/synthesis/Shared-Infrastructure-Map]]

### Keep This Page Open

Bookmark [[Wiki/synthesis/ADHD-Workflow-Optimization]] for quick reference.

---

## Key Principle

**Context-switching is not failure. It's how ADHD brains work.**

The goal is not to eliminate switching—it's to make switching **fast, deliberate, and productive**.

Choose a pattern (or mix of patterns) that feels natural. Iterate. Your workflow will evolve as you learn what works.

**Start with Pattern 1 (Themed Days). Add other patterns as needed.**

---

## Related Synthesis Pages

- [[Wiki/synthesis/Project-Dashboard]] — All projects at a glance
- [[Wiki/synthesis/Quick-Switch-Guide-by-Ecosystem]] — Fast jumps between projects
- [[Wiki/synthesis/Shared-Infrastructure-Map]] — Understand dependencies
