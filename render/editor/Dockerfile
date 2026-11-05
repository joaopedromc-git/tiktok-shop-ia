# Editor de vídeo: HyperFrames (HTML -> MP4) com Chromium e FFmpeg.
# Mesmas dependências do ambiente de produção do HyperFrames (Dockerfile.test do repositório).
# Uso: docker exec editor sh -c "cd /data/<pasta> && hyperframes render ..."
FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl unzip ffmpeg chromium \
      libgbm1 libnss3 libatk-bridge2.0-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 \
      libcups2 libasound2 libpangocairo-1.0-0 libxshmfence1 libgtk-3-0 \
      fonts-liberation fonts-noto-color-emoji fonts-noto-core fonts-dejavu-core \
      fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Fontes de display do Google Fonts (licença OFL), instaladas no sistema para o render não depender de internet
RUN mkdir -p /usr/share/fonts/truetype/google && cd /usr/share/fonts/truetype/google \
    && for f in montserrat/Montserrat%5Bwght%5D.ttf anton/Anton-Regular.ttf bebasneue/BebasNeue-Regular.ttf archivoblack/ArchivoBlack-Regular.ttf \
                poppins/Poppins-Bold.ttf poppins/Poppins-ExtraBold.ttf poppins/Poppins-Black.ttf poppins/Poppins-SemiBold.ttf \
                bricolagegrotesque/BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf \
                inter/Inter%5Bopsz%2Cwght%5D.ttf dmserifdisplay/DMSerifDisplay-Regular.ttf; do \
         curl -fsSLO "https://raw.githubusercontent.com/google/fonts/main/ofl/$f"; done \
    && fc-cache -f

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    CONTAINER=true

# chrome-headless-shell: renderização determinística (BeginFrame), onde o HyperFrames procura
RUN npx --yes @puppeteer/browsers install chrome-headless-shell@stable --path /root/.cache/puppeteer

# Versão fixa: atualizar aqui (e rebuild) em vez de dentro do container
RUN npm install -g hyperframes@0.8.214 && hyperframes --version

WORKDIR /data
CMD ["sleep", "infinity"]
