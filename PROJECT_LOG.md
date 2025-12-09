# Branch: Reading-First Research Companion - Project Log

## Project Overview
A reading-first system that helps users capture, defer, and develop ideas during reading without breaking flow.

**Started:** December 9, 2025  
**Primary Language:** Python  
**Status:** 🟡 In Progress

---

## Phase 1: Project Setup & Infrastructure

### 1.1 Repository Setup
- [ ] Initialize Git repository
- [ ] Create GitHub repository (branch-research-companion)
- [ ] Setup branch protection rules
- [ ] Create initial project structure

### 1.2 Development Environment
- [ ] Create Python virtual environment
- [ ] Setup `pyproject.toml` with modern Python packaging
- [ ] Configure development dependencies (pytest, black, ruff, mypy)
- [ ] Setup pre-commit hooks
- [ ] Create `.env.example` for environment variables

### 1.3 Project Structure
- [ ] Create source directory structure
- [ ] Setup configuration management
- [ ] Create initial README.md
- [ ] Add LICENSE file
- [ ] Create CONTRIBUTING.md

### 1.4 CI/CD Setup
- [ ] GitHub Actions for testing
- [ ] GitHub Actions for linting
- [ ] Dependabot configuration

---

## Phase 2: Core Data Layer

### 2.1 Data Models
- [ ] Document model
- [ ] IdeaFragment model (content, anchor, timestamp, status)
- [ ] BranchSession model
- [ ] Database schema design

### 2.2 Storage Layer
- [ ] SQLite for local storage (MVP)
- [ ] Repository pattern implementation
- [ ] Migration system setup

---

## Phase 3: Document Reader

### 3.1 PDF Support
- [ ] PDF rendering engine selection
- [ ] Text extraction with position mapping
- [ ] Page navigation
- [ ] Zoom and scroll handling

### 3.2 Text/Markdown Support
- [ ] Plain text reader
- [ ] Markdown rendering
- [ ] Syntax highlighting for code blocks

---

## Phase 4: Idea Capture System

### 4.1 Capture Mechanisms
- [ ] Text input capture
- [ ] Voice capture (speech-to-text)
- [ ] Stylus/drawing capture (future)

### 4.2 Context Anchoring
- [ ] Text selection anchoring
- [ ] Page/position anchoring
- [ ] Timestamp association

---

## Phase 5: Branch Buffer

### 5.1 Buffer Interface
- [ ] Chronological idea queue view
- [ ] Idea review interface
- [ ] Pruning/archiving functionality
- [ ] Promotion to permanent notes

---

## Phase 6: UI/UX Layer

### 6.1 Framework Decision
- [ ] Evaluate: Desktop (Tauri + Python backend) vs Web (FastAPI + React)
- [ ] Mobile consideration for "away from desk" use case

### 6.2 Reading Interface
- [ ] Minimal distraction reader view
- [ ] Quick capture overlay
- [ ] Three-action interaction model

---

## Phase 7: Optional AI Features

### 7.1 Local AI Integration
- [ ] Lightweight local LLM for "Resolve Lightly"
- [ ] Privacy-first approach
- [ ] Ollama integration consideration

---

## Development Sessions Log

### Session 1 - December 9, 2025
**Goal:** Project initialization and repository setup  
**Chat Log:** `docs/dev-logs/session-001-project-setup.md`  
**Status:** 🟡 In Progress

**Completed:**
- [ ] Reviewed PRD document
- [ ] Created project log structure
- [ ] ...

**Decisions Made:**
- Primary language: Python
- ...

**Next Steps:**
- Initialize git repository
- Create GitHub repo
- Setup Python environment

---

## Architecture Decisions Record (ADR)

### ADR-001: Primary Language Selection
**Date:** December 9, 2025  
**Status:** Proposed  
**Context:** Need to choose primary development language  
**Decision:** Python for backend/core logic  
**Rationale:** 
- User proficiency
- Rich ecosystem for PDF handling, NLP, and AI
- Fast prototyping capability

### ADR-002: Application Type (TBD)
**Date:** TBD  
**Status:** Pending  
**Options:**
1. Desktop app (Tauri + Python backend)
2. Web app (FastAPI + frontend framework)
3. Cross-platform (React Native / Flutter + Python API)

---

## Resources & References

- PRD: `Branch_PRD_Reading_First_Research_Companion.pdf`
- Dev Logs: `docs/dev-logs/`
- Copilot Chats: `docs/copilot-chats/`

