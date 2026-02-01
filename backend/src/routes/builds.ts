import { Hono } from 'hono';
import { db, schema } from '../db/index.js';
import { eq } from 'drizzle-orm';
import { CompatibilityChecker } from '../services/compatibility.js';

const app = new Hono();

// List builds
app.get('/', async (c) => {
  const builds = await db.select().from(schema.builds);
  return c.json({ items: builds });
});

// Create build
app.post('/', async (c) => {
  const body = await c.req.json<{ name: string }>();
  
  const result = await db.insert(schema.builds)
    .values({ name: body.name })
    .returning();

  return c.json(result[0], 201);
});

// Get build by ID
app.get('/:id', async (c) => {
  const id = parseInt(c.req.param('id'));

  const build = await db.select()
    .from(schema.builds)
    .where(eq(schema.builds.id, id))
    .limit(1);

  if (!build.length) {
    return c.json({ error: 'Build not found' }, 404);
  }

  // Get build items with parts
  const items = await db.select()
    .from(schema.buildItems)
    .where(eq(schema.buildItems.buildId, id));

  const partIds = items.map(i => i.partId);
  
  // Get parts with specs (simplified - would need proper joins)
  const parts = [];
  for (const partId of partIds) {
    const part = await db.select().from(schema.parts).where(eq(schema.parts.id, partId)).limit(1);
    const specs = await db.select().from(schema.partSpecs).where(eq(schema.partSpecs.partId, partId));
    const category = part[0]?.categoryId 
      ? await db.select().from(schema.categories).where(eq(schema.categories.id, part[0].categoryId)).limit(1)
      : [];
    
    if (part[0]) {
      parts.push({ ...part[0], specs, category: category[0] || null });
    }
  }

  return c.json({
    ...build[0],
    parts,
  });
});

// Add part to build
app.post('/:id/parts', async (c) => {
  const buildId = parseInt(c.req.param('id'));
  const body = await c.req.json<{ partId: number }>();

  await db.insert(schema.buildItems)
    .values({ buildId, partId: body.partId });

  return c.json({ success: true }, 201);
});

// Remove part from build
app.delete('/:id/parts/:partId', async (c) => {
  const buildId = parseInt(c.req.param('id'));
  const partId = parseInt(c.req.param('partId'));

  await db.delete(schema.buildItems)
    .where(eq(schema.buildItems.buildId, buildId));

  return c.json({ success: true });
});

// Check build compatibility
app.get('/:id/compatibility', async (c) => {
  const id = parseInt(c.req.param('id'));

  // Get build items
  const items = await db.select()
    .from(schema.buildItems)
    .where(eq(schema.buildItems.buildId, id));

  // Get parts with specs and categories
  const parts = [];
  for (const item of items) {
    const part = await db.select().from(schema.parts).where(eq(schema.parts.id, item.partId)).limit(1);
    const specs = await db.select().from(schema.partSpecs).where(eq(schema.partSpecs.partId, item.partId));
    const category = part[0]?.categoryId 
      ? await db.select().from(schema.categories).where(eq(schema.categories.id, part[0].categoryId)).limit(1)
      : [];
    
    if (part[0]) {
      parts.push({ 
        ...part[0], 
        specs, 
        category: category[0] ? { slug: category[0].slug } : undefined 
      });
    }
  }

  const checker = new CompatibilityChecker();
  const result = checker.checkBuild(parts as any);

  return c.json(result);
});

export default app;
