# Python-Stock-Market-Analyzer

# Phase-1: RSI Indicator Validation Engine (Python | CLI)

> Objective:
> Build a minimal, deterministic RSI computation pipeline that matches
> TradingView’s indicator logic by validating data integrity,
> initialization assumptions, and smoothing mechanics.

---

## Why this exists

Most RSI implementations fail to match TradingView because they treat RSI
as a *stateless formula*.

It is not.

RSI is a recursive time-series function whose correctness depends on:

- data ordering
- initialization method
- averaging strategy
- state propagation across periods

This phase intentionally avoids high-level libraries to expose these
assumptions explicitly.

---

## System Scope (Phase-1)

RAW CSV (exchange data)
        ↓
Data Cleaning & Normalization
        ↓
Strict Type Validation
        ↓
Gain / Loss Decomposition
        ↓
Initial RSI Calculation (SMA-based)

No optimization.
No backtesting.
No UI.

Correctness first.

---

## Indicator Logic Implemented

### 1. Price Change Decomposition
- Positive change → Gain
- Negative change → Loss
- Zero change → Neutral (0,0)

### 2. Initial RSI (14-period)

Average Gain  = SUM(Gain[1..14]) / 14  
Average Loss  = SUM(Loss[1..14]) / 14  

RS = AvgGain / AvgLoss  
RSI = 100 − (100 / (1 + RS))

> Note:
> This computes the *first valid RSI value*.
> Wilder-smoothed RSI is intentionally excluded in Phase-1.

---

## Key Insight Discovered

Same formula ≠ same indicator.

TradingView displays the *latest smoothed RSI*,
not the initial SMA-based RSI.

Stopping after the first RSI produces a mathematically valid value,
but it is **not comparable** to TradingView unless smoothing is applied.

Indicators are stateful.

---

## Design Choices (Intentional)

- No pandas / ta-lib
- Explicit CSV parsing
- Manual type casting
- Row-level validation
- Deterministic execution order

These trade performance for transparency.

---

## Folder Structure

RAW/
  └── Exchange CSV files

DATA/
  └── CLEAN/
      └── SYMBOL_YYYY-MM-DD.csv

---

## Limitations (By Design)

- Computes only the initial RSI value
- No Wilder smoothing yet
- No MA crossover logic
- No signal generation
- No backtesting engine

All deferred to Phase-2.

---

## Phase-2 Roadmap (Planned)

- Wilder RSI smoothing
- RSI-based moving average
- Signal classification
- Cross-platform parity checks
- Multi-period evaluation

---

## Philosophy

> Numerical finance is about *process*, not formulas.

Correct indicators emerge from correct state handling,
not copy-pasted equations.

---

## Feedback

Beginners:
- Use this as a reference for understanding RSI internals.

Experienced developers / quants:
- I welcome corrections, critiques, and implementation challenges.

---

Built to learn.
Built to be wrong early.
Built to converge to truth.
