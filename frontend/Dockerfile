FROM node:20-alpine
WORKDIR /app
COPY package.json pnpm-lock.yaml* yarn.lock* package-lock.json* ./
RUN corepack enable || true
RUN if [ -f pnpm-lock.yaml ]; then corepack prepare pnpm@latest --activate && pnpm install; \
    elif [ -f yarn.lock ]; then yarn; else npm install; fi
COPY . .
EXPOSE 3000
# Use project local Nuxt
CMD [ "npm", "run", "dev" ]
