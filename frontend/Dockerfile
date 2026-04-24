FROM node:22-slim

WORKDIR /app

RUN corepack enable pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --ignore-scripts

COPY . .
RUN pnpm run postinstall

EXPOSE 9000

CMD ["pnpm", "run", "dev"]
