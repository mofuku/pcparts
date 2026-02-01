import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core';

// Categories: CPU, GPU, RAM, etc.
export const categories = sqliteTable('categories', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  slug: text('slug').notNull().unique(),
  name: text('name').notNull(),
  icon: text('icon'),
});

// Parts: Deduplicated products
export const parts = sqliteTable('parts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  manufacturer: text('manufacturer').notNull(),
  model: text('model').notNull(),
  fullName: text('full_name').notNull(),
  categoryId: integer('category_id').references(() => categories.id),
  imageUrl: text('image_url'),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
});

// Part specs: Flexible key-value
export const partSpecs = sqliteTable('part_specs', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  partId: integer('part_id').references(() => parts.id).notNull(),
  key: text('key').notNull(),
  value: text('value').notNull(),
  unit: text('unit'),
});

// Retailers: Stores we scrape
export const retailers = sqliteTable('retailers', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  slug: text('slug').notNull().unique(),
  name: text('name').notNull(),
  baseUrl: text('base_url').notNull(),
  countryCode: text('country_code').notNull(),
  currency: text('currency').notNull(),
  isActive: integer('is_active', { mode: 'boolean' }).default(true),
});

// Prices: Append-only for history
export const prices = sqliteTable('prices', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  partId: integer('part_id').references(() => parts.id).notNull(),
  retailerId: integer('retailer_id').references(() => retailers.id).notNull(),
  price: real('price').notNull(),
  currency: text('currency').notNull(),
  inStock: integer('in_stock', { mode: 'boolean' }).default(true),
  productUrl: text('product_url').notNull(),
  scrapedAt: integer('scraped_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
});

// Builds: User configurations
export const builds = sqliteTable('builds', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
});

// Build items: Parts in a build
export const buildItems = sqliteTable('build_items', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  buildId: integer('build_id').references(() => builds.id).notNull(),
  partId: integer('part_id').references(() => parts.id).notNull(),
});

// Compatibility rules
export const compatibilityRules = sqliteTable('compatibility_rules', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  description: text('description'),
  categoryA: text('category_a').notNull(),
  categoryB: text('category_b').notNull(),
  ruleType: text('rule_type').notNull(), // match, lte, gte
  specA: text('spec_a').notNull(),
  specB: text('spec_b').notNull(),
  errorMessage: text('error_message').notNull(),
  severity: text('severity').default('error'),
  isActive: integer('is_active', { mode: 'boolean' }).default(true),
});

// Types
export type Category = typeof categories.$inferSelect;
export type Part = typeof parts.$inferSelect;
export type PartSpec = typeof partSpecs.$inferSelect;
export type Retailer = typeof retailers.$inferSelect;
export type Price = typeof prices.$inferSelect;
export type Build = typeof builds.$inferSelect;
