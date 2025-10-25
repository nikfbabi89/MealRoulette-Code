npm init -y
npm install express better-sqlite3 uuid body-parser


// server.js
// Core routes for Meal Roulette: load, add/edit, list with filters, and spin
const express = require('express');
const Database = require('better-sqlite3');
const { v4: uuidv4 } = require('uuid');
const bodyParser = require('body-parser');
const path = require('path');

const DB_PATH = path.join(__dirname, 'meals.db');
const db = new Database(DB_PATH);

// create table if missing (DDL adapted from your doc)
db.prepare(`
CREATE TABLE IF NOT EXISTS meals (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT,             -- JSON string array
  prep_time_min INTEGER,
  difficulty TEXT,
  ingredients TEXT,      -- JSON string array
  notes TEXT,
  weight INTEGER DEFAULT 1,
  last_cooked TEXT       -- ISO date
);
`).run();

const app = express();
app.use(bodyParser.json());

// ---------- Helpers ----------
function parseJSONSafe(s, fallback = []) {
  try {
    return s ? JSON.parse(s) : fallback;
  } catch (e) {
    return fallback;
  }
}

// simple seeded PRNG: mulberry32
// seed with integer
function mulberry32(seed) {
  return function() {
    seed |= 0;
    seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// Weighted random selection using provided RNG (function returning [0,1))
function weightedPick(items, weightFn, rng = Math.random) {
  const total = items.reduce((s, it) => s + Math.max(0, weightFn(it) || 0), 0);
  if (total === 0) return null;
  let r = rng() * total;
  for (const it of items) {
    const w = Math.max(0, weightFn(it) || 0);
    if (r < w) return it;
    r -= w;
  }
  return items[items.length - 1];
}

// Basic validation for a meal payload
function validateMealPayload(payload) {
  if (!payload || !payload.name || payload.name.trim() === '') {
    return { ok: false, error: 'name is required' };
  }
  if (payload.prep_time_min != null && (!Number.isInteger(payload.prep_time_min) || payload.prep_time_min < 0)) {
    return { ok: false, error: 'prep_time_min must be integer >= 0' };
  }
  if (payload.weight != null && (!Number.isInteger(payload.weight) || payload.weight < 1)) {
    return { ok: false, error: 'weight must be integer >= 1' };
  }
  return { ok: true };
}

// ---------- Routes ----------

// GET /meals
// optional query params: type (single), max_prep (integer), difficulty, visible (true|false)
// This returns the filtered meal list (does not modify DB)
app.get('/meals', (req, res) => {
  try {
    const rows = db.prepare('SELECT * FROM meals').all();
    let meals = rows.map(r => ({
      ...r,
      type: parseJSONSafe(r.type, []),
      ingredients: parseJSONSafe(r.ingredients, []),
    }));

    // apply filters from query
    const { type, max_prep, difficulty, exclude } = req.query;
    if (type) meals = meals.filter(m => m.type.includes(type));
    if (max_prep != null) {
      const n = parseInt(max_prep, 10);
      if (!Number.isNaN(n)) meals = meals.filter(m => (m.prep_time_min == null ? Infinity : m.prep_time_min) <= n);
    }
    if (difficulty) meals = meals.filter(m => (m.difficulty || '').toLowerCase() === difficulty.toLowerCase());
    if (exclude) {
      const excludes = Array.isArray(exclude) ? exclude : exclude.split(',');
      meals = meals.filter(m => !excludes.some(e => (m.type || []).includes(e)));
    }

    res.json({ ok: true, count: meals.length, meals });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: 'internal_error' });
  }
});

