import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

import partsRoutes from './routes/parts.js';
import buildsRoutes from './routes/builds.js';

const app = new Hono();

// Middleware
app.use('*', logger());
app.use('*', cors());

// Health check
app.get('/', (c) => c.json({ 
  name: 'PCParts API',
  version: '0.1.0',
  status: 'ok',
}));

app.get('/health', (c) => c.json({ status: 'ok' }));

// API routes
app.route('/api/parts', partsRoutes);
app.route('/api/builds', buildsRoutes);

// Start server
const port = parseInt(process.env.PORT || '8000');
console.log(`🚀 Server running at http://localhost:${port}`);

serve({ fetch: app.fetch, port });

export default app;
