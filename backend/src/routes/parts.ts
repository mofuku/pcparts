import { Hono } from 'hono';
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';
import { db, schema } from '../db/index.js';
import { eq, like } from 'drizzle-orm';

const app = new Hono();

// List parts
app.get('/', async (c) => {
  const category = c.req.query('category');
  const search = c.req.query('search');
  const limit = parseInt(c.req.query('limit') || '50');
  const offset = parseInt(c.req.query('offset') || '0');

  let query = db.select().from(schema.parts);

  // Note: Complex filtering would need proper query building
  // This is simplified for MVP

  const parts = await db.select().from(schema.parts).limit(limit).offset(offset);

  return c.json({ items: parts, total: parts.length });
});

// Get part by ID
app.get('/:id', async (c) => {
  const id = parseInt(c.req.param('id'));
  
  const part = await db.select()
    .from(schema.parts)
    .where(eq(schema.parts.id, id))
    .limit(1);

  if (!part.length) {
    return c.json({ error: 'Part not found' }, 404);
  }

  // Get specs
  const specs = await db.select()
    .from(schema.partSpecs)
    .where(eq(schema.partSpecs.partId, id));

  // Get latest prices
  const prices = await db.select()
    .from(schema.prices)
    .where(eq(schema.prices.partId, id));

  return c.json({
    ...part[0],
    specs,
    prices,
  });
});

// Get price history
app.get('/:id/history', async (c) => {
  const id = parseInt(c.req.param('id'));
  const days = parseInt(c.req.query('days') || '30');

  const history = await db.select()
    .from(schema.prices)
    .where(eq(schema.prices.partId, id));

  return c.json(history);
});

// Search
app.get('/search', async (c) => {
  const q = c.req.query('q') || '';
  const limit = parseInt(c.req.query('limit') || '20');

  const results = await db.select()
    .from(schema.parts)
    .where(like(schema.parts.fullName, `%${q}%`))
    .limit(limit);

  return c.json({ results, total: results.length });
});

export default app;
