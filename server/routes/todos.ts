import { OpenAPIHono, createRoute, z } from '@hono/zod-openapi'

const TodoSchema = z.object({
    id: z.number(),
    name: z.string(),
})

const todos = [
    { id: 1, name: 'Buy groceries' },
    { id: 2, name: 'Buy mobile phone' },
    { id: 3, name: 'Buy laptop' },
]

const router = new OpenAPIHono()

router.openapi(
    createRoute({
        method: 'get',
        path: '/',
        responses: {
            200: {
                content: {
                    'application/json': {
                        schema: z.array(TodoSchema),
                    },
                },
                description: 'Retrieve the list of todos',
            },
        },
    }),
    (c) => c.json(todos)
)

router.openapi(
    createRoute({
        method: 'post',
        path: '/',
        request: {
            body: {
                content: {
                    'application/json': {
                        schema: z.object({ name: z.string() }),
                    },
                },
            },
        },
        responses: {
            201: {
                content: {
                    'application/json': {
                        schema: TodoSchema,
                    },
                },
                description: 'Created a new todo',
            },
        },
    }),
    async (c) => {
        const { name } = c.req.valid('json')
        const todo = { id: todos.length + 1, name }
        todos.push(todo)
        return c.json(todo, 201)
    }
)

export default router