// POST /meals  -> create new meal
app.post('/meals', (req, res) => {
  const payload = req.body;
  const v = validateMealPayload(payload);
  if (!v.ok) return res.status(400).json({ ok: false, error: v.error });

  const id = payload.id || 'm-' + uuidv4();
  const stmt = db.prepare(`
    INSERT INTO meals (id, name, type, prep_time_min, difficulty, ingredients, notes, weight, last_cooked)
    VALUES (@id, @name, @type, @prep_time_min, @difficulty, @ingredients, @notes, @weight, @last_cooked)
  `);

  const row = {
    id,
    name: payload.name,
    type: JSON.stringify(payload.type || []),
    prep_time_min: payload.prep_time_min != null ? payload.prep_time_min : null,
    difficulty: payload.difficulty || null,
    ingredients: JSON.stringify(payload.ingredients || []),
    notes: payload.notes || null,
    weight: payload.weight != null ? payload.weight : 1,
    last_cooked: payload.last_cooked || null
  };

  try {
    stmt.run(row);
    res.status(201).json({ ok: true, meal: { ...row, type: JSON.parse(row.type), ingredients: JSON.parse(row.ingredients) } });
  } catch (err) {
    console.error(err);
    if (err.code === 'SQLITE_CONSTRAINT_PRIMARYKEY') {
      return res.status(409).json({ ok: false, error: 'id_already_exists' });
    }
    res.status(500).json({ ok: false, error: 'db_error' });
  }
});

// PUT /meals/:id -> update (partial allowed)
app.put('/meals/:id', (req, res) => {
  const id = req.params.id;
  const existing = db.prepare('SELECT * FROM meals WHERE id = ?').get(id);
  if (!existing) return res.status(404).json({ ok: false, error: 'not_found' });

  const payload = req.body;
  const merged = {
    ...existing,
    ...payload,
    type: payload.type ? JSON.stringify(payload.type) : existing.type,
    ingredients: payload.ingredients ? JSON.stringify(payload.ingredients) : existing.ingredients,
  };

  const v = validateMealPayload(merged);
  if (!v.ok) return res.status(400).json({ ok: false, error: v.error });

  const stmt = db.prepare(`
    UPDATE meals SET
      name = @name,
      type = @type,
      prep_time_min = @prep_time_min,
      difficulty = @difficulty,
      ingredients = @ingredients,
      notes = @notes,
      weight = @weight,
      last_cooked = @last_cooked
    WHERE id = @id
  `);

  try {
    stmt.run({
      id,
      name: merged.name,
      type: merged.type,
      prep_time_min: merged.prep_time_min,
      difficulty: merged.difficulty,
      ingredients: merged.ingredients,
      notes: merged.notes,
      weight: merged.weight,
      last_cooked: merged.last_cooked
    });
    res.json({ ok: true });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: 'db_error' });
  }
});

// POST /spin
// Body: { filters: { type, max_prep, difficulty, exclude }, seed?: integer|string }
// Returns selected meal object (and updates last_cooked in DB)
app.post('/spin', (req, res) => {
  try {
    const { filters = {}, seed } = req.body || {};

    // load all meals then filter in JS (simple & flexible)
    const rows = db.prepare('SELECT * FROM meals').all();
    let meals = rows.map(r => ({
      ...r,
      type: parseJSONSafe(r.type, []),
      ingredients: parseJSONSafe(r.ingredients, [])
    }));

    // enforce only visible/active if you have such a field in JSON; for now we assume all rows are valid
    // apply filters (same logic as /meals)
    if (filters.type) meals = meals.filter(m => m.type.includes(filters.type));
    if (filters.max_prep != null) {
      const n = parseInt(filters.max_prep, 10);
      if (!Number.isNaN(n)) meals = meals.filter(m => (m.prep_time_min == null ? Infinity : m.prep_time_min) <= n);
    }
    if (filters.difficulty) meals = meals.filter(m => (m.difficulty || '').toLowerCase() === filters.difficulty.toLowerCase());
    if (filters.exclude) {
      const excludes = Array.isArray(filters.exclude) ? filters.exclude : String(filters.exclude).split(',');
      meals = meals.filter(m => !excludes.some(e => (m.type || []).includes(e)));
    }

    if (!Array.isArray(meals) || meals.length === 0) {
      return res.status(400).json({ ok: false, error: 'no_meals_after_filters', message: 'Add meals or relax filters.'});
    }

    // choose RNG: seeded if seed provided, else Math.random
    let rng = Math.random;
    if (seed != null) {
      // turn seed into integer
      let sInt = 0;
      const sStr = String(seed);
      for (let i = 0; i < sStr.length; i++) sInt = (sInt * 31 + sStr.charCodeAt(i)) >>> 0;
      rng = mulberry32(sInt);
    }

    // pick by weight
    const picked = weightedPick(meals, m => m.weight || 1, rng);
    if (!picked) return res.status(500).json({ ok: false, error: 'selection_failed' });

    // update last_cooked to now (ISO)
    const nowIso = new Date().toISOString();
    db.prepare('UPDATE meals SET last_cooked = ? WHERE id = ?').run(nowIso, picked.id);

    // return picked meal (freshly updated)
    const updated = db.prepare('SELECT * FROM meals WHERE id = ?').get(picked.id);
    const mealOut = {
      ...updated,
      type: parseJSONSafe(updated.type, []),
      ingredients: parseJSONSafe(updated.ingredients, [])
    };

    res.json({ ok: true, seed: seed ?? null, selected: mealOut });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: 'internal_error' });
  }
});

