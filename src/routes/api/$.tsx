import { createFileRoute } from '@tanstack/react-router'
import app from '../../../server/app'

export const Route = createFileRoute('/api/$')({
    server: {
        handlers: {
            GET: ({ request }) => app.request(request),
            POST: ({ request }) => app.request(request),
            PUT: ({ request }) => app.request(request),
            DELETE: ({ request }) => app.request(request),
            PATCH: ({ request }) => app.request(request),
        },
    },
})
