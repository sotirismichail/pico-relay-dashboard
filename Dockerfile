FROM node:14 AS builder
WORKDIR /app
COPY deployment/dashboard/package.json .
RUN npm install

FROM httpd:2.4
COPY --from=builder /app/node_modules /usr/local/apache2/htdocs/node_modules
COPY dashboard/ /usr/local/apache2/htdocs/