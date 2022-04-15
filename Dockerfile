# note: override config via node config env variables (https://github.com/node-config/node-config/wiki/Environment-Variables)
FROM node:17.9-alpine3.14
WORKDIR /dist
COPY csl/dependent dependent
COPY csl/renamed-styles.json renamed-styles.json
COPY csljson csljson
COPY csljson-locales csljson-locales
COPY lib lib
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN mkdir config && echo '{\
"cslPath": "./csljson",\
"localesPath": "./csljson-locales",\
"renamedStylesPath": "./renamed-styles.json",\
"cslDependentPath": "./dependent",\
"port": "8085"\
}' > config/default.json
RUN npm install
EXPOSE 8085
CMD ["node", "lib/citeServer.js"]

