FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f pnpm-lock.yaml ]; then npm i -g pnpm && pnpm i --frozen-lockfile; \
	elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
	elif [ -f package-lock.json ]; then npm ci; else npm i; fi
COPY . .
RUN if [ -f pnpm-lock.yaml ]; then pnpm build; \
	elif [ -f yarn.lock ]; then yarn build; else npm run build; fi

FROM node:20-alpine
ENV NITRO_PORT=3000 HOST=0.0.0.0 NODE_ENV=production
WORKDIR /app
COPY --from=build /app/.output ./.output
EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]