FROM node:18

WORKDIR /app
COPY . .

ARG VITE_BACKEND_API_URL
ENV VITE_BACKEND_API_URL=$VITE_BACKEND_API_URL

RUN npm install
RUN npm run build

RUN npm install -g serve

# Serve the built app
CMD ["serve", "-s", "dist", "-l", "5173"]
