import { OpenAPIHono } from '@hono/zod-openapi'
import { apiReference } from '@scalar/hono-api-reference'
import { auth } from './foundation/auth'
import { logger } from './foundation/logger'
import todos from './routes/todos'
import demo from './routes/demo'

const app = new OpenAPIHono().basePath('/api')

// Middleware
app.use('*', async (c, next) => {
    logger.info({ method: c.req.method, path: c.req.path }, 'Request received')
    await next()
})

// Auth
app.on(['GET', 'POST'], '/auth/*', (c) => auth.handler(c.req.raw))

// Standard Routes
app.get('/health', (c) => c.json({ success: true, data: { status: 'ok' } }))

// API Routes
app.route('/todos', todos)
app.route('/demo', demo)

// OpenAPI & Scalar
app.doc('/doc', {
    openapi: '3.0.0',
    info: {
        title: 'TanStack POC API',
        version: '1.0.0',
    },
})

app.get('/reference', apiReference({
    spec: {
        url: '/api/doc',
    },
}) as any)

export default app
export type AppType = typeof app