// POST /import -> import JSON file payload { json: {...} } (simple)
app.post('/import', (req, res) => {
  const payload = req.body && req.body.json;
  if (!payload || !Array.isArray(payload.Meals) && !Array.isArray(payload)) {
    return res.status(400).json({ ok: false, error: 'invalid_import_format' });
  }

  const mealsArr = Array.isArray(payload.Meals) ? payload.Meals : payload;
  const insert = db.prepare(`
    INSERT INTO meals (id, name, type, prep_time_min, difficulty, ingredients, notes, weight, last_cooked)
    VALUES (@id, @name, @type, @prep_time_min, @difficulty, @ingredients, @notes, @weight, @last_cooked)
  `);

  const insertMany = db.transaction((items) => {
    for (const m of items) {
      const id = m.id || ('m-' + uuidv4());
      const row = {
        id,
        name: m.Name || m.name,
        type: JSON.stringify(m.Groups || m.type || []),
        prep_time_min: m.PrepTime != null ? m.PrepTime : (m.prep_time_min || null),
        difficulty: m.Difficulty || m.difficulty || null,
        ingredients: JSON.stringify(m.Ingredients || m.ingredients || []),
        notes: m.Notes || m.notes || null,
        weight: m.Weight != null ? m.Weight : (m.weight != null ? m.weight : 1),
        last_cooked: m.LastCooked || m.last_cooked || null
      };
      insert.run(row);
    }
  });

  try {
    insertMany(mealsArr);
    res.json({ ok: true, imported: mealsArr.length });
  } catch (err) {
    console.error(err);
    res.status(500).json({ ok: false, error: 'import_failed', detail: err.message });
  }
});

// GET /export -> return all meals as JSON object
app.get('/export', (req, res) => {
  const rows = db.prepare('SELECT * FROM meals').all();
  const meals = rows.map(r => ({
    id: r.id,
    name: r.name,
    type: parseJSONSafe(r.type, []),
    prep_time_min: r.prep_time_min,
    difficulty: r.difficulty,
    ingredients: parseJSONSafe(r.ingredients, []),
    notes: r.notes,
    weight: r.weight,
    last_cooked: r.last_cooked
  }));
  res.json({ ok: true, count: meals.length, meals });
});

// start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Meal Roulette server listening on port ${PORT}`);
});




Notes / rationale





Persistence: Uses SQLite (better-sqlite3) and auto-creates table from your DDL. This matches your document.
Spin Engine: Implements weighted selection and supports an optional seed for deterministic picks (useful for testing). The PRNG is simple and deterministic (mulberry32 seeded from the provided seed string).
Filters: Both GET /meals and POST /spin support filters (type, max_prep, difficulty, exclude). Filtering is done in JS for flexibility (you can push more filtering into SQL later).
Validation & Errors: Basic validation on create/update. Spin returns a helpful error if zero meals after filters.
Import/Export: Simple /import (accepts your JSON structure) and /export endpoints for demo/demo-ready persistence swap.




Spin (random): POST /spin with body { "filters": { "type": "Dinner" } }
Spin (seeded/deterministic): POST /spin with { "filters": { "type": "Dinner" }, "seed": "test-001" }
