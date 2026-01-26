import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'

const router = new OpenAPIHono()

router.openapi(
    createRoute({
        method: 'get',
        path: '/names',
        responses: {
            200: {
                content: {
                    'application/json': {
                        schema: z.array(z.string()),
                    },
                },
                description: 'Retrieve a list of names',
            },
        },
    }),
    (c) => c.json(['Alice', 'Bob', 'Charlie'])
)

export default router
